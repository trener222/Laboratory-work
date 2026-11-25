# -*- coding: utf-8 -*-
import json
from pathlib import Path
import pandas as pd
import config
from src.load import load_trips
from src.prepare import prepare_trips
from src.analyze import descriptive_stats, overall_kpi, kpi_by_carrier, monthly_kpi

def df_to_markdown(df):
    '''Превращает таблицу в markdown без внешних зависимостей.'''
    header = "| " + " | ".join(str(c) for c in df.columns) + " |"
    sep = "|" + "---|" * len(df.columns)
    rows = ["| " + " | ".join(str(v) for v in row) + " |"
            for row in df.itertuples(index=False)]
    return chr(10).join([header, sep] + rows)

def main():
    Path(config.PROCESSED_DIR).mkdir(parents=True, exist_ok=True)
    Path(config.REPORTS_DIR).mkdir(parents=True, exist_ok=True)
    raw = load_trips(config.RAW_FILE)
    clean = prepare_trips(raw)
    clean.to_csv(Path(config.PROCESSED_DIR) / "trips_clean.csv", index=False, encoding="utf-8")
    stats = descriptive_stats(clean)
    kpi = overall_kpi(clean)
    carrier = kpi_by_carrier(clean)
    month = monthly_kpi(clean)
    pd.DataFrame([stats]).to_csv(Path(config.PROCESSED_DIR) / "descriptive_stats.csv", index=False)
    carrier.to_csv(Path(config.PROCESSED_DIR) / "kpi_by_carrier.csv", encoding="utf-8")
    month.to_csv(Path(config.PROCESSED_DIR) / "kpi_by_month.csv", encoding="utf-8")
    df = clean.copy()
    df["cost_group"] = pd.cut(df["cost_rub"], bins=config.COST_GROUP_BINS, labels=config.COST_GROUP_LABELS)
    freq = df.groupby("cost_group", observed=True).agg(trips=("trip_id", "count"), revenue=("cost_rub", "sum"))
    freq["trip_share_percent"] = (freq["trips"] / len(df) * 100).round(1)
    freq["revenue_share_percent"] = (freq["revenue"] / df["cost_rub"].sum() * 100).round(1)
    freq.to_csv(Path(config.PROCESSED_DIR) / "cost_frequency.csv", encoding="utf-8")
    
    lines = ["# Отчёт по анализу перевозок практика 10", "", "## Описательная статистика стоимости рейса"]
    lines += [f"- {key}: {value}" for key, value in stats.items()]
    lines += ["", "## Общие KPI"] + [f"- {key}: {value}" for key, value in kpi.items()]
  
    lines += ["", "## KPI по перевозчикам", df_to_markdown(carrier.reset_index())]
    lines += ["", "## KPI по месяцам", df_to_markdown(month.reset_index())]
    lines += ["", "## Распределение стоимости", df_to_markdown(freq.reset_index())]
    
    lines += ["", "## Вывод", "Стоимость рейсов имеет заметный разброс; для типичного уровня стоимости следует смотреть на медиану вместе со средним. OTD показывает долю рейсов без задержек. Таблицы по перевозчикам и месяцам позволяют сравнивать выручку, средний чек и своевременность доставки."]
    report_path = Path(config.REPORTS_DIR) / "report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    manifest = {"trips": len(clean), "kpi": kpi, "source_file": config.RAW_FILE,
                "source_file_size": Path(config.RAW_FILE).stat().st_size}
    (Path(config.PROCESSED_DIR) / "run_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Pipeline завершён. Рейсов:", len(clean))
    print("Отчёт:", report_path)
    print("KPI:", kpi)
    return manifest


if __name__ == "__main__":
    main()