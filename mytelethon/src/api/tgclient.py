import asyncio
import json
from collections import namedtuple
from fastapi.responses import JSONResponse
from typing import Tuple, Optional, List, Dict

from telethon import TelegramClient, events
from telethon.helpers import TotalList
from telethon.tl.custom import QRLogin
from dataclasses import dataclass

from telethon.tl.types import PeerUser, PeerChannel

from .utils import object_to_dict, to_dict_req

TELEGRAM_API_ID = 19247042
TELEGRAM_API_HASH = "46da5b325cae69f8e8fab4f70b93e7ba"

DISCONNECTED = (0, "disconnected")
CONNECTED = (1, "connected")
WAITING_QR_AUTH = (2, "waiting_qr_auth")
AUTHORIZED = (3, "authorized")


class TTClient(TelegramClient):
    status = DISCONNECTED
    qr_login_obj: QRLogin = None
    dialogs = {}
    messages = {}

    async def my_event_handler(self, event):
        print("NewMessage contents dialog_to_dict:", object_to_dict(event))
        print("NewMessage contents to_dict_req:", to_dict_req(event))


@dataclass()
class WaitQRCodeAuthTask:
    client: TTClient

    async def wait_qrcode_accept(self):
        if self.client.status == WAITING_QR_AUTH:
            try:
                print("\tЖдем авторизации.")
                await self.client.qr_login_obj.wait(40)
                self.client.status = AUTHORIZED
            except Exception as ex:
                print("\tНе дождались. Напрашивается новый запрос на логин\n\tEx: {}".format(ex))
                # Не факт, но вернем в готовность к логину. Он и перезапросит новый QR
                self.client.status = CONNECTED
        return self.client.status[1]


# MessageService = namedtuple('MessageService', ('id', 'peer_id'))
#
# User = namedtuple('User', ('id', 'contact', 'bot', 'first_name', 'last_name', 'username'))
#
# Dialog = namedtuple('Dialog', ('name', 'message', 'entity'))


class TTClientsManager:
    clients: Dict[str, TTClient] = {}
    waiting_tasks = []

    @classmethod
    async def get_client_by_tel(cls, tel: str) -> Optional[TTClient]:
        # print("get_client_by_tel {}".format(tel))
        if tel in cls.clients:
            return cls.clients[tel]

        loop = asyncio.get_event_loop()
        new_client = TTClient("sn{}".format(tel), TELEGRAM_API_ID, TELEGRAM_API_HASH, loop=loop)
        new_client.add_event_handler(new_client.my_event_handler, events.NewMessage)
        new_client.status = DISCONNECTED
        cls.clients[tel] = new_client

        try:
            await cls.clients[tel].connect()
        except OSError as ex:
            # print("get_client_by_tel {}: connection error {}".format(tel, ex))
            cls.clients[tel].disconnect()
            del cls.clients[tel]
            return None

        cls.clients[tel].status = CONNECTED
        cls.clients[tel].status = AUTHORIZED if await cls.clients[tel].is_user_authorized() else WAITING_QR_AUTH

        return cls.clients[tel]

    @classmethod
    async def worker(cls, task: WaitQRCodeAuthTask):
        try:
            await task.wait_qrcode_accept()
        except Exception as ex:
            print("TTClientsManager: worker: exception:", ex)

    @classmethod
    async def get_qrcode_url(cls, tel: str) -> str:
        print("get_qrcode_url {}".format(tel))
        client = await cls.get_client_by_tel(tel)

        if client is None:
            return "No client {}".format(tel)
        if client.status == AUTHORIZED:
            return "authorized"

        client.qr_login_obj = await client.qr_login()
        cls.waiting_tasks.append(
            asyncio.create_task(cls.worker(
                WaitQRCodeAuthTask(client=client)
            ))
        )
        client.status = WAITING_QR_AUTH
        # print("\tCreated QR_URL. WAITING_QR_AUTH")
        return client.qr_login_obj.url

    @classmethod
    async def get_auth_status(cls, tel: str):
        # client = await cls.get_client_by_tel(tel)
        if await cls.get_client_by_tel(tel) is None:
            return "No client {}".format(tel)
        # print("get_auth_status for client {}: {}".format(tel, cls.clients[tel].status[1]))
        return cls.clients[tel].status[1]

    @classmethod
    async def get_dialogs(cls, tel):
        print("----------------------------------------------------------------------")
        print("get_dialogs {}".format(tel))
        ret_list = []
        client = await cls.get_client_by_tel(tel)
        dialogs = await client.get_dialogs()

        # print("dialog contents:", dialog_to_dict(dialogs[0]))
        for dialog in dialogs:
            print("dialog contents:", object_to_dict(dialog))
            # if not dialog.archived:
            client.dialogs[dialog.entity.id] = dialog
            ret_list.append({
                'id': dialog.entity.id,
                'title': dialog.entity.id if dialog.title == "" else dialog.title,
                'unread_count': dialog.unread_count,
                'username': dialog.entity.username,
            })

        # print("ret:\n", ret_list)
        return ret_list

        # return JSONResponse()
        # ret_list.append([dialog.name, dialog.entity.id])
        # async for dialog in client.iter_dialogs():
        #     # print('{:>14}: {}'.format(dialog.id, dialog.title))
        #     print("--------------------\nddd:", dialog)
        #     print("\nto_dict:", dialog.to_dict())
        #     print("\nstringify():", dialog.stringify())
        # print("ret:", cls.clients[tel].dialogs.stringify())
        # return cls.clients[tel].dialogs.

    @classmethod
    async def get_messages(cls, tel, entity):
        print("----------------------------------------------------------------------")
        print("get_messages {}, entity {}".format(tel, entity))
        client = await cls.get_client_by_tel(tel)
        client.messages = await client.get_messages(int(entity), limit=3)

        ret_messages = {}
        for mess in client.messages:
            # print("\nmessage contents dialog_to_dict:", dialog_to_dict(mess))
            # print("message contents to_dict_req:", to_dict_req(mess))
            try:
                ret_messages[mess.id] = {
                    'from_id': None if mess.from_id is None else mess.from_id.user_id,
                    'message': mess.message,
                    'out': mess.out,
                    'date': mess.date.strftime("%Y.%m.%d, %H:%M:%S"),
                }
                ret_messages[mess.id]['user_id'] = mess.peer_id.user_id \
                    if isinstance(mess.peer_id, PeerUser) else None

                ret_messages[mess.id]['channel_id'] = mess.peer_id.channel_id \
                    if isinstance(mess.peer_id, PeerChannel) else None

            except Exception as ex:
                print("\tCan't guess message: ", mess, "\nException:\n", ex)
        # print("messages to return:\n", ret_messages)
        return ret_messages
