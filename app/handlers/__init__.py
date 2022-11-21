from aiogram import Router

from handlers.balance_handlers.check_balance_update import (
    router as check_qiwi_balance_router
)
from handlers.balance_handlers.deposit_balance_handler import (
    router as deposit_balance_router
)
from handlers.balance_handlers.show_info_handler import (
    router as balance_info_router,
)
from handlers.main_menu_handler import router as main_menu_router
from handlers.profile_handlers.profile_handler import router as profile_router
from handlers.base_comands_handlers.start_handler import router as start_router


global_router = Router()


global_router.include_router(profile_router)
global_router.include_router(start_router)
global_router.include_router(balance_info_router)
global_router.include_router(check_qiwi_balance_router)
global_router.include_router(main_menu_router)
global_router.include_router(deposit_balance_router)
