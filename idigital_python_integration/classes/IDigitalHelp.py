from src.classes.IDigitalException import IDigitalException
from src.classes.IDigitalMessage import IDigitalMessage
import hashlib
import secrets
import base64
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
            encode = 'base64'
            code_verifier = IDigitalHelp.get_random_bytes()
            sha256 = hashlib.sha256(code_verifier.encode(encode)).hexdigest()
            pre_code_challenge = base64.urlsafe_b64encode(sha256.encode(encode)).decode(encode)
            code_challenge = pre_code_challenge.replace('+/', '-_').replace(' ', '-')
            return {
                'code_verifier': code_verifier,
                'code_challenge': code_challenge
            }
        except Exception:
            message = IDigitalMessage.COULD_NOT_GENERATE_PKCE
            raise IDigitalException(500, message)
