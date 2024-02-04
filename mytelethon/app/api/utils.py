import datetime
import secrets
import string


white_list = [
    # поля с ключами из белого списка раскрываем как вложенные объекты
    'message', 'entity', 'draft', 'photo', 'status', 'peer_id', 'from_id', 'input_entity', 'reply_to',
    'original_update', 'action', 'emoji_status', #'color', 'media', 'replies', 'entities'
]

black_list = [
    # ключи из черного списка игнорируем, как и имена полей начинающиеся с _
    'dialog',
]


def object_to_dict(obj, level: int = 0):
    result = {}
    # print("---dir: ", [el for el in dir(obj) if not el.startswith('_')])
    for key, value in vars(obj).items():
        if not (key.startswith('_') or key in black_list):
            if key in white_list:
                # print("!sub ", key)
                if hasattr(getattr(obj, key, None), '__dict__'):
                    result[key] = object_to_dict(getattr(obj, key, None), level + 1)
                else:
                    result[key] = value.__str__()
            else:
                # print("! {}key: {}={}".format('\t' * level, key, value))
                result[key] = value.strftime("%Y.%m.%d, %H:%M:%S") if isinstance(value, datetime.datetime) else value
    return result


# *******************************************


def has_to_dict(obj):
    method = getattr(obj, "to_dict", None)
    return callable(method)


def to_dict_req(obj):
    res = {}
    if has_to_dict(obj):
        for key, value in obj.to_dict().items():
            if has_to_dict(value):
                value = to_dict_req(value)
            else:
                value = str(value)
            res[key] = value
        return res
    else:
        return str(obj)

# ********************************************


letters_and_numbers = string.ascii_letters + string.digits


def get_random_secret_string(length: int) -> str:
    return "".join(
        secrets.choice(letters_and_numbers) for i in range(length)
    )
