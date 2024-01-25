import re
from dataclasses import dataclass
from collections import namedtuple
from datetime import datetime


# @dataclass
# class PeerUser:
#     user_id: int
#     out: bool
#
#
# @dataclass
# class User:
#     id: int
#     contact: bool
#     bot: bool
#     first_name: str
#     last_name: str
#     username: str
#
#
# @dataclass
# class MessageService:
#     id: int
#     peer_id: PeerUser
#
#
# @dataclass
# class Dialog:
#     name: str
#     message: MessageService
#     entity: User

text = "Dialog(name='name contact', out=False, message=Message(id=2333, peer_id=PeerUser(user_id=272992901)))"
txt = """Dialog(
        name='namecontact1',
        date=datetime.datetime(2021, 4, 9, 15, 13, 41, tzinfo=datetime.timezone.utc),
        message=MessageService(
                id=47,
                peer_id=PeerUser(
                        user_id=1777374180
                ),
                date=datetime.datetime(2021, 4, 9, 15, 13, 41, tzinfo=datetime.timezone.utc),
                action=MessageActionContactSignUp(
                ),
                out=False,
                mentioned=False,
                media_unread=False,
                silent=False,
                post=False,
                legacy=False,
                from_id=None,
                reply_to=None,
                ttl_period=None
        ),
        entity=User(
                id=1777374180,
                is_self=False,
                contact=True,
                mutual_contact=True,
                deleted=False,
                bot=False,
                bot_chat_history=False,
                bot_nochats=False,
                verified=False,
                restricted=False,
                min=False,
                bot_inline_geo=False,
                support=False,
                scam=False,
                apply_min_photo=True,
                fake=False,
                bot_attach_menu=False,
                premium=False,
                attach_menu_enabled=False,
                bot_can_edit=False,
                close_friend=False,
                stories_hidden=False,
                stories_unavailable=True,
                access_hash=7277724265657408838,
                first_name='namecontact1',
                last_name=None,
                username=None,
                phone='79517253016',
                photo=UserProfilePhoto(
                        photo_id=5371057209141738694,
                        dc_id=2,
                        has_video=False,
                        personal=False,
                        stripped_thumb=b'\x01\x08\x08\xd1(q\xbb<b\x8a(\xa95N\xe7'
                ),
                status=UserStatusOffline(
                        was_online=datetime.datetime(2024, 1, 12, 20, 15, 46, tzinfo=datetime.timezone.utc)
                ),
                bot_info_version=None,
                restriction_reason=[
                ],
                bot_inline_placeholder=None,
                lang_code=None,
                emoji_status=None,
                usernames=[
                ],
                stories_max_id=None,
                color=None,
                profile_color=None
        )
)
"""


MessageActionContactSignUp = namedtuple('MessageActionContactSignUp', ())

PeerUser = namedtuple('PeerUser', ('user_id', ))

# PeerChannel = namedtuple('PeerChannel', ('channel_id', ))
#
# Message = namedtuple('Message', ('id', 'peer_id'))

MessageService = namedtuple('MessageService', ('id', 'peer_id'))

User = namedtuple('User', ('id', 'contact', 'bot', 'first_name', 'last_name', 'username'))

Dialog = namedtuple('Dialog', ('name', 'message', 'entity'))

sstr = "id=47, out=False"
print("! ", MessageService(sstr))

import datetime


# dg1 = eval(text)
# , message='ttt'
# message=Message(id=2333, peer_id=PeerUser(user_id=272992901))
# print("user:", dg1)
# txt = re.sub(r"b'.+'", "''", txt)
# date = datetime.datetime(2021, 4, 9, 15, 13, 41, tzinfo=datetime.timezone.utc)
# print("dialog:", eval(txt))
