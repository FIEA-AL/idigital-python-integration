from src.classes.IDigitalDiscovery import IDigitalDiscovery
from src.classes.IDigitalException import IDigitalException
from src.classes.IDigitalMessage import IDigitalMessage
from typing import Any
import requests


class IDigitalHttp:
    __WWW_FORM_TYPE: str = 'application/x-www-form-urlencoded'
    __JSON_TYPE: str = 'application/json'

    @staticmethod
    def get_discovery(url: str) -> IDigitalDiscovery:
        return IDigitalDiscovery(IDigitalHttp.get(url))

    @staticmethod
    def get_jwks(url: str) -> Any:
        return IDigitalHttp.get(url)

    @staticmethod
    def get_tokens(url: str, body: dict) -> Any:
        return IDigitalHttp.post(url, body)

    @staticmethod
    def get(url: str) -> Any:
        try:
            return requests.get(url, headers={
                'Content-Type': IDigitalHttp.__JSON_TYPE,
            })
        except Exception:
            message = IDigitalMessage.HTTP_ERROR
            raise IDigitalException(500, message)

    @staticmethod
    def post(url: str, body: dict) -> Any:
        try:
            return requests.post(url, data=body, headers={
                'Content-Type': IDigitalHttp.__WWW_FORM_TYPE
            })
        except Exception:
            message = IDigitalMessage.HTTP_ERROR
            raise IDigitalException(500, message)
