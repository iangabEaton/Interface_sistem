# utils.py
import json
from pathlib import Path

DATA_FILE = Path("dados_cotacao.json")

def salvar_dados(dados):
    """Salva os dados em arquivo JSON"""
    try:
        existentes = carregar_dados()
        existentes.update(dados)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(existentes, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return False

def carregar_dados():
    """Carrega os dados do arquivo JSON"""
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar: {e}")
    return {}

def limpar_dados():
    """Limpa todos os dados salvos"""
    if DATA_FILE.exists():
        DATA_FILE.unlink()
