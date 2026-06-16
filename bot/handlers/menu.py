from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext


async def show_action_buttons(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📄 Converter (1 crédito)", callback_data="action_convert")],
        [InlineKeyboardButton("🌐 Converter + Traduzir (2 créditos)", callback_data="action_translate")],
        [InlineKeyboardButton("⚙️ Configurações", callback_data="action_config")],
        [InlineKeyboardButton("💳 Meu Plano", callback_data="action_plano")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha uma ação:", reply_markup=reply_markup)


async def show_config_menu(update: Update, context: CallbackContext, edit: bool = False):
    from bot.db import get_ignore_words
    from bot.services.credits import get_user_info

    user_id = update.effective_user.id
    info = get_user_info(user_id)
    words = get_ignore_words(user_id)
    lang = info.get("default_language", "pt-BR") if info else "pt-BR"

    keyboard = [
        [InlineKeyboardButton(f"🌐 Idioma: {lang}", callback_data="config_idioma")],
        [InlineKeyboardButton(f"🚫 Palavras não traduzir: {len(words)}", callback_data="config_palavras")],
        [InlineKeyboardButton("➕ Adicionar palavra", callback_data="config_add")],
        [InlineKeyboardButton("➖ Remover palavra", callback_data="config_remove")],
        [InlineKeyboardButton("🗑️ Limpar lista", callback_data="config_clear")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="config_back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"⚙️ Configurações\n\n🌐 Idioma: {lang}\n🚫 Palavras: {len(words)}"

    if edit:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)
