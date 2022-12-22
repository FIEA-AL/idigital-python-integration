from src.classes.IDigitalAccessToken import IDigitalAccessToken
from src.classes.IDigitalDiscovery import IDigitalDiscovery
from src.classes.IDigitalException import IDigitalException
from src.classes.IDigitalIDToken import IDigitalIDToken
from src.classes.IDigitalMessage import IDigitalMessage
from src.classes.IDigitalSession import IDigitalSession
from src.classes.IDigitalConfig import IDigitalConfig
from src.classes.IDigitalHelp import IDigitalHelp
from src.classes.IDigitalHttp import IDigitalHttp
from typing import Any, Callable


class IDigital:
    def __init__(self, configs):
        self.configs = IDigitalConfig(configs)
        self.discovery = None
        self.jwks = None

    @staticmethod
    def create(configs):
        instance = IDigital(configs)
        instance.prepare()
        return instance

    def prepare(self):
        self.discovery = self.getDiscovery()
        self.jwks = self.getJwks()

    def authorize(self, session: dict) -> str:
        authorization_endpoint = self.discovery.authorization_endpoint
        pkce_keys_pair = IDigitalHelp.get_pkce_keys_pair()
        nonce = IDigitalHelp.get_random_bytes()
        state = IDigitalHelp.get_random_bytes()

        # Update session object with provider response
        IDigitalSession.put(session, 'code_challenge', pkce_keys_pair['code_challenge'])
        IDigitalSession.put(session, 'code_verifier', pkce_keys_pair['code_verifier'])
        IDigitalSession.put(session, 'nonce', nonce)
        IDigitalSession.put(session, 'state', state)

        return IDigitalHelp.get_parameterized_url(authorization_endpoint, [
            ['code_challenge_method', self.configs.code_challenge_method],
            ['code_challenge', pkce_keys_pair['code_challenge']],
            ['response_type', self.configs.response_type],
            ['redirect_uri', self.configs.redirect_uri],
            ['resource', self.configs.application_host],
            ['scope', '+'.join(self.configs.scopes)],
            ['client_id', self.configs.client_id],
            ['nonce', nonce],
            ['state', state]
        ])

    def callback(self, code: str, issuer: str, state: str, session: dict) -> dict:
        if issuer != self.configs.issuer:
            message = IDigitalMessage.DIVERGENT_ISSUER
            raise IDigitalException(400, message)

        if state != IDigitalSession.get(session, 'state'):
            message = IDigitalMessage.DIVERGENT_STATE
            raise IDigitalException(400, message)

        tokens = self.getTokens(code, session)
        nonce = IDigitalSession.get(session, 'nonce')
        id_token = IDigitalIDToken.verify(tokens['id_token'], nonce, self.jwks, self.configs)
        access_token = IDigitalAccessToken.verify(tokens['access_token'], self.jwks, self.configs)

        # Update session object with provider response
        IDigitalSession.put(session, 'access_token', tokens['access_token'])
        IDigitalSession.put(session, 'id_token', tokens['id_token'])
        IDigitalSession.put(session, 'code', code)
        return {
            'id_token': id_token,
            'access_token': access_token
        }

    def is_authenticated(self, session: dict) -> dict:
        try:
            nonce = IDigitalSession.get(session, 'nonce')
            id_token = IDigitalSession.get(session, 'id_token')
            access_token = IDigitalSession.get(session, 'access_token')
            return {
                'status': True,
                'id_token': IDigitalIDToken.verify(id_token, nonce, self.jwks, self.configs),
                'access_token': IDigitalAccessToken.verify(access_token, self.jwks, self.configs)
            }
        except Exception:
            return {
                'status': False,
                'id_token': None,
                'access_token': None
            }

    def logout(self, session: dict, after_session_destroy_fn: Callable) -> str:
        if self.is_authenticated(session)['status']:
            url = IDigitalHelp.get_parameterized_url(self.discovery.end_session_endpoint, [
                ['post_logout_redirect_uri', self.configs.post_logout_redirect_uri],
                ['client_id', self.configs.client_id]
            ])

            # Destroy IDigital object
            IDigitalSession.flush(session)

            # Run function after session destroy
            if callable(after_session_destroy_fn):
                after_session_destroy_fn()

            return url

    def getTokens(self, code: str, session: Any | None) -> dict:
        token_endpoint = self.discovery.token_endpoint
        return IDigitalHttp.get_tokens(token_endpoint, {
            'code_challenge_method': self.configs.code_challenge_method,
            'code_challenge': IDigitalSession.get(session, 'code_challenge'),
            'code_verifier': IDigitalSession.get(session, 'code_verifier'),
            'nonce': IDigitalSession.get(session, 'nonce'),
            'redirect_uri': self.configs.redirect_uri,
            'resource': self.configs.application_host,
            'grant_type': self.configs.grant_type,
            'client_id': self.configs.client_id,
            'code': code
        })

    def getDiscovery(self):
        issuer = self.configs.issuer
        pathname = IDigitalDiscovery.PATHNAME
        url = '/'.join([issuer, pathname])
        return IDigitalHttp.get_discovery(url)

    def getJwks(self):
        url = self.discovery.jwks_uri
        return IDigitalHttp.get_jwks(url)
