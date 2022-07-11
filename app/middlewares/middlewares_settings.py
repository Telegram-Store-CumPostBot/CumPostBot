class ThrottlingSettings:
    DEFAULT_THROTTLE_TIME = 3
    DEFAULT_THROTTLE_KEY = 'default'
    DEFAULT_FLAGS = {'throttling_key': DEFAULT_THROTTLE_KEY, 'throttle_time': DEFAULT_THROTTLE_TIME}
    MAX_CACHE_SIZE = 10_000
