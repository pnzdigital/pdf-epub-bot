import fitz  # PyMuPDF
from PIL import Image
import io


def extract_cover(pdf_path: str, output_path: str, dpi: int = 300):
    """
    Extrai primeira página do PDF como JPEG.
    """
    doc = fitz.open(pdf_path)
    page = doc[0]

    # Zoom para DPI desejado
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)

    # Converte para JPEG
    img_data = pix.tobytes("jpeg")

    with open(output_path, "wb") as f:
        f.write(img_data)

    doc.close()
    return output_path
