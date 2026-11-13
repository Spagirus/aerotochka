"""модуль всех справочных значений Enum"""


from enum import StrEnum


class FlightRank(StrEnum):
    """значения летных рангов"""
    ROOKIE = "ROOKIE"
    PILOT = "PILOT"
    PRO = "PRO"
    ACE = "ACE"

    @property
    def rank(self):
        """функция для выполнения операций над рангами(по типу сравнения там и т.д)"""
        ranks = {
            FlightRank.ROOKIE: 1,
            FlightRank.PILOT: 2,
            FlightRank.PRO: 3,
            FlightRank.ACE: 4,
        }
        return ranks[self]


class DronePurpose(StrEnum):
    """значения Назначения для дронов и запчастей"""
    TOY = "toy"
    CAMERA = "camera"
    FPV = "fpv"
    AGRO = "argo"
    CARGO = "cargo"
    INSPECTION = "inspection"


class DroneStatus(StrEnum):
    """Статусы дронов"""
    IN_STOCK = "in_stock"
    SOLD = "sold"
    WITHDRAWN = "withdrawn"


class LicenseStatus(StrEnum):
    """Статусы лицензий"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    EXPIRED = "expired"
