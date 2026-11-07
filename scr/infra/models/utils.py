"""утилиты для лицензии"""

import uuid
from datetime import date

from dateutil.relativedelta import relativedelta


def get_valid_until() -> date:
    """получение срока лицензии +1 год"""
    valid = date.today() + relativedelta(years=1)
    return valid


def get_key() -> str:
    """получение ключа формата drl_uuid4 hex"""
    id_hex = uuid.uuid4().hex
    return f"drl_{id_hex}"
