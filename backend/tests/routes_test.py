import json
import app
from uuid import uuid4
from game_engine.game import Game


class MockContext:
    def __init__(self, function_name="test-function", request_id="12345-abc"):
        # Define the attributes your Lambda uses
        self.function_name = function_name
        self.function_version = "$LATEST"
        self.invoked_function_arn = (
            f"arn:aws:lambda:us-east-1:123456789012:function:{function_name}"
        )
        self.memory_limit_in_mb = 128
        self.aws_request_id = request_id
        self.log_group_name = f"/aws/lambda/{function_name}"
        self.log_stream_name = "2026/06/05/[$LATEST]abcdef"

    def get_remaining_time_in_millis(self):
        return 5000


def test_start_game_success(mocker):
    mock_create = mocker.patch.object(app.database_gateway, "create_session")

    mock_event = {
        "rawPath": "api/start-game",
        "requestContext": {"stage": "$default", "http": {"method": "post"}},
        "body": json.dumps({"riskiness": 3.0, "jackpot": 10.0}),
        "headers": {"content-type": "application/json"},
    }

    response = app.lambda_handler(mock_event, MockContext())

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "session_id" in body
    assert len(body["peeks"]) == 4

    mock_create.assert_called_once()


def test_start_game_failiure(mocker):
    mocker.patch.object(app.database_gateway, "create_session")

    mock_event = {
        "rawPath": "api/start-game",
        "requestContext": {"stage": "$default", "http": {"method": "post"}},
        # invalid riskiness multiplier
        "body": json.dumps({"riskiness": -1.0, "jackpot": 10.0}),
        "headers": {"content-type": "application/json"},
    }
    response = app.lambda_handler(mock_event, MockContext())
    assert response["statusCode"] == 422


def test_guess_success(mocker):
    mock_read = mocker.patch.object(app.database_gateway, "get_active_session")
    mocker.patch.object(app.database_gateway, "commit_guess_transaction")

    mock_read.return_value = {"game": Game(8, 10).to_json()}

    mock_event = {
        "rawPath": "api/guess",
        "requestContext": {"stage": "$default", "http": {"method": "post"}},
        "body": json.dumps({"session_id": str(uuid4()), "guess": 7}),
    }

    response = app.lambda_handler(mock_event, MockContext())

    assert response["statusCode"] == 200
    assert "payout" in json.loads(response["body"])

    mock_read.assert_called_once()


def test_guess_failiure(mocker):
    mock_read = mocker.patch.object(app.database_gateway, "get_active_session")
    mocker.patch.object(app.database_gateway, "commit_guess_transaction")

    mock_read.return_value = {"game": Game(8, 10).to_json()}

    mock_event = {
        "rawPath": "api/guess",
        "requestContext": {"stage": "$default", "http": {"method": "post"}},
        "body": json.dumps({"session_id": str(uuid4()), "guess": 13}),  # invalid guess
    }

    response = app.lambda_handler(mock_event, MockContext())

    assert response["statusCode"] == 422
