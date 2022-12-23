class IDigitalConfig:
    def __init__(self, configs: dict):
        self.issuer: str = configs['issuer']
        self.client_id: str = configs['client_id']
        self.redirect_uri: str = configs['redirect_uri']
        self.application_host: str = configs['application_host']

        # Adding Default options for oauth2 authorization code flow
        self.response_type = configs.get('response_type', 'code')
        self.application_type = configs.get('application_type', 'web')
        self.grant_type = configs.get('grant_type', 'authorization_code')
        self.scopes = configs.get('scopes', ['openid', 'profile', 'email'])
        self.code_challenge_method = configs.get('code_challenge_method', 'S256')
        self.token_endpoint_auth_method = configs.get('token_endpoint_auth_method', 'none')
        self.post_logout_redirect_uri = configs.get('post_logout_redirect_uri', self.application_host)
