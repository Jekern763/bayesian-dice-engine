from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.event_handler.exceptions import NotFoundError, BadRequestError
from game_engine.game import Game
from uuid import uuid4
import boto3
import os
from enums import RecordType
from decimal import Decimal

MID_SESSION = RecordType.MID_SESSION
SESSION_LOG = RecordType.SESSION_LOG

logger = Logger(service="BayesianDiceAPI")
tracer = Tracer(service="BayesianDiceAPI")

app = APIGatewayHttpResolver(enable_validation=True)

IS_LOCAL = os.environ.get("AWS_SAM_LOCAL") == "true" or os.environ.get("LOCAL_DEV") == "true"
TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "BayesianDiceSessions")

if IS_LOCAL:
    logger.info("Connecting to LOCAL DynamoDB instance at http://127.0.0.1:8000")
    dynamodb = boto3.resource('dynamodb',
        endpoint_url='http://127.0.0.1:8000', # Stable loopback 
        region_name='us-east-1',
        aws_access_key_id='fakeAccessKeyId', # Strict alpha credentials
        aws_secret_access_key='fakeSecretAccessKey'
    )
else:
    logger.info("Connecting to PRODUCTION AWS DynamoDB")
    dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(TABLE_NAME)

@app.get("/start-game/multipliers/<riskiness>/<jackpot>")
@tracer.capture_method
def start_game(riskiness: int, jackpot: int):
    try:
        session_id = str(uuid4())
        logger.append_keys(session_id=session_id)
        
        new_game = Game(riskiness, jackpot)
        peeks = [new_game.peek() for _ in range(4)]

        game_state = new_game.to_json()

        table.put_item(Item={
            "session_id": session_id,
            "record_type": MID_SESSION,
            "game": game_state
        })
        
        return {"session_id": session_id, "peeks": peeks}
    except Exception as e:
        logger.exception("Failed to initialize game environment")
        raise BadRequestError(str(e))


@app.post("/guess")
@tracer.capture_method
def guess():
    request_data = app.current_event.json_body
    try:
        user_guess = request_data["guess"]
        session_id = request_data["session_id"]
        
        logger.append_keys(session_id=session_id) # Fixed typo 'sesion_id'
        
        # Pull envelope and check existence to avoid KeyErrors
        session_data = table.get_item(Key={
            "session_id": session_id,
            "record_type": MID_SESSION
        })
        
        item = session_data.get("Item")
        if not item:
            raise NotFoundError("Active session not found or already completed.")
            
        game_json = item["game"]
        hydrated_game = Game.from_json(game_json)

        payout = hydrated_game.guess(user_guess)
        payout_decimal = Decimal(str(payout))

        # 1. Log permanent transaction history
        table.put_item(Item={
            "session_id": session_id,
            "record_type": SESSION_LOG,
            "game": hydrated_game.to_json(),
            "payout": payout_decimal
        })

        # 2. Delete the active session row so the user can't double-submit
        table.delete_item(Key={
            "session_id": session_id,
            "record_type": MID_SESSION
        })

        return {"session_id": session_id, "payout": payout_decimal}

    except KeyError as e:
        raise BadRequestError(f"Missing required parameter: {str(e)}")
    except Exception as e:
        logger.exception("Failure during processing of user guess interaction")
        raise BadRequestError(str(e))


@logger.inject_lambda_context(clear_state=True)
def lambda_handler(event, context):
    raw_path = event.get("rawPath", "")
    if raw_path.startswith("/api"):
        event["rawPath"] = raw_path.replace("/api", "", 1)
    return app.resolve(event, context)