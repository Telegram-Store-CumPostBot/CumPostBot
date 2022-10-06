from logger import get_logger


def one_run(func):
    log = get_logger(__name__)

    async def wrapper(*args, **kwargs):
        if func.runs:
            log.info('%s already is running', str(func))
            return None
        func.runs = True
        res = await func(*args, **kwargs)
        func.runs = False
        return res
    func.runs = False
    return wrapper
