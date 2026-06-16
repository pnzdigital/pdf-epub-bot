import subprocess
import os


def markdown_to_epub(md_path: str, epub_path: str) -> str:
    """
    Converte Markdown para EPUB usando Calibre.
    """
    result = subprocess.run(
        ["ebook-convert", md_path, epub_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Calibre error: {result.stderr}")
    return epub_path
