from errors.ValidationError import ValidationError
from logger import get_logger
from settings.digit_constants import BASE_LEN_ID


def transform_tg_id(tg_id: int) -> int:
    log = get_logger(__name__)
    if len(str(tg_id)) > BASE_LEN_ID:
        msg = f'find tg_id={tg_id} with length > {BASE_LEN_ID}'
        log.error(msg)
        raise ValidationError(msg)

    return int(str(tg_id) + '0' * (BASE_LEN_ID - len(str(tg_id))))
