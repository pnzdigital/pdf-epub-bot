import subprocess


def set_epub_metadata(epub_path: str, title: str, author: str, identifier: str = None) -> str:
    """
    Insere metadados no EPUB usando Calibre ebook-meta.
    """
    cmd = [
        "ebook-meta", epub_path,
        "--title", title,
        "--author", author,
    ]
    if identifier:
        cmd.extend(["--identifier", f"uuid:{identifier}"])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ebook-meta error: {result.stderr}")

    return epub_path
