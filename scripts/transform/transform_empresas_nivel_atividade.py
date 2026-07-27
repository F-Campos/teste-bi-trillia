"""
Script de transformação: empresas_nivel_atividade
Etapa: Transform
Fonte: files/raw/empresas_nivel_atividade.csv
Destino: files/clean/empresas_nivel_atividade.csv

Tratamentos aplicados nesta etapa:
1. Mantém 'cnpj' como texto, preservando os zeros à esquerda.
2. Preenche os nulos (1.173 linhas, ~10%) em 'nivel_atividade' com
   'NÃO INFORMADO', evitando categoria em branco nos filtros do
   Power BI.
3. Remove espaços em branco extras da coluna de nível de atividade.
"""

from pathlib import Path
import pandas as pd

NOME_BASE = "empresas_nivel_atividade"

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_ORIGEM = RAIZ_PROJETO / "files" / "raw" / f"{NOME_BASE}.csv"
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "clean" / f"{NOME_BASE}.csv"


def transformar() -> None:
    print(f"[transform] Iniciando transformação de '{NOME_BASE}'...")

    if not CAMINHO_ORIGEM.exists():
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {CAMINHO_ORIGEM}")

    df = pd.read_csv(CAMINHO_ORIGEM, sep=";", encoding="utf-8", dtype={"cnpj": str})

    linhas_antes = len(df)

    df["nivel_atividade"] = df["nivel_atividade"].astype(str).str.strip()
    df["nivel_atividade"] = df["nivel_atividade"].replace("nan", "NÃO INFORMADO")

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
