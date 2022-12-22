from src.classes.IDigitalException import IDigitalException
from src.classes.IDigitalMessage import IDigitalMessage
from src.classes.IDigitalHelp import IDigitalHelp
from jose import jwt
import base64
import json


class IDigitalToken:
    def __init__(self, token: str, token_decoded: dict):
        self.payload = token_decoded['payload']
        self.header = token_decoded['header']
        self.token = token

    @staticmethod
    def getHeader(token: str | None, typ: str) -> dict:
        header = IDigitalToken.getData(token, 0)

        if header['alg'] is None or header['alg'] != 'RS256':
            message = IDigitalMessage.JWT_WITHOUT_ALG
            raise IDigitalException(400, message)

        if header['typ'] is None or header['typ'] != typ:
            message = IDigitalMessage.JWT_WITHOUT_TYP
            raise IDigitalException(400, message)

        if header['kid'] is None:
            message = IDigitalMessage.JWT_WITHOUT_KID
            raise IDigitalException(400, message)

        return header

    @staticmethod
    def verifyHeader(token: str | None, header: dict, keys):
        public_key = IDigitalToken.getPublicKeyByKid(header['kid'], header['alg'], keys)
        return jwt.decode(token, public_key, algorithms=['RS256'], options={
            "verify_aud": False,
            "verify_iss": False
        })

    @staticmethod
    def getPayload(token: str | None) -> dict:
        return IDigitalToken.getData(token, 1)

    @staticmethod
    def getSignature(token: str | None) -> dict:
        return IDigitalToken.getData(token, 2)

    @staticmethod
    def getPublicKeyByKid(kid: str | None, alg: str | None, keys) -> dict:
        public_key = None

        for value in keys['keys']:
            if value['kid'] is not None and value['alg'] is not None:
                if value['kid'] == kid and value['alg'] == alg:
                    public_key = value
                    break

        if public_key is None:
            message = IDigitalMessage.COULD_NOT_FIND_PUBLIC_KEYS
            raise IDigitalException(500, message)

        return public_key

    @staticmethod
    def getData(token: str | None, offset: int) -> dict:
        if token is not None and IDigitalHelp.is_jwt(token):
            partial = token.split('.')[offset]
            data = partial + "=" * (len(partial) % 4)
            data = base64.urlsafe_b64decode(data)
            data = json.loads(data)
            return data
        else:
            IDigitalToken.isNotJWT()

    @staticmethod
    def isNotJWT() -> None:
        message = IDigitalMessage.INVALID_JWT
        raise IDigitalException(400, message)

    @staticmethod
    def verifyIssuer(value1: str | None, value2: str | None) -> None:
        IDigitalToken.verifyAttributesOfJWT(value1, value2, IDigitalMessage.DIVERGENT_ISSUER)

    @staticmethod
    def verifyClient(value1: str | None, value2: str | None) -> None:
        IDigitalToken.verifyAttributesOfJWT(value1, value2, IDigitalMessage.DIVERGENT_CLIENT_ID)

    @staticmethod
    def verifyAudience(value1: str | None, value2: str | None) -> None:
        IDigitalToken.verifyAttributesOfJWT(value1, value2, IDigitalMessage.DIVERGENT_AUDIENCE)

    @staticmethod
    def verifyNonce(value1: str | None, value2: str | None) -> None:
        IDigitalToken.verifyAttributesOfJWT(value1, value2, IDigitalMessage.DIVERGENT_NONCE)

    @staticmethod
    def verifyAttributesOfJWT(value1: str | None, value2: str | None, message: str) -> None:
        if value1 is None or value2 is None or value1 != value2:
            raise IDigitalException(400, message)
