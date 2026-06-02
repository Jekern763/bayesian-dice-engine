from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.event_handler.exceptions import NotFoundError

# Initialize Powertools utilities
logger = Logger()
tracer = Tracer()

# Initialize the API Router
app = APIGatewayHttpResolver()

@app.get("/start-game")
@tracer.capture_method
def start_game():
    pass

@app.post("/guess")
@tracer.capture_method
def guess():
    request_data = app.current_event.json_body
    pass

