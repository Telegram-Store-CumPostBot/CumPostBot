import asyncio
import time


def async_rate_limit(delay):
    def wrapper(func):
        count = [time.time()]

        async def decorator_sleep():
            while True:
                if time.time() - count[0] > delay:
                    count[0] = time.time()
                    return
                await asyncio.sleep(delay - (time.time() - count[0]))

        async def decorator(*args, **kwargs):
            await decorator_sleep()
            return await func(*args, **kwargs)

        return decorator
    return wrapper


def counter():
    def wrapper(func):
        async def wrapped(*args, **kwargs):
            wrapped.count += 1
            return await func(*args, **kwargs)

        wrapped.count = 0
        return wrapped

    return wrapper
