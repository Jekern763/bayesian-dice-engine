# backend/peek_db.py
import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://127.0.0.1:8000",
    region_name="us-east-1",
    aws_access_key_id="fakeAccessKeyId",
    aws_secret_access_key="fakeSecretAccessKey",
)
table = dynamodb.Table("BayesianDiceSessions")


def dump_table():
    print("--- Scanning Local Database Content ---")
    response = table.scan()
    items = response.get("Items", [])

    if not items:
        print("The database is currently completely empty.")
        return

    for idx, item in enumerate(items, 1):
        print(f"\n[ROW {idx}]")
        print(f"  Partition Key (session_id): {item.get('session_id')}")
        print(f"  Sort Key (record_type):     {item.get('record_type')}")
        print(f"  Attributes:")
        for key, val in item.items():
            if key not in ["session_id", "record_type"]:
                print(f"    - {key}: {val}")


if __name__ == "__main__":
    dump_table()
