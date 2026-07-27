"""
Script de carga: Fato_Cotacoes
Etapa: Load
Fonte: files/clean/cotacoes_bolsa.csv
Destino: files/enrich/fato_cotacoes.csv

Mantém apenas as chaves de ligação com as dimensões do modelo
(cd_acao_rdz -> Dim_Empresa_B3, dt_pregao -> Dim_Data,
tp_merc -> Dim_Mercado) e as métricas numéricas de negociação.
Colunas administrativas e redundantes com as dimensões (id, tp_reg,
cd_bdi, nm_empresa_rdz, especi, moeda_ref, cd_isin, created_at,
updated_at, entre outras) são descartadas nesta etapa.
"""

from pathlib import Path
import pandas as pd

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_ORIGEM = RAIZ_PROJETO / "files" / "clean" / "cotacoes_bolsa.csv"
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "enrich" / "fato_cotacoes.csv"

COLUNAS_FATO = [
    "cd_acao_rdz", "dt_pregao", "tp_merc",
    "vl_abertura", "vl_maximo", "vl_minimo", "vl_medio", "vl_fechamento",
    "vl_mlh_oft_compra", "vl_mlh_oft_venda", "vl_ttl_neg", "qt_tit_neg",
    "vl_volume",
]


def carregar() -> None:
    print("[load] Gerando Fato_Cotacoes...")

    if not CAMINHO_ORIGEM.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {CAMINHO_ORIGEM}")

    df = pd.read_csv(CAMINHO_ORIGEM, sep=";", encoding="utf-8", parse_dates=["dt_pregao"])
    df = df[COLUNAS_FATO]

    CAMINHO_DESTINO.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CAMINHO_DESTINO, sep=";", encoding="utf-8", index=False)

    print(f"[load] OK: {len(df)} linhas e {len(df.columns)} colunas geradas.")
    print(f"[load] Arquivo salvo em: {CAMINHO_DESTINO}")


if __name__ == "__main__":
    carregar()
