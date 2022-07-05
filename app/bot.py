import asyncio
import ssl

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram.types import ParseMode, MenuButtonWebApp, WebAppInfo
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import start_webhook
from aiohttp import web

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

    await dp.bot.set_webhook(
        url=f'{settings.tg_bot_webhook_url}{settings.tg_bot_webhook_path}/{settings.tg_bot_token}',
        certificate=open(settings.webhook_ssl_cert, 'rb'),
        drop_pending_updates=True,
    )
    await dp.bot.set_chat_menu_button(menu_button=MenuButtonWebApp(
        text='Магазин',
        web_app=WebAppInfo(url='https://MihailPereverza.github.io')
    ))


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
    bot = Bot(token=settings.tg_bot_token, parse_mode=ParseMode.MARKDOWN_V2)
    dp = Dispatcher(bot, storage=storage)

    logger.info('Сonfiguring web app')

    # app = get_new_configured_app(
    #     dispatcher=dp,
    #     path=settings.tg_bot_webhook_path,
    # )
    # app.on_startup.append(on_startup)
    # app.on_shutdown.append(on_shutdown)

    logger.info('Creating SSL context...')

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(settings.webhook_ssl_cert, settings.webhook_ssl_priv)
    print(settings.webhook_ssl_cert)

    logger.info('SSL context was created')
    logger.info('Web app was configuring')

    logger.info('Running web app...')
    print('adfsd')
    # web.run_app(
    #     app,
    #     host='0.0.0.0',
    #     port=3001,
    #     ssl_context=context
    # )
    start_webhook(
        dispatcher=dp,
        webhook_path=settings.tg_bot_webhook_path + settings.tg_bot_token,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port=80,
        ssl_context=context
    )

    logger.info('Web app was run')
    logger.info('Bot stated!')


if __name__ == '__main__':
    logger = get_logger('root')
    # try:
    main()
    # except (KeyboardInterrupt, SystemExit):
    #     logger.error('Bot stopped!')
    # except Exception as e:
    #     print(e)