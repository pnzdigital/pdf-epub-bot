import fitz  # PyMuPDF


def needs_ocr(pdf_path: str, threshold: int = 50) -> bool:
    """
    Verifica se primeira página do PDF tem texto suficiente.
    Se < threshold caracteres -> precisa de OCR.
    """
    doc = fitz.open(pdf_path)
    page = doc[0]
    text = page.get_text()
    doc.close()

    # Conta caracteres não-brancos
    chars = len(text.strip())
    return chars < threshold


def has_watermark(pdf_path: str) -> bool:
    """
    Detecta marca d'água básica na primeira página.
    Procura padrões comuns de marca d'água.
    """
    doc = fitz.open(pdf_path)
    page = doc[0]
    text = page.get_text().lower()
    doc.close()

    watermark_patterns = [
        "watermark", "amostra", "gratuito", "preview",
        "sample", "copy", "evaluation", "trial",
    ]
    return any(p in text for p in watermark_patterns)
