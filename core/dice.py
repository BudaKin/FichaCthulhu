# core/dice.py
import re
import random

def eval_dice_expression(expr: str):
    """
    Avalia expressões tipo '2d6+3' ou '1d20-1+2'.
    Retorna (valor_integer, detalhes_string).
    """
    clean = expr.replace(' ', '')
    rolls_detail = []
    expr2 = clean

    # Encontrar todos os grupos NdS
    for m in re.finditer(r"(\d*)d(\d+)", clean):
        full = m.group(0)
        n = int(m.group(1)) if m.group(1) else 1
        s = int(m.group(2))
        rolls = [random.randint(1, s) for _ in range(n)]
        total = sum(rolls)
        rolls_detail.append(f"{full}={rolls}")
        # substitui apenas a primeira ocorrência para evitar conflitos com nomes iguais
        expr2 = expr2.replace(full, str(total), 1)

    # Avalia a expressão resultante com segurança minima (sem builtins)
    try:
        val = eval(expr2, {'__builtins__': None}, {})
    except Exception as e:
        raise ValueError(f"Erro ao avaliar expressão: {e}")

    details = '; '.join(rolls_detail) if rolls_detail else 'sem dados'
    return int(val), details

def parse_and_roll(expr: str):
    v, d = eval_dice_expression(expr)
    return v, d, expr