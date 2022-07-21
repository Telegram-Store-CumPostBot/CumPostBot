import ssl

import handlers.base

from aiohttp import web
from pyngrok import ngrok
from aiogram import Bot, Dispatcher
from aiogram.types import MenuButtonWebApp, WebAppInfo
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from logger import get_logger
from database.connection import connect_to_database
from settings import settings

from middlewares.throttling import ThrottlingMiddleware


def register_all_middlewares(dp: Dispatcher):
    dp.message.middleware(ThrottlingMiddleware())


def register_all_filters(dp: Dispatcher):
    # dp.filters_factory.bind()
    pass


def register_all_handlers(dp: Dispatcher):
    dp.include_router(handlers.base.router)


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    logger.info('Connecting to database...')
    await connect_to_database()
    logger.info('Was connect to database')

    register_all_middlewares(dispatcher)
    register_all_filters(dispatcher)
    register_all_handlers(dispatcher)

    certificate = None
    if settings.production:
        certificate = open(settings.webhook_ssl_cert, 'rb')

    url = f'https://{settings.tg_bot_webhook_host}:{settings.tg_bot_webhook_port}{settings.tg_bot_webhook_path}/{settings.tg_bot_token}'
    if not settings.production:
        logger.info('Connecting to ngrok...')
        ngrok.set_auth_token(settings.ngrok_token)
        http_tunnel = ngrok.connect(bind_tls=True)
        logger.info('Was connect to ngrok')
        url = f'{http_tunnel.public_url}{settings.tg_bot_webhook_path}/{settings.tg_bot_token}'

    logger.debug(url)
    await bot.set_webhook(
        url=url,
        certificate=certificate,
        drop_pending_updates=True,
    )
    await bot.set_chat_menu_button(menu_button=MenuButtonWebApp(
        text='Магазин',
        web_app=WebAppInfo(url='https://vk.com')
    ))

    logger.info('Web app was run')
    logger.info('Bot stated!')


async def on_shutdown(dp: Dispatcher, bot: Bot):
    logger.info('Deleting telegram webhook...')
    await bot.delete_webhook()
    logger.info('Telegram webhook was deleted')

    logger.info('Closing telegram storage...')
    await dp.storage.close()
    logger.info('Telegram storage was closed')


def main():
    logger.info("Starting bot")
    storage = MemoryStorage()
    bot = Bot(token=settings.tg_bot_token)
    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)

    logger.info('Сonfiguring web app')
    logger.info('Creating SSL context...')

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f'/webhook/{settings.tg_bot_token}')
    setup_application(app, dp, bot=bot)

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

    web.run_app(app, host=webapp_host, port=webapp_port, ssl_context=context)


if __name__ == '__main__':
    logger = get_logger(__name__)
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
