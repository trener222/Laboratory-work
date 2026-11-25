# -*- coding: utf-8 -*-
import pandas as pd

def prepare_trips(df):
    result = df.copy()
    result = result.drop_duplicates(subset=["trip_id"]).copy()
    numeric_cols = ["weight_t", "distance_km", "duration_h", "cost_rub", "delay_h"]
    for col in numeric_cols:
        result[col] = pd.to_numeric(result[col], errors="coerce")
    result = result.dropna(subset=["date", "weight_t", "distance_km", "cost_rub", "delay_h"])
    result = result[(result["weight_t"] > 0) & (result["distance_km"] > 0) & (result["cost_rub"] > 0)]
    result["month"] = result["date"].dt.to_period("M").astype(str)
    result["is_delayed"] = result["delay_h"] > 0
    result["cost_per_km"] = (result["cost_rub"] / result["distance_km"]).round(2)
    return result.reset_index(drop=True)
