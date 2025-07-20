# -*- coding: utf-8 -*-
# enforce_schema.py

import pandas as pd
from datetime import datetime
from constants import UNIVERSAL_CSV_SCHEMA

def enforce_schema(df, platform_name):
    df["platform"] = platform_name
    df["scrape_ts"] = datetime.utcnow().isoformat()

    for col in UNIVERSAL_CSV_SCHEMA:
        if col not in df.columns:
            df[col] = None

    df = df[UNIVERSAL_CSV_SCHEMA]
    return df



