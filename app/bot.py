import ssl

from pyngrok import ngrok
from aiogram import Bot, Dispatcher
from aiogram.types import MenuButtonWebApp, WebAppInfo
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import start_webhook

from logger import get_logger
from database.connection import connect_to_database
from settings import settings

from handlers.base import register_base


def register_all_middlewares(dp: Dispatcher):
    # dp.setup_middleware()
    pass


def register_all_filters(dp: Dispatcher):
    # dp.filters_factory.bind()
    pass


def register_all_handlers(dp: Dispatcher):
    register_base(dp)


async def on_startup(dp: Dispatcher):
    logger.info('Connecting to database...')
    await connect_to_database()
    logger.info('Was connect to database')

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    certificate = None
    if settings.production:
        certificate = open(settings.webhook_ssl_cert, 'rb')

    url = f'https://{settings.tg_bot_webhook_host}:{settings.tg_bot_webhook_port}{settings.tg_bot_webhook_path}/{settings.tg_bot_token}'
    if not settings.production:
        ngrok.set_auth_token(settings.ngrok_token)
        http_tunnel = ngrok.connect(bind_tls=True)
        url = f'{http_tunnel.public_url}{settings.tg_bot_webhook_path}/{settings.tg_bot_token}'

    logger.debug(url)
    await dp.bot.set_webhook(
        url=url,
        certificate=certificate,
        drop_pending_updates=True,
    )
    await dp.bot.set_chat_menu_button(menu_button=MenuButtonWebApp(
        text='Магазин',
        web_app=WebAppInfo(url='https://MihailPereverza.github.io')
    ))

    logger.info('Web app was run')
    logger.info('Bot stated!')


async def on_shutdown(dp: Dispatcher):
    logger.info('Deleting telegram webhook...')
    await dp.bot.delete_webhook()
    logger.info('Telegram webhook was deleted')

    logger.info('Closing telegram storage...')
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info('Telegram storage was closed')


def main():
    logger.info("Starting bot")

    storage = RedisStorage2() if settings.bot_use_redis_for_fsm_storage else MemoryStorage()
    bot = Bot(token=settings.tg_bot_token)
    dp = Dispatcher(bot, storage=storage)

    logger.info('Сonfiguring web app')
    logger.info('Creating SSL context...')

    context = None
    if settings.production:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(settings.webhook_ssl_cert, settings.webhook_ssl_priv)

    logger.info('SSL context was created')
    logger.info('Web app was configuring')

    logger.info('Running web app...')

    webapp_host = '0.0.0.0'
    webapp_port = settings.tg_bot_webhook_port
    if not settings.production:
        webapp_host = 'localhost'
        webapp_port = 80

    start_webhook(
        dispatcher=dp,
        webhook_path=f'/webhook/{settings.tg_bot_token}',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=webapp_host,
        port=webapp_port,
        ssl_context=context
    )


if __name__ == '__main__':
    logger = get_logger(__name__)
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
