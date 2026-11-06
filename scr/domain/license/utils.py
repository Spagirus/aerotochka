"""утилиты для лицензии"""

import uuid
from datetime import date

from dateutil.relativedelta import relativedelta


def get_valid_until() -> date:
    valid = date.today() + relativedelta(years=1)
    return valid


def get_key() -> str:
    id_hex = uuid.uuid4().hex
    return f"drl_{id_hex}"
