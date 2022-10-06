import ssl

import requests as requests
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, \
    setup_application
from cashews import cache

from database.models.api.tg_bot import DBAPITGBot
from handlers import global_router

from aiohttp import web
from aiogram import Dispatcher
from update_aiogram.client.bot import Bot

from logger import get_logger
from database.connection import connect_to_database
from settings.settings import settings

from middlewares.throttling import ThrottlingMiddleware


async def register_bot_in_db(bot: Bot):
    if not await DBAPITGBot.check_availability(bot.id):
        await DBAPITGBot.create_new(bot.id, bot.token)


def register_all_middlewares(dp: Dispatcher):
    dp.message.middleware(ThrottlingMiddleware())


def register_all_filters(dp: Dispatcher):
    print(dp.message)
    # dp.filters_factory.bind()
    pass


def register_all_handlers(dp: Dispatcher):
    dp.include_router(global_router)


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    logger.info('Connecting to database...')
    await connect_to_database()
    logger.info('Was connect to database')

    register_all_middlewares(dispatcher)
    register_all_filters(dispatcher)
    register_all_handlers(dispatcher)
    await register_bot_in_db(bot)

    certificate = open(settings.webhook_ssl_cert, 'rb')

    # set webhook url and self-signed certificate
    host = f'{settings.tg_bot_webhook_host}:{settings.tg_bot_webhook_port}'
    path = f'{settings.tg_bot_webhook_path}/{settings.tg_bot_token}'
    webhook_url = f'https://{host}{path}'
    files = {
        'url': (None, webhook_url),
        'certificate': certificate,
    }
    set_url = f'https://api.telegram.org/bot{settings.tg_bot_token}/setWebhook'
    requests.post(set_url, files=files)

    logger.debug(webhook_url)
    # await bot.set_chat_menu_button(menu_button=MenuButtonWebApp(
    #     text='Магазин',
    #     web_app=WebAppInfo(url='https://vk.com')
    # ))

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
    cache.setup("mem://", size=1000)

    logger.info("Starting bot")
    storage = MemoryStorage()
    bot = Bot(
        token=settings.tg_bot_token,
        qiwi_access_token=settings.qiwi_access_token,
        qiwi_phone_with_plus=settings.qiwi_phone,
    )
    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)

    logger.info('Сonfiguring web app')
    logger.info('Creating SSL context...')

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(
        app,
        path=f'/webhook/{settings.tg_bot_token}'
    )
    setup_application(app, dp, bot=bot)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        settings.webhook_ssl_cert,
        settings.webhook_ssl_priv
    )

    logger.info('SSL context was created')
    logger.info('Web app was configuring')

    logger.info('Running web app...')

    webapp_host = '0.0.0.0'
    webapp_port = settings.tg_bot_webhook_port

    web.run_app(app, host=webapp_host, port=webapp_port, ssl_context=context)
    # web.run_app(app, host=webapp_host, port=webapp_port)


if __name__ == '__main__':
    logger = get_logger(__name__)
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
