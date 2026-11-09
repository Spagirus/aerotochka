"""Кастомные ошибки 404 и 409"""

from fastapi import HTTPException


class MainError(HTTPException):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class NotFound404Error(MainError):
    """бъекта с таким id нет — и в пути, и в теле запроса
        (например, drone_id у запчасти)"""


class Conflict409Error(MainError):
    """запрос корректный,но нарушает бизнес-правило
            или уникальность"""
