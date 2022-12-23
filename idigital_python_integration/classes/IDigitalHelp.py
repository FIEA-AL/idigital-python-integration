from idigital_python_integration.classes.IDigitalException import IDigitalException
from idigital_python_integration.classes.IDigitalMessage import IDigitalMessage
import secrets
import pkce
import re


class IDigitalHelp:
    @staticmethod
    def get_parameterized_url(url: str, params: list) -> str:
        def query_element(item): return f"{item[0]}={item[1]}"
        return f"{url}?{'&'.join(map(query_element, params))}"

    @staticmethod
    def is_jwt(value: str) -> bool:
        regex = re.compile("^([a-zA-Z0-9_=]+)\.([a-zA-Z0-9_=]+)\.([a-zA-Z0-9_\-+\/=]*)")
        return type(value) is str and bool(regex.match(value))

    @staticmethod
    def get_random_bytes(length: int = 32) -> str:
        try:
            return secrets.token_urlsafe(length)
        except Exception:
            message = IDigitalMessage.COULD_NOT_GENERATE_BYTES
            raise IDigitalException(500, message)

    @staticmethod
    def get_pkce_keys_pair() -> dict:
        try:
            code_verifier = pkce.generate_code_verifier(length=128)
            code_challenge = pkce.get_code_challenge(code_verifier)
            return {
                'code_verifier': code_verifier,
                'code_challenge': code_challenge
            }
        except Exception:
            message = IDigitalMessage.COULD_NOT_GENERATE_PKCE
            raise IDigitalException(500, message)
