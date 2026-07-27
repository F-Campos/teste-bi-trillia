"""
Script de carga: Dim_Data
Etapa: Load
Fonte: files/clean/cotacoes_bolsa.csv (coluna dt_pregao)
Destino: files/enrich/dim_data.csv

Gera uma dimensão calendário cobrindo do menor ao maior dt_pregao
presente na base de cotações, com atributos padrão de análise
temporal (ano, mês, trimestre, dia da semana).
"""

from pathlib import Path
import pandas as pd

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_COTACOES = RAIZ_PROJETO / "files" / "clean" / "cotacoes_bolsa.csv"
CAMINHO_DESTINO = RAIZ_PROJETO / "files" / "enrich" / "dim_data.csv"

MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
    7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}

DIAS_SEMANA_PT = {
    0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira", 3: "Quinta-feira",
    4: "Sexta-feira", 5: "Sábado", 6: "Domingo",
}


def carregar() -> None:
    print("[load] Gerando Dim_Data...")

    if not CAMINHO_COTACOES.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {CAMINHO_COTACOES}")

    cotacoes = pd.read_csv(CAMINHO_COTACOES, sep=";", encoding="utf-8", parse_dates=["dt_pregao"])
    data_min = cotacoes["dt_pregao"].min()
    data_max = cotacoes["dt_pregao"].max()

    dim_data = pd.DataFrame({"data": pd.date_range(start=data_min, end=data_max, freq="D")})
    dim_data["ano"] = dim_data["data"].dt.year
    dim_data["mes"] = dim_data["data"].dt.month
    dim_data["nm_mes"] = dim_data["mes"].map(MESES_PT)
    dim_data["trimestre"] = dim_data["data"].dt.quarter
    dim_data["dia"] = dim_data["data"].dt.day
    dim_data["dia_semana"] = dim_data["data"].dt.weekday.map(DIAS_SEMANA_PT)
    dim_data["fim_de_semana"] = dim_data["data"].dt.weekday >= 5

    CAMINHO_DESTINO.parent.mkdir(parents=True, exist_ok=True)
    dim_data.to_csv(CAMINHO_DESTINO, sep=";", encoding="utf-8", index=False)

    print(f"[load] OK: {len(dim_data)} linhas geradas ({data_min.date()} a {data_max.date()}).")
    print(f"[load] Arquivo salvo em: {CAMINHO_DESTINO}")


if __name__ == "__main__":
    carregar()
