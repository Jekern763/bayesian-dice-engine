from decimal import Decimal
from uuid import uuid4

import boto3
import pytest
from database_gateway import DatabaseGateway
from game_engine.game import Game
from models import RecordType
from moto import mock_aws

TABLE_NAME = "dynamodb-test"
SESSION_ID = str(uuid4())


@pytest.fixture
def mock_dynamodb(mocker):
    with mock_aws():
        # Initialize the mock resource
        dynamodb = boto3.resource(
            "dynamodb",
            region_name="us-east-1",
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
        )

        # Build the same table architecture
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "session_id", "KeyType": "HASH"},
                {"AttributeName": "record_type", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "session_id", "AttributeType": "S"},
                {"AttributeName": "record_type", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        # Wait until the virtual infrastructure component is ready
        table.meta.client.get_waiter("table_exists").wait(TableName=TABLE_NAME)

        yield table


@pytest.fixture()
def gateway(mock_dynamodb):
    return DatabaseGateway(TABLE_NAME, is_local=False)


def test_gateway_init(gateway):
    assert gateway.table.name == TABLE_NAME

    key_schema = gateway.table.key_schema
    assert key_schema[0]["AttributeName"] == "session_id"
    assert key_schema[1]["AttributeName"] == "record_type"


def test_create_session(mock_dynamodb, gateway):
    game = Game(8, 10)
    for _ in range(4):
        game.peek()
    gateway.create_session(SESSION_ID, game.to_json())

    response = mock_dynamodb.get_item(
        Key={"session_id": SESSION_ID, "record_type": "mid_session"}
    )

    assert "Item" in response

    item = response["Item"]

    assert item["session_id"] == SESSION_ID


def test_get_active_session(mock_dynamodb, gateway):
    game = Game(8, 10)

    for _ in range(4):
        game.peek()
    mock_dynamodb.put_item(
        Item={
            "session_id": SESSION_ID,
            "record_type": RecordType.MID_SESSION,
            "game": game.to_json(),
        }
    )
    response = mock_dynamodb.get_item(
        Key={"session_id": SESSION_ID, "record_type": RecordType.MID_SESSION}
    )
    gateway_response = gateway.get_active_session(SESSION_ID)
    assert gateway_response["session_id"] == response["Item"]["session_id"]


def test_commit_guess_transaction(mock_dynamodb, gateway):
    game = Game(8, 10)
    for _ in range(4):
        game.peek()

    guess = 7
    payout = game.guess(guess)

    mock_dynamodb.put_item(
        Item={
            "session_id": SESSION_ID,
            "record_type": RecordType.MID_SESSION,
            "game": game.to_json(),
        }
    )

    gateway.commit_guess_transaction(str(SESSION_ID), game.to_json(), Decimal(payout))

    response = mock_dynamodb.get_item(
        Key={"session_id": SESSION_ID, "record_type": str(RecordType.SESSION_LOG)}
    )

    assert "Item" in response

    item = response["Item"]

    assert item["payout"] == Decimal(payout)
