import re


def extract_metadata(file_name: str) -> dict:
    """
    Extrai metadados do nome do arquivo.
    nome-do-livro-autor.pdf -> {title: nome-do-livro, author: autor}
    """
    # Remove extensão
    name = file_name.rsplit(".", 1)[0]

    # Separa por "-"
    parts = name.split("-")

    if len(parts) >= 2:
        title = parts[0].strip()
        author = "-".join(parts[1:]).strip()
    else:
        title = name
        author = "Desconhecido"

    return {
        "title": title,
        "author": author,
        "filename": name,
    }
