from idigital_python_integration.classes.IDigitalException import IDigitalException
from idigital_python_integration.classes.IDigitalMessage import IDigitalMessage
from typing import Any


class IDigitalSession:
    NAME: str = 'idigital'

    @staticmethod
    def guarantees_already_exists(session: dict) -> None:
        if session is None:
            message = IDigitalMessage.REQUIRED_SESSION
            raise IDigitalException(400, message)

        session.setdefault(IDigitalSession.NAME, {})

    @staticmethod
    def flush(session: dict) -> None:
        IDigitalSession.guarantees_already_exists(session)
        session.setdefault(IDigitalSession.NAME, {})
        del(session[IDigitalSession.NAME])

    @staticmethod
    def get(session: dict, key: str, default=None) -> Any:
        IDigitalSession.guarantees_already_exists(session)
        dictonary = session.get(IDigitalSession.NAME, {})
        value = dictonary.get(key, None)

        if value is None and not callable(default):
            IDigitalSession.put(session, key, default)
            value = default
        elif value is None and callable(default):
            value = default()
            IDigitalSession.put(session, key, value)

        return value

    @staticmethod
    def delete(session: dict, key: str) -> None:
        IDigitalSession.guarantees_already_exists(session)
        session.get(IDigitalSession.NAME, {}).pop(key, None)

    @staticmethod
    def put(session: dict, key: str, value) -> None:
        IDigitalSession.guarantees_already_exists(session)
        session.get(IDigitalSession.NAME, {}).update({key: value})

    @staticmethod
    def pull(session: dict, key: str, default=None) -> Any:
        IDigitalSession.guarantees_already_exists(session)
        value = IDigitalSession.get(session, key, default)
        IDigitalSession.delete(session, key)
        return value
