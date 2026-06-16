import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from bot.db import init_db

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Olá! Envie um PDF para começar.\n\n"
        "📄 Converter (1 crédito)\n"
        "🌐 Converter + Traduzir (2 créditos)\n"
        "⚙️ Configurações\n"
        "💳 Meu Plano"
    )


async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Comandos:\n"
        "/start - Iniciar\n"
        "/plano - Ver créditos\n"
        "/config - Configurações\n"
        "/fila - Ver arquivos na fila\n"
        "/limpar - Limpar fila\n"
        "/ajuda - Esta mensagem"
    )


async def plano_command(update: Update, context: CallbackContext):
    from bot.services.credits import get_user_info
    user_id = update.effective_user.id
    info = get_user_info(user_id)
    if info:
        await update.message.reply_text(
            f"💳 Seu Plano\n"
            f"Créditos: {info['credits']}\n"
            f"Plano: {info['plan_type'] or 'Nenhum'}\n"
            f"Expira: {info['plan_expires'] or 'N/A'}"
        )
    else:
        await update.message.reply_text(
            "Você ainda não tem um plano.\n"
            "Escolha um:\n"
            "📦 Básico - R$15/mês (20 créditos)\n"
            "📦 Padrão - R$25/mês (30 créditos)"
        )


async def config_command(update: Update, context: CallbackContext):
    from bot.services.credits import get_user_info
    from bot.db import get_ignore_words
    user_id = update.effective_user.id
    info = get_user_info(user_id)
    words = get_ignore_words(user_id)
    lang = info.get("default_language", "pt-BR") if info else "pt-BR"
    await update.message.reply_text(
        f"⚙️ Configurações\n\n"
        f"🌐 Idioma: {lang}\n"
        f"🚫 Palavras não traduzir: {len(words)}\n\n"
        f"Adicionar palavra: /config addpalavra\n"
        f"Remover palavra: /config removepalavra\n"
        f"Idioma: /config idioma [código]"
    )


async def fila_command(update: Update, context: CallbackContext):
    from bot.db import get_queue
    user_id = update.effective_user.id
    queue = get_queue(user_id)
    if not queue:
        await update.message.reply_text("📭 Fila vazia.")
        return
    msg = "📋 Sua fila:\n"
    for i, item in enumerate(queue, 1):
        msg += f"{i}. {item['file_name']} [{item['status']}]\n"
    await update.message.reply_text(msg)


async def limpar_command(update: Update, context: CallbackContext):
    from bot.db import clear_queue
    user_id = update.effective_user.id
    clear_queue(user_id)
    await update.message.reply_text("🗑️ Fila limpa.")


async def receive_pdf(update: Update, context: CallbackContext):
    from bot.db import add_to_queue
    from bot.handlers.menu import show_action_buttons

    file = update.message.document
    if not file.file_name.lower().endswith(".pdf"):
        await update.message.reply_text("Por favor, envie um arquivo PDF.")
        return

    user_id = update.effective_user.id
    file_path = f"/tmp/{file.file_unique_id}.pdf"

    # Download
    downloaded = await file.get_file()
    await downloaded.download_to_drive(file_path)

    # Add to queue
    add_to_queue(user_id, file.file_name, file_path)

    queue_count = len(get_queue(user_id))
    await update.message.reply_text(
        f"✅ Adicionado à fila. {queue_count} arquivo(s).\n\n"
        f"O que deseja fazer?"
    )
    await show_action_buttons(update, context)


def get_queue(user_id: int):
    from bot.db import get_queue as _get_queue
    return _get_queue(user_id)


from bot.handlers.admin import get_admin_handlers
from bot.handlers.config import get_config_handlers
from bot.handlers.actions import get_action_handlers


def create_app():
    init_db()

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ajuda", help_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("plano", plano_command))
    application.add_handler(CommandHandler("config", config_command))
    application.add_handler(CommandHandler("fila", fila_command))
    application.add_handler(CommandHandler("limpar", limpar_command))
    application.add_handler(MessageHandler(filters.Document.PDF, receive_pdf))

    # Admin handlers
    for handler in get_admin_handlers():
        application.add_handler(handler)

    # Config handlers
    for handler in get_config_handlers():
        application.add_handler(handler)

    # Action handlers (Converter, Converter+Traduzir, etc)
    for handler in get_action_handlers():
        application.add_handler(handler)

    return application


if __name__ == "__main__":
    tg_app = create_app()
    tg_app.run_polling()


# FastAPI app for health checks (Coolify)
from fastapi import FastAPI

api = FastAPI()


@api.get("/health")
async def health():
    return {"status": "ok"}


@api.get("/")
async def root():
    return {"bot": "pdf-epub-bot", "status": "running"}
