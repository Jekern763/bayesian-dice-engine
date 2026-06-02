# backend/test_direct_router.py
import json
import os

# Force local database connectivity parameters
os.environ["LOCAL_DEV"] = "true"

# Import the core API router directly, bypassing the lambda_handler decorator
from app import app

def run_direct_session():
    print("=== Running Direct API Router Test ===")

    # ---------------------------------------------------------
    # STEP 1: Start a Game Session
    # ---------------------------------------------------------
    print("\n[STEP 1] Direct Route: GET /start-game/multipliers/3/100")
    
    start_event = {
        "rawPath": "/start-game/multipliers/3/100",
        "requestContext": {
            "stage": "$default",  # Added to satisfy Powertools internal router
            "http": {
                "method": "GET"
            }
        }
    }

    start_response = app.resolve(start_event, None)
    
    print(f"-> Status Code: {start_response['statusCode']}")
    start_body = json.loads(start_response["body"])
    print(f"-> Returned Body: {start_body}")

    session_id = start_body.get("session_id")

    # ---------------------------------------------------------
    # STEP 2: Submit a Guess against that Session
    # ---------------------------------------------------------
    print(f"\n[STEP 2] Direct Route: POST /guess for Session: {session_id}")
    
    guess_payload = {
        "session_id": session_id,
        "guess": 15
    }

    guess_event = {
        "rawPath": "/guess",
        "requestContext": {
            "stage": "$default",  # Added here as well
            "http": {
                "method": "POST"
            }
        },
        "body": json.dumps(guess_payload),
        "headers": {
            "content-type": "application/json"
        }
    }

    guess_response = app.resolve(guess_event, None)
    
    print(f"-> Status Code: {guess_response['statusCode']}")
    print(f"-> Returned Body: {json.loads(guess_response['body'])}")
    print("\n=== End-to-End Session Execution Verified ===")

if __name__ == "__main__":
    run_direct_session()