from fastapi import APIRouter, Body, Query, Depends

from .models import TelNumber
from .tgclient import TTClientsManager as TTCManager

router = APIRouter(tags=["api"])


@router.post("/api/login")
async def api_login(phone: TelNumber):
    """
    tel получается не используется.
    :param phone:
    :param tel: номер телефона клиента для авторизации.
    :return: url: str. URL для QR-кода для авторизации.
    """
    print("api_login: tel: {}".format(phone))
    qr_login_url = await TTCManager.get_qrcode_url(phone.phone)
    return {'qr_link_url': qr_login_url}


@router.get("/api/check/status")
async def api_check_status(phone: TelNumber = Depends(TelNumber)):
    print("api_check_status: {}".format(phone))
    return {'status': await TTCManager.get_auth_status(phone.phone)}


@router.get("/api/get/dialogs")
async def api_get_dialogs(phone: str = Query(regex=r"^\d{11,}$")):
    print("api_get_dialogs: {}".format(phone))
    return {'dialogs': await TTCManager.get_dialogs(phone)}


@router.get("/api/get/messages")
async def api_get_dialogs(phone: str = Query(regex=r"^\d{11,}$"), entity: str = Query()):
    print("api_get_dialogs: {}".format(phone))
    return {'messages': await TTCManager.get_messages(phone, entity)}


