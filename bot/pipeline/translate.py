from bot.services.translation import translate_markdown


def translate_pipeline(markdown: str, user_id: int, target_lang: str = "Português") -> str:
    """
    Pipeline de tradução: usa lista de palavras do usuário.
    """
    return translate_markdown(markdown, user_id, target_lang)
