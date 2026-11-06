"""Модуль всех справочных значений Enum"""


from enum import StrEnum


class FlightRank(StrEnum):
    ROOKIE = "Новичок"
    PILOT = "Пилот"
    PRO = "Профи"
    ACE = "Ac"

    @property
    def rank(self):
        ranks = {
            FlightRank.ROOKIE: 1,
            FlightRank.PILOT: 2,
            FlightRank.PRO: 3,
            FlightRank.ACE: 4,
        }
        return ranks[self]


class DronePurpose(StrEnum):
    toy = "игрушечный"
    camera = "для фото- и видеосъёмки"
    fpv = "гоночный, с видом от первого лица"
    agro = "сельскохозяйственный"
    cargo = "грузовой"
    inspection = "для осмотра объектов: ЛЭП, трубы, крыши"


class DroneStatus(StrEnum):
    in_stock = "на складе, можно купить"
    sold = "продан, у дрона есть владелец"
    withdrawn = "снят с продажи, купить нельзя"


class LicenseStatus(StrEnum):
    active = "Действует"
    suspended = "временно приостановлена, может снова стать активной"
    revoked = "отозвана окончательно, восстановить нельзя"
    expired = "истёк срок действия"
