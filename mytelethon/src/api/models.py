from fastapi import Query
from pydantic import BaseModel, Field


class TelNumber(BaseModel):
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


class QRUrl(BaseModel):
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


class AuthStatus(BaseModel):
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

