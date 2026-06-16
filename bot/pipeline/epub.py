import os
from bot.services.calibre import markdown_to_epub
from bot.services.epub_metadata import set_epub_metadata
from bot.pipeline.cleanup import cleanup_file


def build_epub(
    markdown: str,
    cover_path: str,
    metadata: dict,
    output_path: str,
    workspace: str
) -> str:
    """
    Constrói EPUB: salva markdown, converte, insere capa e metadados.
    """
    # Salva markdown temporário
    md_path = f"{workspace}/content.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    # Converte para EPUB
    epub_path = output_path
    markdown_to_epub(md_path, epub_path)

    # Insere metadados
    set_epub_metadata(
        epub_path,
        title=metadata.get("title", "Sem título"),
        author=metadata.get("author", "Desconhecido"),
        identifier=metadata.get("filename"),
    )

    # Limpa markdown temporário
    cleanup_file(md_path)

    return epub_path
