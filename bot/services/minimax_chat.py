import os
import httpx


MINIMAX_API_KEY=os.getenv("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat")


def translate_text(text: str, target_lang: str = "Português") -> str:
    """
    Traduz texto usando MiniMax M2.7.
    """
    if not MINIMAX_API_KEY:
        raise ValueError("MINIMAX_API_KEY não configurado")

    prompt = (
        f"Traduza o seguinte texto para {target_lang}. "
        "Mantenha a formatação Markdown (headings, listas, tabelas, código). "
        "Não traduza nomes próprios, nomes de personagens ou termos técnicos quando apropriado.\n\n"
        f"TEXTO:\n{text}"
    )

    payload = {
        "model": "MiniMax-M2.7",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 8192,
    }

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json",
    }

    with httpx.Client(timeout=120) as client:
        resp = client.post(
            f"{MINIMAX_BASE_URL}/v1/text/chatcompletion_v2",
            headers=headers,
            json=payload
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
