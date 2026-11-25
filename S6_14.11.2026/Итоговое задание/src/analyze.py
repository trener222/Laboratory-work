# -*- coding: utf-8 -*-
import pandas as pd

def descriptive_stats(df):
    # Меры центра, разброса и положения для стоимости рейса.
    s = df["cost_rub"]
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    return {"mean": round(s.mean(), 1), "median": round(s.median(), 1),
            "mode": float(s.mode().iloc[0]), "min": float(s.min()), "max": float(s.max()),
            "std": round(s.std(), 2), "q1": float(q1), "q3": float(q3),
            "iqr": float(q3 - q1), "cv_percent": round(s.std() / s.mean() * 100, 2),
            "p90": float(s.quantile(0.90))}

def overall_kpi(df):
    revenue = df["cost_rub"].sum()
    return {"trips": int(len(df)), "revenue_rub": int(revenue),
            "avg_ticket_rub": round(df["cost_rub"].mean(), 1),
            "median_ticket_rub": round(df["cost_rub"].median(), 1),
            "revenue_per_km": round(revenue / df["distance_km"].sum(), 2),
            "revenue_per_ton_km": round(revenue / (df["weight_t"] * df["distance_km"]).sum(), 3),
            "avg_weight_t": round(df["weight_t"].mean(), 2),
            "otd_percent": round((~df["is_delayed"]).mean() * 100, 1),
            "avg_delay_h": round(df["delay_h"].mean(), 2)}

def kpi_by_carrier(df):
    result = df.groupby("carrier").agg(
        trips=("trip_id", "count"), revenue=("cost_rub", "sum"),
        avg_ticket=("cost_rub", "mean"),
        otd=("is_delayed", lambda s: (~s).mean() * 100),
        distance_km=("distance_km", "sum")
    )
    result["rev_per_km"] = result["revenue"] / result["distance_km"]
    return result.drop(columns="distance_km").round(1).sort_values("revenue", ascending=False)

def monthly_kpi(df):
    return df.groupby("month").agg(
        trips=("trip_id", "count"), revenue=("cost_rub", "sum"),
        avg_ticket=("cost_rub", "mean"), avg_weight=("weight_t", "mean"),
        avg_distance=("distance_km", "mean"),
        otd=("is_delayed", lambda s: (~s).mean() * 100)
    ).round(1)
