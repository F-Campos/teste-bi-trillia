
"""
Script de carga: Dim_Mercado
Etapa: Load
Fonte: tabela oficial "TPMERC" do layout de Cotações Históricas da B3
       (https://www.b3.com.br/data/files/33/67/B9/50/D84057102C784E47AC094EA8/SeriesHistoricas_Layout.pdf)
Destino: files/enrich/dim_mercado.csv

Esta dimensão não deriva de nenhuma das 7 bases fornecidas - ela
traduz os códigos numéricos de 'tp_merc' (presentes em
files/clean/cotacoes_bolsa.csv) para rótulos legíveis, usando a
tabela oficial publicada pela própria B3. Os únicos códigos que
aparecem no dado fornecido são 10, 70 e 80.
"""

from pathlib import Path
import pandas as pd

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "enrich" / "dim_mercado.csv"

# Tabela oficial TPMERC da B3 (apenas os códigos presentes no dado fornecido)
DIM_MERCADO = pd.DataFrame([
    {"tp_merc": 10, "ds_mercado": "À Vista"},
    {"tp_merc": 70, "ds_mercado": "Opções de Compra"},
    {"tp_merc": 80, "ds_mercado": "Opções de Venda"},
])


def carregar() -> None:
    print("[load] Gerando Dim_Mercado...")

    CAMINHO_DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DIM_MERCADO.to_csv(CAMINHO_DESTINO, sep=";", encoding="utf-8", index=False)

    print(f"[load] OK: {len(DIM_MERCADO)} linhas geradas.")
    print(f"[load] Arquivo salvo em: {CAMINHO_DESTINO}")


if __name__ == "__main__":
    carregar()
    