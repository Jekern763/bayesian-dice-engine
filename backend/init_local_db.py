# backend/init_local_db.py
import boto3
from botocore.exceptions import ClientError

# Connected via your verified local testing parameters
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://127.0.0.1:8000",
    region_name="us-east-1",
    aws_access_key_id="fakeAccessKeyId",
    aws_secret_access_key="fakeSecretAccessKey",
)
TABLE_NAME = "BayesianDiceSessions"


def setup_fresh_table():
    client = dynamodb.meta.client
    table = dynamodb.Table(TABLE_NAME)

    # --- STEP 1: DELETE EXISTING TABLE IF IT EXISTS ---
    try:
        print(f"Checking for existing table '{TABLE_NAME}'...")
        table.delete()
        print(f"Deleting old version of '{TABLE_NAME}', waiting for clearance...")

        # Force Python to wait until the table is completely purged from Docker memory
        client.get_waiter("table_not_exists").wait(TableName=TABLE_NAME)
        print("Old table successfully removed.")
    except ClientError as e:
        # If the table didn't exist in the first place, ignore the error and move on
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            print("No existing table found. Proceeding straight to creation.")
        else:
            raise e

    # --- STEP 2: CREATE FRESH TABLE WITH COMPOSITE KEY SCHEMA ---
    try:
        print(f"Carving out fresh layout for '{TABLE_NAME}'...")
        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "session_id", "KeyType": "HASH"},  # Partition Key
                {"AttributeName": "record_type", "KeyType": "RANGE"},  # Sort Key
            ],
            AttributeDefinitions=[
                {"AttributeName": "session_id", "AttributeType": "S"},
                {"AttributeName": "record_type", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )

        # Wait until the new structure is physically active
        client.get_waiter("table_exists").wait(TableName=TABLE_NAME)
        print("Successfully created fresh local table structure.")

        # --- STEP 3: ENABLE THE TTL SPECIFICATION ---
        print("Activating Time to Live (TTL) engine targeting the 'ttl' attribute...")
        client.update_time_to_live(
            TableName=TABLE_NAME,
            TimeToLiveSpecification={"Enabled": True, "AttributeName": "ttl"},
        )
        print("--- Database Initialization Complete! Fresh Slate Active. ---")

    except Exception as e:
        print(f"Table creation sequence failed: {e}")


if __name__ == "__main__":
    setup_fresh_table()
