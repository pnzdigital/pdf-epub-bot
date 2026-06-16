from telegram import Update, InputFile
from telegram.ext import CallbackContext
import os


async def deliver_epub(
    update: Update,
    context: CallbackContext,
    epub_path: str,
    file_name: str = None
):
    """
    Envia EPUB para o chat do usuário.
    """
    if not os.path.exists(epub_path):
        await update.callback_query.edit_message_text(
            "❌ Erro: arquivo EPUB não encontrado."
        )
        return

    if file_name is None:
        file_name = os.path.basename(epub_path)

    with open(epub_path, "rb") as f:
        await update.callback_query.edit_message_text("📤 Enviando...")
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=f,
            filename=file_name,
            caption="✅ EPUB pronto!"
        )
