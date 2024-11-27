from rest_framework.throttling import ScopedRateThrottle


class ScopedSettingThrottle(ScopedRateThrottle):
    DEFAULT_AUTH = "5/min"
    DEFAULT_PUBLIC = "120/min"
