from idigital_python_integration.classes.IDigitalDiscovery import IDigitalDiscovery
from idigital_python_integration.classes.IDigitalException import IDigitalException
from idigital_python_integration.classes.IDigitalMessage import IDigitalMessage
from typing import Any
import requests


class IDigitalHttp:
    __WWW_FORM_TYPE: str = 'application/x-www-form-urlencoded'
    __JSON_TYPE: str = 'application/json'

    @staticmethod
    def get_discovery(url: str) -> IDigitalDiscovery:
        response = IDigitalHttp.get(url)

        if 'error' in response:
            message = IDigitalMessage.COULD_NOT_GET_DISCOVERY
            raise IDigitalException(500, message)

        return IDigitalDiscovery(response)

    @staticmethod
    def get_jwks(url: str) -> Any:
        response = IDigitalHttp.get(url)

        if 'error' in response:
            message = IDigitalMessage.COULD_NOT_GET_JWKS
            raise IDigitalException(500, message)

        return response

    @staticmethod
    def get_tokens(url: str, body: dict) -> Any:
        response = IDigitalHttp.post(url, body)

        if 'error' in response:
            message = IDigitalMessage.COULD_NOT_GET_TOKENS
            raise IDigitalException(500, message)

        return response

    @staticmethod
    def get(url: str) -> Any:
        try:
            return requests.get(url, headers={
                'Content-Type': IDigitalHttp.__JSON_TYPE,
            }).json()
        except Exception:
            message = IDigitalMessage.HTTP_ERROR
            raise IDigitalException(500, message)

    @staticmethod
    def post(url: str, body: dict) -> Any:
        try:
            return requests.post(url, data=body, headers={
                'Content-Type': IDigitalHttp.__WWW_FORM_TYPE
            }).json()
        except Exception:
            message = IDigitalMessage.HTTP_ERROR
            raise IDigitalException(500, message)
