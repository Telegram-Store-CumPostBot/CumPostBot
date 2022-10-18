import configparser

from pydantic import BaseSettings


def calculate_qiwi_amount(amount: float) -> float:
    return max(amount - (amount // 100 + 1), 0)


class Settings(BaseSettings):
    pg_user: str
    pg_pass: str
    pg_host: str
    pg_port: str
    pg_db_name: str

    tg_bot_token: str
    tg_bot_webhook_host: str
    tg_bot_webhook_port: int
    tg_bot_webhook_path: str

    qiwi_phone: str
    qiwi_access_token: str

    webhook_ssl_cert: str
    webhook_ssl_priv: str

    logging_file_name: str = 'app.log'


settings = Settings(
    _env_file='./.env',
    _env_file_encoding='utf-8'
)


config = configparser.ConfigParser()
config.read('./app/settings/project.ini')
