# bot_user/keyboards/inline_buttons.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ============================================================
# FORCE-SUB KEYBOARD (For download & verification flows)
# ============================================================
def force_sub_keyboard(not_joined_channels):
    """
    not_joined_channels = [
      {"channel": "@Backup", "button_text": "BACKUP"},
      {"channel": "@MovieZone", "button_text": "MOVIES"},
    ]
    """
    rows = []

    for ch in not_joined_channels:
        rows.append([
            InlineKeyboardButton(
                text=ch.get("button_text", ch["channel"]),
                url=f"https://t.me/{ch['channel'].replace('@','')}"
            )
        ])

    # TRY AGAIN button
    rows.append([
        InlineKeyboardButton(text="🔄 TRY AGAIN", callback_data="force_try_again")
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


# ============================================================
# VERIFICATION BUTTONS
# ============================================================
def verify_keyboard(encoded):
    """
    Buttons shown in the main verification screen:
    VERIFY NOW • GET PREMIUM • HOW TO VERIFY
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✔ VERIFY NOW",
                    url=f"https://t.me/{''}?start=verify_{encoded}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💎 GET PREMIUM (UNLIMITED)",
                    callback_data=f"getpremium_{encoded}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📘 HOW TO VERIFY",
                    callback_data="how_to_verify"
                )
            ]
        ]
    )


def verify_now_button(short_url):
    """
    Button for redirect through shortlink.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✔ VERIFY NOW",
                    url=short_url
                )
            ]
        ]
    )


def get_premium_button(encoded):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💎 GET PREMIUM",
                    callback_data=f"getpremium_{encoded}"
                )
            ]
        ]
    )


def how_to_verify_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📘 HOW TO VERIFY",
                    callback_data="how_to_verify"
                )
            ]
        ]
    )


# ============================================================
# SHORTLINK VERIFICATION – MAIN UI (short_url + encoded)
# ============================================================
def verification_main_keyboard(short_url, encoded):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✔ VERIFY NOW",
                    url=short_url
                )
            ],
            [
                InlineKeyboardButton(
                    text="💎 GET PREMIUM",
                    callback_data=f"getpremium_{encoded}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📘 HOW TO VERIFY",
                    callback_data="how_to_verify"
                )
            ]
        ]
    )


# ============================================================
# CLICK HERE FLOW (after file auto-delete)
# ============================================================
def clickhere_keyboard(encoded):
    """
    encoded = encoded token for click_<encoded>
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📥 CLICK HERE TO DOWNLOAD",
                    url=f"https://t.me/{''}?start=click_{encoded}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ CLOSE",
                    callback_data="close_click_here"
                )
            ]
        ]
    )


# ============================================================
# CLOSE MESSAGE BUTTON
# ============================================================
def close_message_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ CLOSE",
                    callback_data="close_message_now"
                )
            ]
        ]
    )


# ============================================================
# BYPASS DETECTION – TRY AGAIN BUTTON
# ============================================================
def try_again_keyboard(file_id, post_no):
    encoded = f"{file_id}|{post_no}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 TRY AGAIN",
                    url=f"https://t.me/{''}?start=get_{encoded}"
                )
            ]
        ]
    )


# ============================================================
# PREMIUM PLANS KEYBOARD
# ============================================================
def premium_plans_keyboard(plans):
    """
    plans = [
      {"plan_id": "...", "days": 30, "price": 40},
      ...
    ]
    """
    rows = []

    for p in plans:
        text = f"{p['days']} DAYS — ₹{p['price']}"
        rows.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"buyplan_{p['plan_id']}"
            )
        ])

    # BACK button (back to verify panel)
    rows.append([
        InlineKeyboardButton(
            text="⬅ BACK",
            callback_data="premium_back"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


# ============================================================
# UPI QR PAYMENT KEYBOARD
# ============================================================
def premium_qr_keyboard(upi_url, order_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 PAY NOW (UPI)",
                    url=upi_url
                )
            ],
            [
                InlineKeyboardButton(
                    text="✔ VERIFY PAYMENT",
                    callback_data=f"verifypay_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅ BACK",
                    callback_data="premium_back"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ CLOSE",
                    callback_data="close_message_now"
                )
            ]
        ]
    )


# ============================================================
# PAYMENT VERIFY KEYBOARD (for pending orders)
# ============================================================
def payment_verify_keyboard(order_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✔ VERIFY PAYMENT AGAIN",
                    callback_data=f"verifypay_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅ BACK",
                    callback_data="premium_back"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ CLOSE",
                    callback_data="close_message_now"
                )
            ]
        ]
    )


# ============================================================
# PREMIUM BACK BUTTON
# ============================================================
def premium_back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅ BACK",
                    callback_data="premium_back"
                )
            ]
        ]
    )
