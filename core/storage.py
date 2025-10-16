# core/storage.py
import json
import os

def save_json_to_path(data: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json_from_path(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)