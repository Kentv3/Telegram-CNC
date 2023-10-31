from telegram import Update
from telegram.ext import ContextTypes


async def helpme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "available commands:\n\n\n"
        "/attack - Start an attack\n"
        "Usage: /attack <host> <port> <time> <method>\n\n"

        "/attacks - Manage attacks\n"
        "Usage: /attacks <enable|disable>\n\n"

        "/start - Start the bot\n"
        "Usage: /start\n\n"

        "/ongoing - View ongoing attacks\n"
        "Usage: /ongoing\n\n"

        "/users - Manage users\n"
        "Usage: /users <add|remove|list>\n\n"

        "/help - Show this menu\n"
        "Usage: /help\n"
    )

    await update.message.reply_text(help_text)
