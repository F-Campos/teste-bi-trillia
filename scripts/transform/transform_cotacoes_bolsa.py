"""
Script de transformação: cotacoes_bolsa
Etapa: Transform
Fonte: files/raw/cotacoes_bolsa.csv
Destino: files/clean/cotacoes_bolsa.csv

Tratamentos aplicados nesta etapa:
1. Converte 'dt_pregao' do formato numérico AAAAMMDD (ex: 20221021)
   para um tipo de data real (AAAA-MM-DD), permitindo uso correto
   em filtros de período, ordenação e relacionamento com Dim_Data.

Observações sobre o dado (não tratadas aqui, por não serem erros):
- 'prazot' possui ~65% de nulos, mas isso é esperado: só se aplica a
  operações a termo, não é problema de qualidade.
- 'tp_merc' contém códigos (10, 70, 80) do padrão B3. A tradução para
  rótulos amigáveis (ex: 'À vista') é responsabilidade da etapa de
  load, ao construir a Dim_Mercado - não é uma limpeza de dado.
"""

from pathlib import Path
import pandas as pd

NOME_BASE = "cotacoes_bolsa"

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_ORIGEM = RAIZ_PROJETO / "files" / "raw" / f"{NOME_BASE}.csv"
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "clean" / f"{NOME_BASE}.csv"


def transformar() -> None:
    print(f"[transform] Iniciando transformação de '{NOME_BASE}'...")

    if not CAMINHO_ORIGEM.exists():
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {CAMINHO_ORIGEM}")

    df = pd.read_csv(CAMINHO_ORIGEM, sep=";", encoding="utf-8")

    linhas_antes = len(df)

    # 1. Converte dt_pregao de AAAAMMDD (int) para data real
    df["dt_pregao"] = pd.to_datetime(df["dt_pregao"], format="%Y%m%d")

    if df["dt_pregao"].isnull().any():
        raise ValueError(
            "Alguma data em 'dt_pregao' não pôde ser convertida. Verifique o formato de origem."
        )

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
