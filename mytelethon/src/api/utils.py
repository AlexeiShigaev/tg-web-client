import secrets
import string
from functools import lru_cache
from typing import Any, Dict

import telethon.tl.custom


# def has_to_dict(obj):
#     method = getattr(obj, "to_dict", None)
#     # print("------obj: {}\n------has to_dict(): {}".format(obj.__class__, method))
#     return callable(method)


# узлы полей с именами из белого списка раскрываем как вложенные
white_list = ['message', 'entity', 'draft', 'photo', 'status', 'peer_id', 'input_entity']
# узлы из черного списка игнорируем, как и имена полей начинающиеся с _
black_list = ['dialog', ]


def dialog_to_dict(obj, level: int = 0):
    result = {}
    # print("---dir: ", [el for el in dir(obj) if not el.startswith('_')])
    for key, value in vars(obj).items():
        if not (key.startswith('_') or key in black_list):
            if key not in white_list:
                # print("! {}key: {}={}".format('\t' * level, key, value))
                result[key] = value
            else:
                # print("!sub ", key)
                if not hasattr(getattr(obj, key, None), '__dict__'):
                    result[key] = value.__str__()
                else:
                    result[key] = dialog_to_dict(getattr(obj, key, None), level + 1)
    return result
    # for key, value in obj.items():
    #     #     print("dialog:", dialog)
    #     print("-------\ndialog: key: {},\tvalue: {}".format(key, value))


# def to_dict_req(obj):
#     res = {}
#     if has_to_dict(obj):
#         for key, value in obj.to_dict().items():
#             if has_to_dict(value):
#                 value = to_dict_req(value)
#             else:
#                 value = str(value)
#             res[key] = value
#             print("\t--------par key: {}, value: {}".format(key, value))
#         return res
#     else:
#         return str(obj)

# def get_elem(obj: Any, elem: str) -> Any:
#     return getattr(obj, elem, None)
#
#
# def dialog_to_dict(obj):
#     if not obj.__class__
#     return {
#         'name': get_elem(obj, 'name'),
#         'date': get_elem(obj, 'date'),
#         'message': {
#             'id': get_elem(obj.message, 'id') if get_elem(obj, 'message') else None,
#             'peer_user_id': get_elem(obj.message, 'peer_user_id') if get_elem(obj, 'message') else None,
#             'message': get_elem(obj.message, 'message') if get_elem(obj, 'message') else None,
#             'out': get_elem(obj.message, 'out') if get_elem(obj, 'message') else None,
#             'from_id': obj.message.from_id.user.id,
#         }
#     }


letters_and_numbers = string.ascii_letters + string.digits


def get_random_secret_string(length: int) -> str:
    return "".join(
        secrets.choice(letters_and_numbers) for i in range(length)
    )

