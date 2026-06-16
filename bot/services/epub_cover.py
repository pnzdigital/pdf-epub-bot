import subprocess
import os


def insert_cover(epub_path: str, cover_path: str) -> str:
    """
    Insere capa JPEG no EPUB usando Calibre.
    """
    if not os.path.exists(cover_path):
        raise FileNotFoundError(f"Capa não encontrada: {cover_path}")

    # Calibre pode inserir capa durante conversão ou via ebook-meta
    # Aqui usamos abordagem simples: metadata + capa como primeira página
    # O ideal seria usar epub-meta ou similar

    # Por enquanto, a capa já é inserida pelo ebook-convert
    # quando o markdown tem a imagem no início
    return epub_path
