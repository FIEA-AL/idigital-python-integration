from idigital_python_integration.classes.IDigitalConfig import IDigitalConfig
from idigital_python_integration.classes.IDigitalToken import IDigitalToken
from idigital_python_integration.classes.IDigitalHelp import IDigitalHelp


class IDigitalIDToken(IDigitalToken):
    @staticmethod
    def verify(token: str | None, access_token: str | None, nonce: str | None, keys, options: IDigitalConfig):
        if token is not None and nonce is not None and IDigitalHelp.is_jwt(token):
            header = IDigitalIDToken.getHeader(token, 'JWT')
            payload = IDigitalIDToken.verifyHeader(token, access_token, header, keys)
            IDigitalIDToken.verifyAudience(payload['aud'], options.client_id)
            IDigitalIDToken.verifyIssuer(payload['iss'], options.issuer)
            IDigitalIDToken.verifyNonce(payload['nonce'], nonce)

            return IDigitalIDToken(token, {
                'payload': payload,
                'header': header
            })

        IDigitalIDToken.isNotJWT()
