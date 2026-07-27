"""
Script de transformação: empresas_simples
Etapa: Transform
Fonte: files/raw/empresas_simples.csv
Destino: files/clean/empresas_simples.csv

Tratamentos aplicados nesta etapa:
1. Mantém 'cnpj' como texto, preservando os zeros à esquerda.
2. Converte 'optante_simples' e 'optante_simei' de booleano
   (True/False) para texto categórico ('SIM'/'NÃO'), preenchendo
   os 640 nulos de cada coluna com 'NÃO INFORMADO'. Isso torna as
   colunas mais amigáveis como segmentação (slicer) no Power BI do
   que um booleano puro, e evita blank nos filtros.
"""

from pathlib import Path
import pandas as pd

NOME_BASE = "empresas_simples"

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_ORIGEM = RAIZ_PROJETO / "files" / "raw" / f"{NOME_BASE}.csv"
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "clean" / f"{NOME_BASE}.csv"

COLUNAS_BOOLEANAS = ["optante_simples", "optante_simei"]

MAPA_BOOLEANO = {True: "SIM", False: "NÃO"}


def transformar() -> None:
    print(f"[transform] Iniciando transformação de '{NOME_BASE}'...")

    if not CAMINHO_ORIGEM.exists():
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {CAMINHO_ORIGEM}")

    df = pd.read_csv(CAMINHO_ORIGEM, sep=";", encoding="utf-8", dtype={"cnpj": str})

    linhas_antes = len(df)

    for coluna in COLUNAS_BOOLEANAS:
        df[coluna] = df[coluna].map(MAPA_BOOLEANO)
        df[coluna] = df[coluna].fillna("NÃO INFORMADO")

    if len(df) != linhas_antes:
        raise ValueError(
            f"Número de linhas mudou durante o transform "
            f"({linhas_antes} -> {len(df)}), isso não deveria acontecer nesta etapa."
        )

    CAMINHO_DESTINO.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CAMINHO_DESTINO, sep=";", encoding="utf-8", index=False)

    print(f"[transform] OK: {len(df)} linhas e {len(df.columns)} colunas tratadas.")
    print(f"[transform] Arquivo salvo em: {CAMINHO_DESTINO}")


if __name__ == "__main__":
    transformar()
