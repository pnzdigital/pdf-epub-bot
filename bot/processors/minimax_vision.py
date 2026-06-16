import os
import httpx
from PIL import Image
import fitz
import io


MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat")


def ocr_page(image_path: str) -> str:
    """
    Envia uma página como imagem para MiniMax Visão.
    Retorna texto extraído.
    """
    if not MINIMAX_API_KEY:
        raise ValueError("MINIMAX_API_KEY não configurado")

    with open(image_path, "rb") as f:
        image_data = f.read()

    # Codifica como base64
    import base64
    b64 = base64.b64encode(image_data).decode()

    prompt = (
        "Extraia todo o texto desta página. Preserve parágrafos, legendas e formatação. "
        "Retorne apenas o texto extraído, sem comentários."
    )

    payload = {
        "model": "MiniMax-VL-01",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                ]
            }
        ],
        "max_tokens": 4096,
    }

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json",
    }

    with httpx.Client(timeout=60) as client:
        resp = client.post(
            f"{MINIMAX_BASE_URL}/v1/text/chatcompletion_v2",
            headers=headers,
            json=payload
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


def pdf_page_to_image(pdf_path: str, page_num: int, dpi: int = 200) -> bytes:
    """
    Converte uma página do PDF para bytes de imagem JPEG.
    """
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    data = pix.tobytes("jpeg")
    doc.close()
    return data


def ocr_pdf_pages(pdf_path: str, temp_dir: str) -> str:
    """
    Faz OCR de todas as páginas do PDF via MiniMax Visão.
    Retorna texto concatenado.
    """
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()

    texts = []
    for i in range(total_pages):
        # Salva página temporária
        img_bytes = pdf_page_to_image(pdf_path, i)
        temp_img = f"{temp_dir}/page_{i}.jpg"
        with open(temp_img, "wb") as f:
            f.write(img_bytes)

        # OCR
        text = ocr_page(temp_img)
        texts.append(text)

    return "\n\n".join(texts)
