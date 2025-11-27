# bot_admin/__init__.py

from aiogram import Router

# Import all handler modules
from bot_admin.handlers.start import router as start_router
from bot_admin.handlers.menu import router as menu_router
from bot_admin.handlers.file_upload import router as file_upload_router
from bot_admin.handlers.file_template import router as file_template_router
from bot_admin.handlers.force_sub import router as force_sub_router
from bot_admin.handlers.verification_settings import router as verification_router
from bot_admin.handlers.premium_plans import router as premium_plans_router
from bot_admin.handlers.payment_settings import router as payment_settings_router
from bot_admin.handlers.order_management import router as order_router
from bot_admin.handlers.shortener_settings import router as shortener_router
from bot_admin.handlers.stats import router as stats_router
from bot_admin.handlers.grant_verify import router as grant_verify_router


def setup_admin_handlers() -> Router:
    """
    Register and combine all Admin Bot routers.
    Returns a Router object to be included in admin_main.py.
    """

    admin_router = Router()

    # Add all routers
    admin_router.include_router(start_router)
    admin_router.include_router(menu_router)
    admin_router.include_router(file_upload_router)
    admin_router.include_router(file_template_router)
    admin_router.include_router(force_sub_router)
    admin_router.include_router(verification_router)
    admin_router.include_router(premium_plans_router)
    admin_router.include_router(payment_settings_router)
    admin_router.include_router(order_router)
    admin_router.include_router(shortener_router)
    admin_router.include_router(stats_router)
    admin_router.include_router(grant_verify_router)

    return admin_router
