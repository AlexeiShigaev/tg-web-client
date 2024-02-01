from fastapi import Query
from pydantic import BaseModel, Field


class TelNumber(BaseModel):
    phone: str = Field(Query(regex=r"^\d{11,}$"))

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "phone": "+7-9219219211"
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


"""
Данные передаваемы от телеграм помещаем в следующие структуры.
class PeerUser(BaseModel):
    user_id: int


class PeerChannel(BaseModel):
    channel_id: int


class Message(BaseModel):
    id: int
    peer_id: Union[PeerUser, PeerChannel, None]
    message: str
    out: bool


class MessageService(BaseModel):
    id: int
    peer_id: Union[PeerUser, PeerChannel, None]


class Dialog(BaseModel):
    name: str
    # date: datetime.datetime
    message: Message


"""


# PeerUser = namedtuple('PeerUser', ('user_id', ))
#
# PeerChannel = namedtuple('PeerChannel', ('channel_id', ))
#
# Message = namedtuple('Message', ('id', 'peer_id'))
#
# MessageService = namedtuple('MessageService', ('id', 'peer_id'))
#
# Dialog = namedtuple('Dialog', ('name', 'out', 'message', 'message'))

# @dataclass
# class PeerUser:
#     user_id: int
#
#
# @dataclass
# class PeerChannel:
#     channel_id: int
#
#
# @dataclass
# class Message:
#     id: int
#     peer_id: Union[PeerUser, PeerChannel, None]
#     message: str
#     out: bool
#
#
# @dataclass
# class MessageService:
#     id: int
#     peer_id: Union[PeerUser, PeerChannel, None]
#
#
# @dataclass
# class Dialog:
#     name: str
#     # date: datetime.datetime
#     out: bool
#     # message: str
#     # message: Message = None






