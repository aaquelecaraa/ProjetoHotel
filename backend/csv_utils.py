import csv
from pathlib import Path

# Pasta base onde os CSVs ficarão (raiz do projeto)
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_DIR = BASE_DIR / "csv_data"

# Garante que a pasta exista
CSV_DIR.mkdir(exist_ok=True)


def salvar_clientes_csv(clientes: list, nome_arquivo: str = "clientes.csv"):
    """
    Recebe uma lista de dicionários ou objetos Cliente com to_dict()
    e salva em um arquivo CSV.
    """
    caminho = CSV_DIR / nome_arquivo

    # Se a lista estiver vazia, não faz nada
    if not clientes:
        return

    # Garante que cada item seja um dicionário
    if hasattr(clientes[0], "to_dict"):
        clientes = [c.to_dict() for c in clientes]

    campos = ["id", "nome", "telefone", "email"]

    with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(clientes)


def salvar_quartos_csv(quartos: list, nome_arquivo: str = "quartos.csv"):
    """
    Recebe uma lista de dicionários ou objetos Quarto com to_dict()
    e salva em um arquivo CSV.
    """
    caminho = CSV_DIR / nome_arquivo

    if not quartos:
        return

    if hasattr(quartos[0], "to_dict"):
        quartos = [q.to_dict() for q in quartos]

    campos = ["id", "numero", "tipo", "preco_diaria", "status"]

    with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(quartos)


def salvar_reservas_csv(reservas: list, nome_arquivo: str = "reservas.csv"):
    """
    Recebe uma lista de dicionários ou objetos Reserva com to_dict()
    e salva em um arquivo CSV.
    """
    caminho = CSV_DIR / nome_arquivo

    if not reservas:
        return

    if hasattr(reservas[0], "to_dict"):
        reservas = [r.to_dict() for r in reservas]

    campos = ["id", "cliente_id", "quarto_id", "data_checkin", "data_checkout", "status"]

    with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(reservas)


def ler_csv(nome_arquivo: str) -> list:
    """
    Lê um arquivo CSV (se existir) e retorna uma lista de dicionários.
    Caso o arquivo não exista, retorna lista vazia.
    """
    caminho = CSV_DIR / nome_arquivo

    if not caminho.exists():
        return []

    with open(caminho, mode="r", newline="", encoding="utf-8") as arquivo:
        reader = csv.DictReader(arquivo)
        return list(reader)