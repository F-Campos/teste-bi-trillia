"""
Script de transformação: empresas_porte
Etapa: Transform
Fonte: files/raw/empresas_porte.csv
Destino: files/clean/empresas_porte.csv

Tratamentos aplicados nesta etapa:
1. Mantém 'cnpj' como texto, preservando os zeros à esquerda.
2. Remove espaços em branco extras da coluna de porte.

Observação: esta base não possui nulos nem duplicatas na origem,
portanto não há tratamento de preenchimento nesta etapa.
"""

from pathlib import Path
import pandas as pd

NOME_BASE = "empresas_porte"

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_ORIGEM = RAIZ_PROJETO / "files" / "raw" / f"{NOME_BASE}.csv"
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "clean" / f"{NOME_BASE}.csv"


def transformar() -> None:
    print(f"[transform] Iniciando transformação de '{NOME_BASE}'...")

    if not CAMINHO_ORIGEM.exists():
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {CAMINHO_ORIGEM}")

    df = pd.read_csv(CAMINHO_ORIGEM, sep=";", encoding="utf-8", dtype={"cnpj": str})

    linhas_antes = len(df)

    df["empresa_porte"] = df["empresa_porte"].astype(str).str.strip()

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
