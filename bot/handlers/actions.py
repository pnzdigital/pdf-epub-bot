from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot.db import get_queue, update_queue_status
from bot.services.credits import check_credits, descontar_creditos
from bot.pipeline.core import process_pdf
from bot.pipeline.translate import translate_pipeline
from bot.pipeline.epub import build_epub
from bot.pipeline.cleanup import cleanup_workspace
from bot.handlers.deliver import deliver_epub


async def action_convert_callback(update: Update, context: CallbackContext):
    """Processa fila: apenas converter."""
    query = update.callback_query
    user_id = update.effective_user.id

    # Verifica créditos
    if not check_credits(user_id, 1):
        await query.answer("❌ Créditos insuficientes.", show_alert=True)
        return

    # Pega fila
    queue = get_queue(user_id)
    if not queue:
        await query.answer("📭 Fila vazia.", show_alert=True)
        return

    await query.answer("🔄 Processando...")
    await query.edit_message_text("🔄 Convertendo...")

    # Processa cada PDF
    for item in queue:
        try:
            update_queue_status(item["id"], "processing")

            # Pipeline core
            result = process_pdf(item["file_path"], str(item["id"]))

            # Constrói EPUB
            epub_path = f"/tmp/{result['metadata']['filename']}.epub"
            build_epub(
                markdown=result["markdown"],
                cover_path=result["cover_path"],
                metadata=result["metadata"],
                output_path=epub_path,
                workspace=result["workspace"],
            )

            # Desconta crédito
            descontar_creditos(user_id, 1)

            # Entrega
            await deliver_epub(update, context, epub_path)

            # Limpa
            cleanup_workspace(result["workspace"])

            update_queue_status(item["id"], "done")

        except Exception as e:
            cleanup_workspace(result.get("workspace", ""))
            update_queue_status(item["id"], "failed")
            await query.edit_message_text(f"❌ Erro: {str(e)}")


async def action_translate_callback(update: Update, context: CallbackContext):
    """Processa fila: converter + traduzir."""
    query = update.callback_query
    user_id = update.effective_user.id

    # Verifica créditos
    if not check_credits(user_id, 2):
        await query.answer("❌ Créditos insuficientes.", show_alert=True)
        return

    # Pega fila
    queue = get_queue(user_id)
    if not queue:
        await query.answer("📭 Fila vazia.", show_alert=True)
        return

    await query.answer("🔄 Processando...")
    await query.edit_message_text("🔄 Convertendo e traduzindo...")

    # Processa cada PDF
    for item in queue:
        try:
            update_queue_status(item["id"], "processing")

            # Pipeline core
            result = process_pdf(item["file_path"], str(item["id"]))

            # Traduz
            translated = translate_pipeline(result["markdown"], user_id)

            # Constrói EPUB
            epub_path = f"/tmp/{result['metadata']['filename']}_translated.epub"
            build_epub(
                markdown=translated,
                cover_path=result["cover_path"],
                metadata=result["metadata"],
                output_path=epub_path,
                workspace=result["workspace"],
            )

            # Desconta créditos
            descontar_creditos(user_id, 2)

            # Entrega
            await deliver_epub(update, context, epub_path)

            # Limpa
            cleanup_workspace(result["workspace"])

            update_queue_status(item["id"], "done")

        except Exception as e:
            cleanup_workspace(result.get("workspace", ""))
            update_queue_status(item["id"], "failed")
            await query.edit_message_text(f"❌ Erro: {str(e)}")


async def action_plano_callback(update: Update, context: CallbackContext):
    """Mostra plano do usuário."""
    from bot.services.credits import get_user_info

    query = update.callback_query
    user_id = update.effective_user.id
    info = get_user_info(user_id)

    if info:
        text = (
            f"💳 Seu Plano\n"
            f"Créditos: {info['credits']}\n"
            f"Plano: {info['plan_type'] or 'Nenhum'}\n"
            f"Expira: {info['plan_expires'] or 'N/A'}"
        )
    else:
        text = (
            "💳 Você ainda não tem um plano.\n\n"
            "📦 Básico - R$15/mês (20 créditos)\n"
            "📦 Padrão - R$25/mês (30 créditos)"
        )

    keyboard = [[InlineKeyboardButton("🔙 Voltar", callback_data="action_back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)


async def action_config_callback(update: Update, context: CallbackContext):
    """Redireciona para configurações."""
    from bot.handlers.config import config_command
    query = update.callback_query
    await query.answer()
    await config_command(update, context)


async def action_back_callback(update: Update, context: CallbackContext):
    """Volta para menu principal."""
    from bot.handlers.menu import show_action_buttons
    query = update.callback_query
    await query.answer()
    await show_action_buttons(update, context)


def get_action_handlers():
    return [
        CallbackQueryHandler(action_convert_callback, pattern="action_convert"),
        CallbackQueryHandler(action_translate_callback, pattern="action_translate"),
        CallbackQueryHandler(action_plano_callback, pattern="action_plano"),
        CallbackQueryHandler(action_config_callback, pattern="action_config"),
        CallbackQueryHandler(action_back_callback, pattern="action_back"),
    ]
