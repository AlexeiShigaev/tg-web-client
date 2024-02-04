from sqlmodel import SQLModel, Field

from fastapi import Query
# from pydantic import BaseModel


class TelNumber(SQLModel):
    phone: str = Field(Query(regex=r"^\d{11,}$"))

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    # for phone number ru: +7-921-921-0123
                    "phone": "79219210123"
                }
            ]
        }
    }


class QRUrl(SQLModel):
    qr_link_url: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "qr_link_url": "tg://login?token=AQJiMqJl_k2_2fpmykG0oaPb4IVIscgUg"
                }
            ]
        }
    }


class AuthStatus(SQLModel):
    status: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "waiting_qr_auth"
                }
            ]
        }
    }


# *******************************************************************************

class DialogBase(SQLModel):
    name: str
    artist: str


class DialogsRecord(DialogBase, table=True):
    __tablename__ = "dialogs"
    id: int = Field(default=None, primary_key=True)
