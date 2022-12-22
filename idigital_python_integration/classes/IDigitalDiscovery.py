class IDigitalDiscovery:
    PATHNAME: str = 'sso/oidc/.well-known/openid-configuration'

    def __init__(self, discovery: dict):
        self.issuer: str = discovery['issuer']
        self.jwks_uri: str = discovery['jwks_uri']
        self.token_endpoint: str = discovery['token_endpoint']
        self.claims_supported: tuple = discovery['claims_supported']
        self.scopes_supported: tuple = discovery['scopes_supported']
        self.end_session_endpoint: str = discovery['end_session_endpoint']
        self.claim_types_supported: tuple = discovery['claim_types_supported']
        self.grant_types_supported: tuple = discovery['grant_types_supported']
        self.authorization_endpoint: str = discovery['authorization_endpoint']
        self.subject_types_supported: tuple = discovery['subject_types_supported']
        self.userinfo_endpoint: str | None = discovery['userinfo_endpoint'] or None
        self.response_modes_supported: tuple = discovery['response_modes_supported']
        self.response_types_supported: tuple = discovery['response_types_supported']
        self.claims_parameter_supported: bool = discovery['claims_parameter_supported']
        self.request_parameter_supported: bool = discovery['request_parameter_supported']
        self.backchannel_logout_supported: bool = discovery['backchannel_logout_supported']
        self.request_uri_parameter_supported: bool = discovery['request_uri_parameter_supported']
        self.require_request_uri_registration: bool = discovery['require_request_uri_registration']
        self.code_challenge_methods_supported: tuple = discovery['code_challenge_methods_supported']
        self.dpop_signing_alg_values_supported: tuple = discovery['dpop_signing_alg_values_supported']
        self.backchannel_logout_session_supported: bool = discovery['backchannel_logout_session_supported']
        self.id_token_signing_alg_values_supported: tuple = discovery['id_token_signing_alg_values_supported']
        self.token_endpoint_auth_methods_supported: tuple = discovery['token_endpoint_auth_methods_supported']
        self.request_object_signing_alg_values_supported: tuple = discovery['request_object_signing_alg_values_supported']
        self.authorization_response_iss_parameter_supported: bool = discovery['authorization_response_iss_parameter_supported']
