from aiogram import Router

from handlers.profile_handlers.profile_handler import router as profile_router
from handlers.base_comands_handlers.start_handler import router as start_router


global_router = Router()


global_router.include_router(profile_router)
global_router.include_router(start_router)
