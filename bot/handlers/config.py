from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler

from bot.db import (
    get_ignore_words, add_ignore_word, remove_ignore_word,
    clear_ignore_words, get_user, update_user_language
)
from bot.services.credits import get_user_info


# Estados da conversa
ASK_WORD, ASK_LANG = range(2)


async def config_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    info = get_user_info(user_id)
    words = get_ignore_words(user_id)
    lang = info.get("default_language", "pt-BR") if info else "pt-BR"

    keyboard = [
        [InlineKeyboardButton(f"🌐 Idioma: {lang}", callback_data="config_idioma")],
        [InlineKeyboardButton(f"🚫 Palavras: {len(words)}", callback_data="config_palavras")],
        [InlineKeyboardButton("➕ Adicionar palavra", callback_data="config_add")],
        [InlineKeyboardButton("➖ Remover palavra", callback_data="config_remove")],
        [InlineKeyboardButton("🗑️ Limpar lista", callback_data="config_clear")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="config_back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"⚙️ Configurações\n\n🌐 Idioma: {lang}\n🚫 Palavras: {len(words)}",
        reply_markup=reply_markup
    )


async def config_idioma_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🇧🇷 Português", callback_data="lang_pt-BR")],
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en-US")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es-ES")],
        [InlineKeyboardButton("🇫🇷 Français", callback_data="lang_fr-FR")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="config_back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "🌐 Escolha o idioma de tradução:",
        reply_markup=reply_markup
    )


async def config_lang_select_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    lang_map = {
        "lang_pt-BR": "pt-BR",
        "lang_en-US": "en-US",
        "lang_es-ES": "es-ES",
        "lang_fr-FR": "fr-FR",
    }

    lang_code = lang_map.get(query.data)
    if not lang_code:
        return

    user_id = update.effective_user.id
    user = get_user(user_id)
    if user:
        update_user_language(user_id, lang_code)

    await config_command(update, context)


async def config_palavras_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    words = get_ignore_words(user_id)

    if not words:
        text = "🚫 Lista vazia."
    else:
        text = "🚫 Palavras não traduzir:\n\n" + "\n".join(f"- {w}" for w in words)

    keyboard = [[InlineKeyboardButton("🔙 Voltar", callback_data="config_back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text, reply_markup=reply_markup)


async def config_add_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "➕ Digite a palavra que NÃO quer traduzir:"
    )
    return ASK_WORD


async def config_add_word(update: Update, context: CallbackContext):
    word = update.message.text.strip()
    if not word:
        await update.message.reply_text("Palavra vazia. Tente novamente.")
        return ASK_WORD

    user_id = update.effective_user.id
    add_ignore_word(user_id, word)

    await update.message.reply_text(f"✅ '{word}' adicionada à lista.")
    await config_command(update, context)
    return ConversationHandler.END


async def config_remove_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    words = get_ignore_words(user_id)

    if not words:
        await query.edit_message_text("🚫 Lista vazia.")
        return

    keyboard = [
        [InlineKeyboardButton(f"❌ {w}", callback_data=f"remove_{w}")]
        for w in words
    ]
    keyboard.append([InlineKeyboardButton("🔙 Voltar", callback_data="config_back")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "➖ Selecione a palavra para remover:",
        reply_markup=reply_markup
    )


async def config_remove_word_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if not query.data.startswith("remove_"):
        return

    word = query.data[7:]  # Remove "remove_"
    user_id = update.effective_user.id
    remove_ignore_word(user_id, word)

    await query.edit_message_text(f"✅ '{word}' removida.")
    await config_command(update, context)


async def config_clear_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    clear_ignore_words(user_id)

    await query.edit_message_text("🗑️ Lista limpa.")
    await config_command(update, context)


async def config_back_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await config_command(update, context)


def get_config_handlers():
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(config_add_callback, pattern="config_add")],
        states={
            ASK_WORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, config_add_word)],
        },
        fallbacks=[],
    )

    return [
        CommandHandler("config", config_command),
        CallbackQueryHandler(config_idioma_callback, pattern="config_idioma"),
        CallbackQueryHandler(config_lang_select_callback, pattern="^lang_"),
        CallbackQueryHandler(config_palavras_callback, pattern="config_palavras"),
        CallbackQueryHandler(config_remove_callback, pattern="config_remove"),
        CallbackQueryHandler(config_remove_word_callback, pattern="^remove_"),
        CallbackQueryHandler(config_clear_callback, pattern="config_clear"),
        CallbackQueryHandler(config_back_callback, pattern="config_back"),
        conv,
    ]
