# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd

def load_trips(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Файл с рейсами не найден: {path}")
    return pd.read_csv(path, parse_dates=["date"])