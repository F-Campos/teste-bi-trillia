"""
Script de extração: empresas_saude_tributaria
Etapa: Extract
Fonte: files/spreadsheets/empresas_saude_tributaria.csv
Destino: files/raw/empresas_saude_tributaria.csv

Responsabilidade desta etapa: apenas ler a base original e gravar uma
cópia fiel em files/raw/, validando que o arquivo existe, não está
vazio e possui as colunas esperadas. Nenhuma transformação de dados
acontece aqui - isso é responsabilidade da etapa de transform.
"""

from pathlib import Path
import pandas as pd

NOME_BASE = "empresas_saude_tributaria"

COLUNAS_ESPERADAS = ["cnpj", "saude_tributaria"]

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_ORIGEM = RAIZ_PROJETO / "files" / "spreadsheets" / f"{NOME_BASE}.csv"
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "raw" / f"{NOME_BASE}.csv"


def extrair() -> None:
    print(f"[extract] Iniciando extração de '{NOME_BASE}'...")

    if not CAMINHO_ORIGEM.exists():
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {CAMINHO_ORIGEM}")

    df = pd.read_csv(CAMINHO_ORIGEM, sep=";", encoding="utf-8", dtype={"cnpj": str})

    if df.empty:
        raise ValueError(f"O arquivo '{NOME_BASE}.csv' foi lido, mas está vazio.")

    colunas_faltantes = set(COLUNAS_ESPERADAS) - set(df.columns)
    if colunas_faltantes:
        raise ValueError(
            f"Colunas esperadas não encontradas em '{NOME_BASE}.csv': {colunas_faltantes}"
        )

    CAMINHO_DESTINO.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CAMINHO_DESTINO, sep=";", encoding="utf-8", index=False)

    print(f"[extract] OK: {len(df)} linhas e {len(df.columns)} colunas extraídas.")
    print(f"[extract] Arquivo salvo em: {CAMINHO_DESTINO}")


if __name__ == "__main__":
    extrair()
