class IDigitalConfig:
    def __init__(self, configs: dict):
        self.issuer: str = configs['issuer']
        self.client_id: str = configs['client_id']
        self.redirect_uri: str = configs['redirect_uri']
        self.application_host: str = configs['application_host']

        # Adding Default options for oauth2 authorization code flow
        self.response_type = configs['response_type'] or 'code'
        self.application_type = configs['application_type'] or 'web'
        self.grant_type = configs['grant_type'] or 'authorization_code'
        self.scopes = configs['scopes'] or ['openid', 'profile', 'email']
        self.code_challenge_method = configs['code_challenge_method'] or 'S256'
        self.token_endpoint_auth_method = configs['token_endpoint_auth_method'] or 'none'
        self.post_logout_redirect_uri = configs['post_logout_redirect_uri'] or self.issuer
