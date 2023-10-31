from telegram.ext import ContextTypes

from core.utils.utils import *

async def toggle_attacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global AttacksEnabled
    if len(context.args) < 2:
        await update.message.reply_text("Invalid args! <enable/disable>")
        return
    users_data = load_users_data()
    command = context.args[0].lower()
    if command == "enable":
        AttacksEnabled = True
        await update.message.reply_text("Attacks enabled.")
    elif command == "disable":
        AttacksEnabled = False
        await update.message.reply_text("Attacks disabled.")
    else:
        await update.message.reply_text("use: /attacks <new status>")
