"""утилиты для лицензии"""

import uuid
from datetime import date, datetime
from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta


def get_valid_until() -> date:
    """получение срока лицензии +1 год"""
    valid = (datetime.now(ZoneInfo("Europe/Moscow")) + relativedelta(years=1)).date()
    return valid


def get_key() -> str:
    """получение ключа формата drl_uuid4 hex"""
    id_hex = uuid.uuid4().hex
    return f"drl_{id_hex}"


def get_msk_time() -> datetime:
    """получение московского времени"""
    return datetime.now(ZoneInfo("Europe/Moscow"))
