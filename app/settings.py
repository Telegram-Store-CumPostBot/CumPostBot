from pydantic import BaseSettings


class Settings(BaseSettings):
    production: bool = False

    pg_user: str
    pg_pass: str
    pg_host: str
    pg_port: str
    pg_db_name: str

    tg_bot_token: str
    tg_bot_webhook_host: str
    tg_bot_webhook_port: int
    tg_bot_webhook_path: str

    webhook_ssl_cert: str
    webhook_ssl_priv: str

    logging_file_name: str = 'app.log'

    bot_use_redis_for_fsm_storage: bool = False

    ngrok_token: str


settings = Settings(
    _env_file='./.env',
    _env_file_encoding='utf-8'
)
