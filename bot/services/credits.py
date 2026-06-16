import os
from bot.db import get_user, update_credits, add_transaction


LUA_USER_ID = int(os.getenv("LUA_USER_ID", "0"))  # Substituir pelo ID real da Lua


def get_user_info(user_id: int) -> dict:
    user = get_user(user_id)
    if not user:
        return None
    return {
        "credits": user["credits"],
        "plan_type": user["plan_type"],
        "plan_expires": user["plan_expires"],
        "default_language": user.get("default_language", "pt-BR"),
    }


def check_credits(user_id: int, needed: int) -> bool:
    if user_id == LUA_USER_ID:
        return True  # Lua sempre tem créditos
    user = get_user(user_id)
    if not user:
        return False
    return user["credits"] >= needed


def descontar_creditos(user_id: int, amount: int) -> bool:
    """
    Desconta créditos. Retorna True se bem-sucedido.
    """
    if user_id == LUA_USER_ID:
        return True  # Lua não paga

    user = get_user(user_id)
    if not user or user["credits"] < amount:
        return False

    new_credits = user["credits"] - amount
    update_credits(user_id, new_credits)
    add_transaction(user_id, "convert" if amount == 1 else "translate", amount)
    return True


def reset_credits_lua():
    """Reseta créditos da Lua para 1000."""
    if LUA_USER_ID:
        update_credits(LUA_USER_ID, 1000)
