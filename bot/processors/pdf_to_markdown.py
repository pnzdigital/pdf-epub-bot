import fitz  # PyMuPDF
import re


def pdf_to_markdown(pdf_path: str) -> str:
    """
    Extrai texto de PDF e converte para Markdown.
    Preserva parágrafos, legendas e formatação básica.
    """
    doc = fitz.open(pdf_path)
    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()

        # Limpa texto
        text = clean_text(text)
        pages.append(text)

    doc.close()
    return "\n\n".join(pages)


def clean_text(text: str) -> str:
    """
    Limpa texto extraído: removes caracteres quebrados,
    conserta pontuação, normaliza espaços.
    """
    # Normaliza spaces
    text = re.sub(r"[ \t]+", " ", text)
    # Remove linhas vazias duplicadas
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Conserta hifens quebrados
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    # Remove caracteres de controle
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return text.strip()
