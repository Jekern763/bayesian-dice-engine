# backend/reset_local_db.py
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://127.0.0.1:8000',
    region_name='us-east-1',
    aws_access_key_id='fakeAccessKeyId',
    aws_secret_access_key='fakeSecretAccessKey'
)
table_name = 'BayesianDiceSessions'

def reset_table():
    table = dynamodb.Table(table_name)
    
    # 1. Try to delete the table if it exists
    try:
        print(f"Deleting table '{table_name}'...")
        table.delete()
        
        # Wait until the table is fully removed from memory
        table.meta.client.get_waiter('table_not_exists').wait(TableName=table_name)
        print("Table successfully deleted.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("Table didn't exist yet. Skipping deletion.")
        else:
            raise e

    # 2. Re-create the table using your exact schema configuration
    print(f"Re-creating table '{table_name}'...")
    new_table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'session_id', 'KeyType': 'HASH'},    # Partition Key
            {'AttributeName': 'record_type', 'KeyType': 'RANGE'}   # Sort Key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'session_id', 'AttributeType': 'S'},
            {'AttributeName': 'record_type', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    new_table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print("--- Database Reset Complete! Fresh Slate Ready. ---")

if __name__ == "__main__":
    reset_table()