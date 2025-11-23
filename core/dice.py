# core/dice.py
import re
import random

# ===============================
#   REGRAS ESPECIAIS (d100 / 2d12)
# ===============================

# Atributos que SEMPRE usam d100
D100_ATTRIBUTES = ["Educação", "Sanidade", "Saber", "Sorte", "Ideia"]


# -------------------------------
#   ROLAGEM d100 ESPECIAL
# -------------------------------
def roll_d100_check(valor):
    """
    Rola 1d100 e aplica as regras:
    extremo, bom, normal, ruim, péssimo, desastre.
    """
    r = random.randint(1, 100)

    if r == 100 or r > valor * 4:
        resultado = "Desastre"
    elif r > valor * 2:
        resultado = "Péssimo"
    elif r > valor:
        resultado = "Ruim"
    elif r == 1 or r < max(1, valor // 4):
        resultado = "Extremo"
    elif r <= valor // 2:
        resultado = "Bom"
    else:
        resultado = "Normal"

    detalhes = f"d100 = {r} → {resultado}"
    return r, resultado, detalhes


# -------------------------------
#   ROLAGEM 2d12 ESPECIAL
# -------------------------------
def roll_2d12_check(valor):
    """
    Rola 2d12 e aplica as regras especiais:
    extremo, bom, normal, ruim, péssimo, desastre.
    """
    d1 = random.randint(1, 12)
    d2 = random.randint(1, 12)
    soma = d1 + d2

    # ---- CLASSIFICAÇÃO ----
    if (d1 == d2 and soma > valor) or (d1 == 12 and d2 == 12):
        resultado = "Desastre"
    elif d1 < d2 and soma > valor:
        resultado = "Péssimo"
    elif d1 > d2 and soma > valor:
        resultado = "Ruim"
    elif d1 < d2 and soma <= valor:
        resultado = "Normal"
    elif d1 > d2 and soma <= valor:
        resultado = "Bom"
    elif (d1 == d2 and soma <= valor) or (d1 == 1 and d2 == 1):
        resultado = "Extremo"
    else:
        resultado = "Indefinido"

    detalhes = f"2d12 = [{d1}, {d2}], soma={soma} → {resultado}"
    return d1, d2, soma, resultado, detalhes


# -------------------------------
#   FUNÇÃO PRINCIPAL DE ROLAGEM
# -------------------------------
def roll_stat_or_skill(nome: str, valor: int):
    """
    Decide automaticamente qual sistema usar:
      - d100 para atributos especiais
      - 2d12 para o resto

    Retorna:
      - rolls (lista com 1 ou 2 valores)
      - total
      - resultado textual ("Bom", "Ruim", etc.)
      - detalhes formatados
      - tipo ("d100" ou "2d12")
    """
    if nome in D100_ATTRIBUTES:
        total, resultado, detalhes = roll_d100_check(valor)
        return [total], total, resultado, detalhes, "d100"

    else:
        d1, d2, soma, resultado, detalhes = roll_2d12_check(valor)
        return [d1, d2], soma, resultado, detalhes, "2d12"


# ============================================
#   (CÓDIGO ORIGINAL PERMANECE INALTERADO)
# ============================================

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
        expr2 = expr2.replace(full, str(total), 1)

    # Avalia expressão resultante
    try:
        val = eval(expr2, {'__builtins__': None}, {})
    except Exception as e:
        raise ValueError(f"Erro ao avaliar expressão: {e}")

    details = '; '.join(rolls_detail) if rolls_detail else 'sem dados'
    return int(val), details


def parse_and_roll(expr: str):
    v, d = eval_dice_expression(expr)
    return v, d, expr
