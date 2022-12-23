from idigital_python_integration.classes.IDigitalConfig import IDigitalConfig
from idigital_python_integration.classes.IDigitalToken import IDigitalToken
from idigital_python_integration.classes.IDigitalHelp import IDigitalHelp


class IDigitalAccessToken(IDigitalToken):
    @staticmethod
    def verify(token: str | None, keys, options: IDigitalConfig):
        if token is not None and IDigitalHelp.is_jwt(token):
            header = IDigitalAccessToken.getHeader(token, 'at+jwt')
            payload = IDigitalAccessToken.verifyHeader(token, None, header, keys)
            IDigitalAccessToken.verifyAudience(payload['aud'], options.application_host)
            IDigitalAccessToken.verifyClient(payload['client_id'], options.client_id)
            IDigitalAccessToken.verifyIssuer(payload['iss'], options.issuer)

            return IDigitalAccessToken(token, {
                'payload': payload,
                'header': header
            })

        IDigitalAccessToken.isNotJWT()
