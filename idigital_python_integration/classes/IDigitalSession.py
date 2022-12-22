from src.classes.IDigitalException import IDigitalException
from src.classes.IDigitalMessage import IDigitalMessage
from typing import Any


class IDigitalSession:
    NAME: str = 'idigital'

    @staticmethod
    def guarantees_already_exists(session: dict) -> None:
        if session is None:
            message = IDigitalMessage.REQUIRED_SESSION
            raise IDigitalException(400, message)

        if session[IDigitalSession.NAME] is None:
            session[IDigitalSession.NAME] = {}

    @staticmethod
    def flush(session: dict) -> None:
        IDigitalSession.guarantees_already_exists(session)
        del (session[IDigitalSession.NAME])

    @staticmethod
    def get(session: dict, key: str, default=None) -> Any:
        IDigitalSession.guarantees_already_exists(session)
        value = session[IDigitalSession.NAME][key]

        if value is None and not callable(default):
            value = default
        elif value is None and callable(default):
            value = default()

        return value

    @staticmethod
    def delete(session: dict, key: str) -> None:
        IDigitalSession.guarantees_already_exists(session)
        del (session[IDigitalSession.NAME][key])

    @staticmethod
    def put(session: dict, key: str, value) -> Any:
        IDigitalSession.guarantees_already_exists(session)
        session[IDigitalSession.NAME][key] = value
        return IDigitalSession.get(session, key)

    @staticmethod
    def pull(session: dict, key: str, default=None) -> Any:
        IDigitalSession.guarantees_already_exists(session)
        value = IDigitalSession.get(session, key, default)
        IDigitalSession.delete(session, key)
        return value
