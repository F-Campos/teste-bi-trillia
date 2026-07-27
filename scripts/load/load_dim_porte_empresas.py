"""
Script de carga: Dim_Porte_Empresas
Etapa: Load
Fonte: files/clean/empresas_porte.csv
Destino: files/enrich/dim_porte_empresas.csv

Esta base já está no formato final após o transform; o load aqui
apenas formaliza o nome do arquivo de saída dentro do modelo
dimensional (Bloco 2 - populações independentes de empresas).
"""

from pathlib import Path
import pandas as pd

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_ORIGEM = RAIZ_PROJETO / "files" / "clean" / "empresas_porte.csv"
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "enrich" / "dim_porte_empresas.csv"


def carregar() -> None:
    print("[load] Gerando Dim_Porte_Empresas...")

    if not CAMINHO_ORIGEM.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {CAMINHO_ORIGEM}")

    df = pd.read_csv(CAMINHO_ORIGEM, sep=";", encoding="utf-8", dtype={"cnpj": str})

    CAMINHO_DESTINO.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CAMINHO_DESTINO, sep=";", encoding="utf-8", index=False)

    print(f"[load] OK: {len(df)} linhas e {len(df.columns)} colunas geradas.")
    print(f"[load] Arquivo salvo em: {CAMINHO_DESTINO}")


if __name__ == "__main__":
    carregar()
