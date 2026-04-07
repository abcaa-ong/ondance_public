from rest_framework.throttling import AnonRateThrottle


class RegisterThrottle(AnonRateThrottle):
    scope = 'register'


class TokenThrottle(AnonRateThrottle):
    scope = 'token'


class SocialAuthThrottle(AnonRateThrottle):
    scope = 'social_auth'
