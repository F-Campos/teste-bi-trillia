"""
Script de transformação: empresas_bolsa
Etapa: Transform
Fonte: files/raw/empresas_bolsa.csv
Destino: files/clean/empresas_bolsa.csv

Tratamentos aplicados nesta etapa:
1. Padroniza o CNPJ (tx_cnpj) como texto com 14 dígitos, preservando
   zeros à esquerda (evita perda de precisão que ocorreria se fosse
   tratado como número).
2. Corrige inconsistência de digitação em 'setor_economico': o valor
   'PETRÓLEO. GÁS E BIOCOMBUSTÍVEIS' (com ponto, erro de digitação)
   é unificado com 'PETRÓLEO, GÁS E BIOCOMBUSTÍVEIS' (com vírgula).
3. Remove a coluna 'nm_segmento_b3', que está 100% nula na base
   original e não agrega valor ao modelo.
4. Remove espaços em branco extras (strip) de colunas de texto.
"""

from pathlib import Path
import pandas as pd

NOME_BASE = "empresas_bolsa"

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_ORIGEM = RAIZ_PROJETO / "files" / "raw" / f"{NOME_BASE}.csv"
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "clean" / f"{NOME_BASE}.csv"

COLUNAS_TEXTO = [
    "nm_empresa", "setor_economico", "subsetor", "segmento",
    "segmento_b3", "cd_acao_rdz",
]

# Mapa de correção de inconsistências conhecidas em setor_economico
CORRECOES_SETOR = {
    "PETRÓLEO. GÁS E BIOCOMBUSTÍVEIS": "PETRÓLEO, GÁS E BIOCOMBUSTÍVEIS",
}


def transformar() -> None:
    print(f"[transform] Iniciando transformação de '{NOME_BASE}'...")

    if not CAMINHO_ORIGEM.exists():
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {CAMINHO_ORIGEM}")

    df = pd.read_csv(CAMINHO_ORIGEM, sep=";", encoding="utf-8", dtype={"tx_cnpj": str})

    linhas_antes = len(df)

    # 1. CNPJ como texto, 14 dígitos, zeros à esquerda preservados
    df["tx_cnpj"] = df["tx_cnpj"].str.zfill(14)
    df.loc[df["tx_cnpj"] == "0" * 14, "tx_cnpj"] = pd.NA  # linhas sem CNPJ original

    # 2. Remove espaços extras das colunas de texto
    for coluna in COLUNAS_TEXTO:
        df[coluna] = df[coluna].astype(str).str.strip()

    # 3. Corrige inconsistência de digitação em setor_economico
    df["setor_economico"] = df["setor_economico"].replace(CORRECOES_SETOR)

    # 4. Remove coluna 100% nula
    if "nm_segmento_b3" in df.columns:
        df = df.drop(columns=["nm_segmento_b3"])

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
