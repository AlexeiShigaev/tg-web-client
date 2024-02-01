from fastapi import APIRouter, Request, status, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from .aiohttpconnector import AiohttpConnector
from .models import TelNumber, QRUrl, AuthStatus

# from qrcode import QRCode

router = APIRouter(tags=["client"])
templates = Jinja2Templates(directory="src/client/templates")


@router.get('/nak', status_code=200)
async def ping_pong_response():
    """
    Элементарное эхо, отвечает на обращение.
    :return: kan, code 200
    """
    return "kan"


@router.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    """
    Отдаем страницу для ввода номера телефона, нужен для авторизации.
    :param request: номер телефона
    :return: 200, перенаправляет на страницу авторизации по QR-коду.
    """
    return templates.TemplateResponse(
        request=request, name="hello.html", status_code=status.HTTP_200_OK
    )


# @router.post("/login/")  # = Depends()
# async def get_qr_code(tel: TelNumber):
#     """
#     Обращение к API для авторизации по QR-коду.
#     На первом этапе надо предъявить номер телефона, его отправим на API, получим url на авторизацию,
#     отправим клиенту.
#     Второй этап - ожидание авторизации клиента, используй обращение к /check/login смены статуса на logged_in.
#     :param tel: Словарь должен содержать номер телефона.
#     :return: str: урл для авторизации через QR_code
#     """
#     print("get_qr_code:login: telephone number:", tel.phone)
#     ret = await AiohttpConnector.method_post_to_url(
#         url="http://localhost:8899/api/login",
#         json_data=tel.json()
#     )
#     print("\tret:::: ", ret)
#     try:
#         qr_url_d = QRUrl(*ret)
#     except Exception as ex:
#         print("get_qr_code: Не понятно что вернулось, но это нам не надоть: ", ex)
#         return "error"
#     # qr = QRCode()
#     # qr.add_data(qr_url_d.qr_link_url)
#     # qr.print_ascii()
#     return qr_url_d


# @router.get("/check/statuss")
# async def get_status(phone: str = Query(regex=r"^\d{11,}$")):
#     print("Запрос на проверку статуса {}".format(phone))
#     ret = await AiohttpConnector.method_get_to_url(
#         url="http://localhost:8899/api/check/login?phone={}".format(phone)
#     )
#     print("\tres=", ret)
#     try:
#         stat = AuthStatus(**ret['data'])
#     except Exception as e:
#         # print("Получили ерунду какую-то:{}\nОшибка: {}".format(ret, e))
#         return AuthStatus('error')
#     return stat


@router.get("/client")
async def get_web_client(request: Request, phone: str = Query(regex=r"^\d{11,}$")):
    return templates.TemplateResponse(
        request=request, name="client.html", status_code=status.HTTP_200_OK, context={'phone': phone}
    )


# @router.get("/get/dialogs")
# async def get_dialogs(phone: str = Query(regex=r"^\d{11,}$")):
#     print("get_dialogs для {}".format(phone))
#     ret = await AiohttpConnector.method_get_to_url(
#         url="http://localhost:8890/get/dialogs?phone={}".format(phone)
#     )
#     print("\tret=", ret)
#     return ret

