import os
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from bot.services.credits import reset_credits_lua, update_credits, get_user


LUA_USER_ID = int(os.getenv("LUA_USER_ID", "0"))


async def resetcredits_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if user_id != LUA_USER_ID:
        await update.message.reply_text("Comando não disponível.")
        return

    reset_credits_lua()
    await update.message.reply_text("✅ Créditos resetados para 1000.")


async def setcredits_command(update: Update, context: CallbackContext):
    """Admin: set credits for any user. Usage: /setcredits <user_id> <amount>"""
    user_id = update.effective_user.id

    if user_id != LUA_USER_ID:
        await update.message.reply_text("Comando não disponível.")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Uso: /setcredits <user_id> <amount>")
        return

    try:
        target_id = int(args[0])
        amount = int(args[1])
    except ValueError:
        await update.message.reply_text("user_id e amount devem ser números.")
        return

    update_credits(target_id, amount)
    await update.message.reply_text(f"✅ Créditos de {target_id} definidos para {amount}.")


def get_admin_handlers():
    return [
        CommandHandler("resetcredits", resetcredits_command),
        CommandHandler("setcredits", setcredits_command),
    ]
