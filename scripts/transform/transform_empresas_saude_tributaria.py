"""
Script de transformação: empresas_saude_tributaria
Etapa: Transform
Fonte: files/raw/empresas_saude_tributaria.csv
Destino: files/clean/empresas_saude_tributaria.csv

Tratamentos aplicados nesta etapa:
1. Mantém 'cnpj' como texto, preservando os zeros à esquerda.
2. Preenche os nulos (4.314 linhas, ~36%) em 'saude_tributaria' com
   'NÃO INFORMADO', evitando categoria em branco nos filtros do
   Power BI.
3. Remove espaços em branco extras da coluna de saúde tributária.
"""

from pathlib import Path
import pandas as pd

NOME_BASE = "empresas_saude_tributaria"

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_ORIGEM = RAIZ_PROJETO / "files" / "raw" / f"{NOME_BASE}.csv"
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "clean" / f"{NOME_BASE}.csv"


def transformar() -> None:
    print(f"[transform] Iniciando transformação de '{NOME_BASE}'...")

    if not CAMINHO_ORIGEM.exists():
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {CAMINHO_ORIGEM}")

    df = pd.read_csv(CAMINHO_ORIGEM, sep=";", encoding="utf-8", dtype={"cnpj": str})

    linhas_antes = len(df)

    df["saude_tributaria"] = df["saude_tributaria"].astype(str).str.strip()
    df["saude_tributaria"] = df["saude_tributaria"].replace("nan", "NÃO INFORMADO")

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
