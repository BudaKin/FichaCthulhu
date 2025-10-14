# core/storage.py
import json
import os

def save_json_to_path(data: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json_from_path(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def export_text_to_path(data: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write("Ficha de Personagem\n")
        f.write("="*40 + "\n\n")
        f.write("[Identificação]\n")
        for k, v in data["header"].items():
            f.write(f"{k}: {v}\n")
        f.write("\n[Atributos]\n")
        for k, v in data["attributes"].items():
            f.write(f"{k}: {v}\n")
        f.write("\n[Status]\n")
        for k, v in data["status"].items():
            f.write(f"{k}: {v}\n")
        f.write("\n[Perícias]\n")
        for k, v in data["skills"].items():
            f.write(f"{k}: {v}\n")
        f.write("\n[Outras Línguas]\n")
        for l in data["languages"]:
            f.write(f"{l.get('nome','')}: {l.get('valor','')}\n")
        f.write("\n[Habilidades]\n" + data["habilidades"] + "\n")
        f.write("\n[Rituais]\n" + data["rituals"] + "\n")
        f.write("\n[Equipamento]\n" + data["equipment"] + "\n")
        f.write("\n[Vantagens/Complicações]\n" + data["advantages"] + "\n")
        f.write("\n[Backstory]\n" + data["backstory"] + "\n")