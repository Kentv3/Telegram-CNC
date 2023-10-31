import json
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes, CallbackContext

from core.commands.attack import load_users_data, update_attack_data, save_users_data


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

@restricted(["admin", "reseller"])
async def manage_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Invalid args! /users <add/remove/list>")
        return
    users_data = load_users_data()
    command = context.args[0].lower()

    if command == "add":
        if len(context.args) <= 5:
            await update.message.reply_text(
                "use: /users add <tg id> <concurrents> <expiry[days]> <...roles>")
            return

        userid = int(context.args[1])
        concurrents = int(context.args[2])
        expiry = int(context.args[3])
        roles = context.args[4:]

        user_id = str(userid) # store as string
        if user_id in users_data:
            await update.message.reply_text("This user is already registered.")
            return

        created_by = f"@{update.effective_user.username}"
        users_data[user_id] = {
            "roles": roles,
            "expiry": expiry,
            "createdby": created_by,
            "concurrent_attacks": concurrents
        }
        save_users_data(users_data)
        await update.message.reply_text("User added successfully.")

    elif command == "list":
        user_list = "Users:\n\n"
        for user_id, user_info in users_data.items():
            roles = ', '.join(user_info['roles'])
            user_list += (
                f"User ID: {user_id}\n"
                f"Roles: {roles}\n"
                f"Expiry: {user_info['expiry']} days\n"
                f"Created by: {user_info['createdby']}\n"
                f"Concurrent Attacks: {user_info['concurrent_attacks']}\n\n"
            )
        await update.message.reply_text(user_list.strip())

    elif command == "remove":
        user_id = str(context.args[1])
        if user_id in users_data:
            if "reseller" in users_data[user_id]["roles"] and users_data[user_id][
                "createdby"] != f"@{update.effective_user.username}":
                await update.message.reply_text("You can only remove users created by you.")
            else:
                del users_data[user_id]
                save_users_data(users_data)
                await update.message.reply_text("User removed successfully.")
        else:
            await update.message.reply_text("User not found.")
    else:
        await update.message.reply_text("use: /users <add/remove>")