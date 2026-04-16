import json

def carregar_dados():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)
