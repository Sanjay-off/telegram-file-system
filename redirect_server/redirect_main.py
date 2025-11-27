# redirect_server/redirect_main.py

import uvicorn
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.config import config
from core.database import init_db
from core.utils.logger import get_redirect_logger
from redirect_server.token_handler import RedirectTokenHandler

app = FastAPI()
logger = get_redirect_logger()

# Static & Template Mounts
app.mount("/static", StaticFiles(directory="redirect_server/static"), name="static")
templates = Jinja2Templates(directory="redirect_server/templates")

# Initialize DB
init_db()


# ============================================================
# 1) REDIRECT ENTRY POINT  /redirect?token=<token>
# ============================================================
@app.get("/redirect", response_class=HTMLResponse)
async def redirect_entry(request: Request, token: str = Query(default=None)):
    """
    User lands here after shortlink.
    Steps:
     - Decode token
     - Validate
     - Log visit for anti-bypass
     - Show countdown page
    """
    if not token:
        logger.warning("Redirect request with missing token")
        return HTMLResponse("<h1>Invalid Token</h1>")

    payload = RedirectTokenHandler.decode_incoming_token(token)
    if not payload:
        logger.warning(f"Invalid token decode: {token}")
        return HTMLResponse("<h1>Invalid or Expired Verification Token</h1>")

    user_id = payload.get("user_id")

    # Log the visit (used for bypass detection)
    RedirectTokenHandler.log_visit(user_id, token)

    logger.info(f"[Redirect] User {user_id} visited redirect page")

    # Show countdown.html
    return templates.TemplateResponse(
        "countdown.html",
        {
            "request": request,
            "user_id": user_id,
            "file_id": payload.get("file_id"),
            "post_no": payload.get("post_no"),
            "token": token
        }
    )


# ============================================================
# 2) RETURN URL — Called after countdown completes
# GET /return?result=verified&token=<token>
# ============================================================
@app.get("/return")
async def return_to_bot(
    request: Request,
    result: str = Query(default=None),
    token: str = Query(default=None)
):
    """
    The countdown page calls this after user finishes waiting.
    This endpoint decides:
     - Verified OR
     - Bypass Detected
    and returns an HTTP redirect to Telegram.

    Example final redirect:
      https://t.me/BotB?start=verified_<signedPacket>
    """

    if not token:
        return HTMLResponse("<h1>Missing Token</h1>")

    payload = RedirectTokenHandler.decode_incoming_token(token)
    if not payload:
        logger.warning("Return with invalid token")
        return HTMLResponse("<h1>Invalid Token</h1>")

    user_id = payload.get("user_id")
    file_id = payload.get("file_id")
    post_no = payload.get("post_no")

    visited = RedirectTokenHandler.did_user_visit(user_id, token)

    if not visited:
        # BYPASS DETECTED
        logger.warning(f"[BYPASS] User {user_id} attempted bypass.")
        final_token = RedirectTokenHandler.build_bypass_token(
            user_id, file_id, post_no
        )
    else:
        # VERIFIED SUCCESSFULLY
        logger.info(f"[VERIFIED] User {user_id} successfully verified.")
        final_token = RedirectTokenHandler.build_verified_token(
            user_id, file_id, post_no
        )

    # Redirect back to Telegram Bot B
    bot_username = config.BOT_B_USERNAME
    redirect_url = f"https://t.me/{bot_username}?start={final_token}"

    return RedirectResponse(url=redirect_url)


# ============================================================
# 3) ROOT INDEX
# ============================================================
@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse("<h2>Telegram Verification Redirect Server Running ✔</h2>")


# ============================================================
# 4) SERVER RUNNER
# ============================================================
if __name__ == "__main__":
    logger.info("🚀 Starting Redirect Server")

    uvicorn.run(
        "redirect_server.redirect_main:app",
        host="0.0.0.0",
        port=5000,
        reload=False
    )
