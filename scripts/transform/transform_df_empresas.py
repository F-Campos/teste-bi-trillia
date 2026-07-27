"""
Script de transformação: df_empresas
Etapa: Transform
Fonte: files/raw/df_empresas.csv
Destino: files/clean/df_empresas.csv

Tratamentos aplicados nesta etapa:
1. Mantém 'cnpj', 'cd_cnae_principal' e 'endereco_cep' como texto,
   preservando os zeros à esquerda (essas colunas são identificadores,
   não quantidades - nunca devem virar número).
2. Converte 'dt_abertura' para tipo de data real.
3. Preenche os poucos nulos (9 linhas) em 'cd_cnae_principal',
   'de_ramo_atividade' e 'de_setor' com 'NÃO INFORMADO', evitando
   categorias em branco nos filtros e gráficos do Power BI.
4. Remove espaços em branco extras de colunas de texto.
"""

from pathlib import Path
import pandas as pd

NOME_BASE = "df_empresas"

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_ORIGEM = RAIZ_PROJETO / "files" / "raw" / f"{NOME_BASE}.csv"
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "clean" / f"{NOME_BASE}.csv"

COLUNAS_TEXTO_ID = ["cnpj", "cd_cnae_principal", "endereco_cep"]

COLUNAS_TEXTO_LIVRE = [
    "de_cnae_principal", "de_ramo_atividade", "de_setor",
    "endereco_municipio", "endereco_uf", "endereco_regiao",
    "endereco_mesorregiao", "situacao_cadastral",
]

COLUNAS_PARA_PREENCHER = ["cd_cnae_principal", "de_ramo_atividade", "de_setor"]


def transformar() -> None:
    print(f"[transform] Iniciando transformação de '{NOME_BASE}'...")

    if not CAMINHO_ORIGEM.exists():
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {CAMINHO_ORIGEM}")

    dtype_colunas_id = {coluna: str for coluna in COLUNAS_TEXTO_ID}
    df = pd.read_csv(CAMINHO_ORIGEM, sep=";", encoding="utf-8", dtype=dtype_colunas_id)

    linhas_antes = len(df)

    # 1. Converte dt_abertura para data real
    df["dt_abertura"] = pd.to_datetime(df["dt_abertura"], format="%Y-%m-%d")

    # 2. Remove espaços extras das colunas de texto livre
    for coluna in COLUNAS_TEXTO_LIVRE:
        df[coluna] = df[coluna].astype(str).str.strip()

    # 3. Preenche nulos de classificação com "NÃO INFORMADO"
    for coluna in COLUNAS_PARA_PREENCHER:
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
