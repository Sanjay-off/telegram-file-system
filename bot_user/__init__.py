# bot_user/__init__.py

from aiogram import Router

# ===========================
# IMPORT ALL USER BOT ROUTERS
# ===========================

from bot_user.handlers.start import router as start_router
from bot_user.handlers.help import router as help_router
from bot_user.handlers.checkpremium import router as checkpremium_router
from bot_user.handlers.download_flow import router as download_router
from bot_user.handlers.force_sub_checker import router as force_sub_router
from bot_user.handlers.verification_flow import router as verification_router
from bot_user.handlers.bypass_detection import router as bypass_router
from bot_user.handlers.premium_purchase import router as premium_router
from bot_user.handlers.qr_generator import router as qr_router
from bot_user.handlers.verify_payment import router as verify_payment_router
from bot_user.handlers.file_delivery import router as delivery_router
from bot_user.handlers.click_here_flow import router as click_router

# Optional future handlers (once generated)
# from bot_user.handlers.id import router as id_router
# from bot_user.handlers.how_to_verify import router as how_to_verify_router
# from bot_user.handlers.close_buttons import router as close_router


# ===========================
# MAIN SETUP FUNCTION
# ===========================

def setup_user_handlers() -> Router:
    """
    Creates a root router and registers ALL user bot handlers.

    This router will be imported into user_main.py:
        dp.include_router(setup_user_handlers())
    """

    root = Router()

    # Register all routers
    root.include_router(start_router)
    root.include_router(help_router)
    root.include_router(checkpremium_router)
    root.include_router(download_router)
    root.include_router(force_sub_router)
    root.include_router(verification_router)
    root.include_router(bypass_router)
    root.include_router(premium_router)
    root.include_router(qr_router)
    root.include_router(verify_payment_router)
    root.include_router(delivery_router)
    root.include_router(click_router)

    # If you later generate additional handlers, uncomment these:
    # root.include_router(id_router)
    # root.include_router(how_to_verify_router)
    # root.include_router(close_router)

    return root
