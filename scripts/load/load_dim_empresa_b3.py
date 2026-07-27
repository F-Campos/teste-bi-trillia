"""
Script de carga: Dim_Empresa_B3
Etapa: Load
Fonte: files/clean/empresas_bolsa.csv
Destino: files/enrich/dim_empresa_b3.csv

Finaliza a dimensão de empresas listadas na B3: remove colunas
administrativas (id, created_at, updated_at) e a coluna vl_cnpj
(redundante com tx_cnpj), e renomeia tx_cnpj -> cnpj para manter
o nome do campo de ligação consistente com as demais dimensões
do modelo (usado na ponte com Dim_Cadastro_Empresas).
"""

from pathlib import Path
import pandas as pd

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_ORIGEM = RAIZ_PROJETO / "files" / "clean" / "empresas_bolsa.csv"
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "enrich" / "dim_empresa_b3.csv"

COLUNAS_REMOVER = ["id", "vl_cnpj", "created_at", "updated_at"]


def carregar() -> None:
    print("[load] Gerando Dim_Empresa_B3...")

    if not CAMINHO_ORIGEM.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {CAMINHO_ORIGEM}")

    df = pd.read_csv(CAMINHO_ORIGEM, sep=";", encoding="utf-8", dtype={"tx_cnpj": str})

    df = df.drop(columns=COLUNAS_REMOVER)
    df = df.rename(columns={"tx_cnpj": "cnpj"})

    CAMINHO_DESTINO.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CAMINHO_DESTINO, sep=";", encoding="utf-8", index=False)

    print(f"[load] OK: {len(df)} linhas e {len(df.columns)} colunas geradas.")
    print(f"[load] Arquivo salvo em: {CAMINHO_DESTINO}")


if __name__ == "__main__":
    carregar()
