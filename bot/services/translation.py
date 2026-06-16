import re
from bot.db import get_ignore_words
from bot.services.minimax_chat import translate_text


def protect_words(text: str, words: list[str]) -> tuple[str, dict[str, str]]:
    """
    Substitui palavras da lista por placeholders únicos.
    Retorna texto com placeholders + mapa de restauração.
    """
    placeholder_map = {}
    protected = text

    for i, word in enumerate(words):
        placeholder = f"__PROTECTED_{i}__"
        placeholder_map[placeholder] = word
        # Substitui word case-insensitive
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        protected = pattern.sub(placeholder, protected)

    return protected, placeholder_map


def restore_words(text: str, placeholder_map: dict[str, str]) -> str:
    """
    Restaura palavras originais dos placeholders.
    """
    restored = text
    for placeholder, original in placeholder_map.items():
        restored = restored.replace(placeholder, original)
    return restored


def translate_markdown(markdown: str, user_id: int, target_lang: str = "Português") -> str:
    """
    Traduz Markdown protegendo palavras configuradas.
    """
    # Busca palavras não traduzir
    words = get_ignore_words(user_id)

    # Protege palavras
    protected_text, placeholder_map = protect_words(markdown, words)

    # Traduz
    translated = translate_text(protected_text, target_lang)

    # Restaura palavras
    result = restore_words(translated, placeholder_map)

    return result
