from src.classes.IDigitalToken import IDigitalToken
from src.classes.IDigitalHelp import IDigitalHelp


class IDigitalAccessToken(IDigitalToken):

    @staticmethod
    def verify(token: str | None, keys, options):
        if token is not None and IDigitalHelp.is_jwt(token):
            header = IDigitalAccessToken.getHeader(token, 'at+jwt')
            jwt_decoded = IDigitalAccessToken.verifyHeader(token, header, keys)
            IDigitalAccessToken.verifyIssuer(jwt_decoded['payload']['iss'], options['issuer'])
            IDigitalAccessToken.verifyClient(jwt_decoded['payload']['client_id'], options['client_id'])
            IDigitalAccessToken.verifyAudience(jwt_decoded['payload']['aud'], options['application_host'])

            return IDigitalAccessToken(token, {
                'payload': jwt_decoded['payload'],
                'header': header
            })

        IDigitalAccessToken.isNotJWT()
