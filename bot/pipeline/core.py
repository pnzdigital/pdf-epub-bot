import os
import shutil
from bot.processors.metadata import extract_metadata
from bot.processors.cover import extract_cover
from bot.processors.ocr_detect import needs_ocr, has_watermark
from bot.processors.pdf_to_markdown import pdf_to_markdown
from bot.processors.minimax_vision import ocr_pdf_pages


def create_workspace(session_id: str) -> str:
    """Cria diretório de trabalho temporário."""
    workspace = f"/tmp/pdf-epub-{session_id}"
    os.makedirs(workspace, exist_ok=True)
    return workspace


def process_pdf(pdf_path: str, session_id: str) -> dict:
    """
    Pipeline core: extrai metadados, capa, detecta OCR, converte.
    Retorna dict com markdown, cover_path, metadata.
    """
    workspace = create_workspace(session_id)

    # 1. Metadados
    file_name = os.path.basename(pdf_path)
    metadata = extract_metadata(file_name)

    # 2. Capa
    cover_path = f"{workspace}/cover.jpg"
    extract_cover(pdf_path, cover_path)

    # 3. Detecta OCR
    ocr_needed = needs_ocr(pdf_path)
    watermark = has_watermark(pdf_path)

    # 4. Converte
    if ocr_needed:
        markdown = ocr_pdf_pages(pdf_path, workspace)
    else:
        markdown = pdf_to_markdown(pdf_path)

    return {
        "markdown": markdown,
        "cover_path": cover_path,
        "metadata": metadata,
        "workspace": workspace,
        "ocr_needed": ocr_needed,
        "watermark": watermark,
    }
