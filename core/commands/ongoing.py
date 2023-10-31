import time
from telegram import Update
from telegram.ext import ContextTypes
from core.commands.users import restricted
from core.utils.utils import update_attack_data, load_users_data, ongoing_attacks

@restricted(["admin"])
async def show_ongoing_attacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users_data = load_users_data()
    update_attack_data()
    output = "🛡️ Ongoing Attacks 🛡️\n\n"
    for user_id, attacks in ongoing_attacks.items():
        for attack in attacks:
            remaining_time = attack["start_time"] + attack["duration"] - time.time()
            output += "------------------------------\n"
            output += (
                f"👤 User: {users_data[user_id]['username']}\n"
                f"🌐 Host: {attack['host']}\n"
                f"🔌 Port: {attack['port']}\n"
                f"⏳ Duration: {attack['duration']} seconds\n"
                f"⏰ Remaining Time: {max(0, remaining_time):.2f} seconds\n"
            )
    output += "------------------------------"
    await update.message.reply_text(output)
