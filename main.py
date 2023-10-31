from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler
from core.commands.attacks import toggle_attacks
from core.commands.hello import hello
from core.commands.help import helpme
from core.commands.ongoing import show_ongoing_attacks
from core.commands.users import manage_users
from core.commands.attack import perform_attack
from core.config.loadConfig import loadConfig


def main():
    configuration = loadConfig()
    bot_token = configuration.get("token", "")

    if not bot_token:
        raise ValueError("Bot token not found in configuration.json")

    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", hello))
    app.add_handler(CommandHandler("users", manage_users))
    app.add_handler(CommandHandler("attacks", toggle_attacks))
    app.add_handler(CommandHandler("ongoing", show_ongoing_attacks))
    app.add_handler(CommandHandler("help", helpme))
    app.add_handler(CommandHandler("attack", perform_attack))

    print("\x1b[90m[\x1b[94mCronical \x1b[90m- \x1b[94mDebug\x1b[90m]: \x1b[0mStarting telegram bot")
    app.run_polling()


if __name__ == "__main__":
    main()
