class IDigitalConfig:
    def __init__(self, configs: dict):
        self.issuer: str = configs['issuer']
        self.client_id: str = configs['client_id']
        self.redirect_uri: str = configs['redirect_uri']
        self.application_host: str = configs['application_host']

        # Adding Default options for oauth2 authorization code flow
        self.response_type = configs['response_type'] if configs['response_type'] else 'code'
        self.scopes = configs['scopes'] if configs['scopes'] else ['openid', 'profile', 'email']
        self.grant_type = configs['grant_type'] if configs['grant_type'] else 'authorization_code'
        self.application_type = configs['application_type'] if configs['application_type'] else 'web'
        self.code_challenge_method = configs['code_challenge_method'] if configs['code_challenge_method'] else 'S256'
        self.token_endpoint_auth_method = configs['token_endpoint_auth_method'] if configs['token_endpoint_auth_method'] else 'none'
        self.post_logout_redirect_uri = configs['post_logout_redirect_uri'] if configs['post_logout_redirect_uri'] else self.issuer
