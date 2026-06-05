from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, Response
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from game_engine.game import Game
from uuid import uuid4
import boto3
import os
from models import RecordType, StartGameSchema, GuessGameSchema
from decimal import Decimal
from pydantic import ValidationError
from database_gateway import DatabaseGateway

MID_SESSION = RecordType.MID_SESSION
SESSION_LOG = RecordType.SESSION_LOG

logger = Logger(service="BayesianDiceAPI")
tracer = Tracer(service="BayesianDiceAPI")

app = APIGatewayHttpResolver(enable_validation=True)

IS_LOCAL = os.environ.get("AWS_SAM_LOCAL") == "true" or os.environ.get("LOCAL_DEV") == "true"
TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "BayesianDiceSessions")

database_gateway = DatabaseGateway(TABLE_NAME, IS_LOCAL)


# Exception Handlers
@app.exception_handler(Exception)
def handle_generic_error(exception: Exception) -> Response:
    logger.exception("An unexpected internal runtime error occurred.")
    
    return Response(
        status_code=500,
        content_type="application/json",
        body={"error": "Internal Server Error", "message": "An unexpected error occurred on our end."}
    )

@app.exception_handler(ValidationError)
def handle_validation_error(excpetion: ValidationError) -> Response:
    logger.exception("Invalid data input for post request")
    return Response(status_code=400, 
        content_type="application/json",
        body={"error": "Bad Request", "message": str(excpetion)})

@app.exception_handler(NotFoundError)
def handle_not_found_error(exception: NotFoundError) -> Response:
    logger.exception("Session not found in internal servers")
    return Response(status_code=422,
            content_type="application/json",
            body = {"error": "Unprocessable Content", "message": str(exception)})


# request paths
@app.post("/start-game/multipliers")
@tracer.capture_method
def start_game():
    validated_data = StartGameSchema(**app.current_event.json_body) #could raise ValidationError
    session_id = str(uuid4())
    logger.append_keys(session_id=session_id)
    
    new_game = Game(validated_data.riskiness, validated_data.jackpot)
    peeks = [new_game.peek() for _ in range(4)]

    game_state = new_game.to_json()

    database_gateway.create_session(session_id, game_state)
    
    return {"session_id": session_id, "peeks": peeks}


@app.post("/guess")
@tracer.capture_method
def guess():
    validated_data = GuessGameSchema(**app.current_event.json_body)
    logger.append_keys(session_id=validated_data.session_id)
    
    # Pull envelope and check existence to avoid KeyErrors
    item = database_gateway.get_active_session(str(validated_data.session_id))
    
    if not item:
        raise NotFoundError("Active session not found or already completed.")
        
    game_json = item["game"] # old game data
    hydrated_game = Game.from_json(game_json)

    payout = hydrated_game.guess(validated_data.guess)
    payout_decimal = Decimal(str(payout))

    database_gateway.commit_guess_transaction(str(validated_data.session_id), 
                                              hydrated_game.to_json(),
                                              payout_decimal)

    return {"session_id": validated_data.session_id, "payout": payout_decimal}


@logger.inject_lambda_context(clear_state=True)
def lambda_handler(event, context):
    raw_path = event.get("rawPath", "")
    if raw_path.startswith("/api"):
        event["rawPath"] = raw_path.replace("/api", "", 1)
    return app.resolve(event, context)