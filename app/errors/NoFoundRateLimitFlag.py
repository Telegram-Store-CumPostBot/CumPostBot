class NoFoundRateLimitFlagError(Exception):
    def __str__(self):
        return (
            '\nNo found rate limit flag in handler.'
            '\nUse @flags.rate_limit({throttling_key: %key(str), throttling_time: %time(int)})'
        )
