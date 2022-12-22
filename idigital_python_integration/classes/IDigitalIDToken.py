from src.classes.IDigitalToken import IDigitalToken
from src.classes.IDigitalHelp import IDigitalHelp


class IDigitalIDToken(IDigitalToken):

    @staticmethod
    def verify(token: str | None, nonce: str | None, keys, options):
        if token is not None and nonce is not None and IDigitalHelp.is_jwt(token):
            header = IDigitalIDToken.getHeader(token, 'JWT')
            jwt_decoded = IDigitalIDToken.verifyHeader(token, header, keys)
            IDigitalIDToken.verifyNonce(jwt_decoded['payload']['nonce'], nonce)
            IDigitalIDToken.verifyIssuer(jwt_decoded['payload']['iss'], options['issuer'])
            IDigitalIDToken.verifyAudience(jwt_decoded['payload']['aud'], options['client_id'])

            return IDigitalIDToken(token, {
                'payload': jwt_decoded['payload'],
                'header': header
            })

        IDigitalIDToken.isNotJWT()
