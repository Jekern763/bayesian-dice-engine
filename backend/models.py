from decimal import Decimal
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import UUID4, AfterValidator, BaseModel, Field


def validate_uuid4(v: str) -> str:
    UUID4(v)
    return v


StrUUID4 = Annotated[str, AfterValidator(validate_uuid4)]


# type of record for all database sort keys
class RecordType(StrEnum):
    MID_SESSION = "mid_session"
    SESSION_LOG = "session_log"


# schemas for api calls
class StartGameSchema(BaseModel):
    riskiness: float = Field(
        ..., gt=0, description="Must be a positive float greater than 0"
    )
    jackpot: float = Field(
        ..., ge=1, description="Must be a float greater than or equal to 1"
    )


class GuessGameSchema(BaseModel):
    session_id: StrUUID4 = Field(..., description="Current session id in UUID4 form")
    guess: int = Field(
        ...,
        ge=2,
        le=12,
        description="The valid guess of the sum of two dice: an integer between 2 and 12",
    )
    other_data: dict[str, Decimal] = Field(
        ...,
        description="All other supplemetary data",
    )


# schemas for database put requests
class GameTemporaryRow(BaseModel):
    session_id: StrUUID4 = Field(..., description="Current session id in StrUUID4 form")
    record_type: Literal[RecordType.MID_SESSION] = RecordType.MID_SESSION
    game: str = Field(
        ..., description="The complete current game state in a dictionary state"
    )
    ttl: str = Field(
        ...,
        description="The unix epch timestamp in seconds when this row will be deleted",
    )


class GamePermanentDataRow(BaseModel):
    session_id: StrUUID4 = Field(..., description="Current session id in StrUUID4 form")
    record_type: Literal[RecordType.SESSION_LOG] = RecordType.SESSION_LOG

    game: str = Field(
        ..., description="The complete current game state in a dictionary state"
    )

    payout: Decimal = Field(
        ..., description="Total payout for the session in decimal form (not float)"
    )

    other_data: dict[str, Decimal] = Field(
        ..., description="All other supplemetary data"
    )
