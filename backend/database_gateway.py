from decimal import Decimal
from time import time
from typing import Any, Dict, Optional

import boto3
from aws_lambda_powertools import Logger
from boto3.dynamodb.types import TypeSerializer
from models import GamePermanentDataRow, GameTemporaryRow, RecordType

logger = Logger(child=True)  # Inherits configuration from your main logger
serializer = TypeSerializer()


class DatabaseGateway:
    def __init__(self, table_name: str, is_local: bool = False):
        self.table_name = table_name

        # initialize both the high-level resource and low-level client
        if is_local:
            self.resource = boto3.resource(
                "dynamodb",
                endpoint_url="http://127.0.0.1:8000",
                region_name="us-east-1",
                aws_access_key_id="dummy",
                aws_secret_access_key="dummy",
            )
            self.client = boto3.client(
                "dynamodb",
                endpoint_url="http://127.0.0.1:8000",
                region_name="us-east-1",
                aws_access_key_id="dummy",
                aws_secret_access_key="dummy",
            )
        else:
            self.resource = boto3.resource("dynamodb", "us-east-1")
            self.client = boto3.client("dynamodb", "us-east-1")

        self.table = self.resource.Table(table_name)

    def create_session(self, session_id: str, game_state: str) -> None:
        # Saves a new game session to the table.
        ten_days_in_seconds = 10 * 24 * 60 * 60
        ttl_timestamp = int(time()) + ten_days_in_seconds
        row = GameTemporaryRow(
            session_id=session_id, game=game_state, ttl=str(ttl_timestamp)
        )
        self.table.put_item(
            Item=row.model_dump(mode="python"),
            ConditionExpression="attribute_not_exists(session_id)",
        )

    def get_active_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        # Fetches an active game state, returning None if it doesn't exist
        response = self.table.get_item(
            Key={"session_id": session_id, "record_type": RecordType.MID_SESSION}
        )
        return response.get("Item")

    def commit_guess_transaction(
        self, session_id: str, game_state: str, payout: Decimal, other_data
    ) -> None:
        # excutes an atomic  write and delete operation.
        row = GamePermanentDataRow(
            session_id=session_id, game=game_state, payout=payout, other_data=other_data
        )
        self.client.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": self.table_name,
                        "Item": {
                            k: serializer.serialize(v)
                            for k, v in row.model_dump(mode="python").items()
                        },
                    }
                },
                {
                    "Delete": {
                        "TableName": self.table_name,
                        "Key": {
                            "session_id": {"S": session_id},
                            "record_type": {"S": RecordType.MID_SESSION},
                        },
                        "ConditionExpression": "attribute_exists(session_id)",
                    }
                },
            ]
        )
