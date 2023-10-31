import json
from collections import defaultdict
import time
from functools import wraps

from telegram import Update
from telegram.ext import CallbackContext


def restricted(allowed_roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
            update_attack_data()
            users_data = load_users_data()
            user_id = str(update.effective_user.id)
            if user_id in users_data and any(role in users_data[user_id]["roles"] for role in allowed_roles):
                return await func(update, context, *args, **kwargs)
            else:
                await update.message.reply_text("You are not authorized to perform this action.")

        return wrapper

    return decorator


def update_attack_data():
    global attack_cooldown, ongoing_attacks
    current_time = time.time()
    for user_id, attacks in ongoing_attacks.items():
        attacks[:] = [attack for attack in attacks if attack["start_time"] + attack["duration"] > current_time]
    if current_time - attack_cooldown > 60:
        attack_cooldown = current_time
        global_attack_count = 0
def load_users_data():
    with open("users.json", "r") as users_file:
        return json.load(users_file)


def save_users_data(users_data):
    with open("users.json", "w") as users_file:
        json.dump(users_data, users_file, indent=4)


def load_attacks_config():
    with open("attacks.json", "r") as attacks_file:
        return json.load(attacks_file)


attack_cooldown = time.time()
ongoing_attacks = defaultdict(list)
global_attack_count = 0
AttacksEnabled = True

