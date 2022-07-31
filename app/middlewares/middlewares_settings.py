from settings.settings import config


class ThrottlingSettings:
    DEFAULT_THROTTLE_TIME = 3
    DEFAULT_THROTTLE_KEY = 'default'
    DEFAULT_FLAGS = {
        config['FlagsNames']['throttling_key']: DEFAULT_THROTTLE_KEY,
        config['FlagsNames']['throttle_time']: DEFAULT_THROTTLE_TIME,
    }
    MAX_CACHE_SIZE = 10_000
