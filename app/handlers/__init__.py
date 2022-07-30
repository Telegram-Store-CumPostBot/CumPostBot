from aiogram import Router

from handlers.profile_handler import router as profile_router


global_router = Router()


global_router.include_router(profile_router)
