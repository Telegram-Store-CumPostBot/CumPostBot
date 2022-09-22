import configparser

from pydantic import BaseSettings


class Settings(BaseSettings):
    production: bool = False
    bot_use_redis_for_fsm_storage: bool = False

    pg_user: str
    pg_pass: str
    pg_host: str
    pg_port: str
    pg_db_name: str

    tg_bot_token: str
    tg_bot_webhook_host: str
    tg_bot_webhook_port: int
    tg_bot_webhook_path: str

    qiwi_access_token: str
    qiwi_public_p2p_token: str
    qiwi_secret_p2p_token: str
    qiwi_phone: str

    webhook_ssl_cert: str
    webhook_ssl_priv: str

    logging_file_name: str = 'app.log'

    ngrok_token: str


settings = Settings(
    _env_file='./.env',
    _env_file_encoding='utf-8'
)


config = configparser.ConfigParser()
config.read('./app/settings/project.ini')
