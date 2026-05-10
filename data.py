import io

import pandas as pd

SAMPLE_DATA_PATH = "data/sales-data.csv"

REQUIRED_COLUMNS = [
    "date",
    "order_id",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
    "total_amount",
]


def load_data(file_bytes: bytes | None) -> pd.DataFrame:
    if file_bytes is None:
        df = pd.read_csv(SAMPLE_DATA_PATH)
    else:
        df = pd.read_csv(io.BytesIO(file_bytes))

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ("total_amount", "unit_price", "quantity"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def validate_columns(df: pd.DataFrame) -> list[str]:
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]


def compute_kpis(df: pd.DataFrame) -> dict:
    total_sales = float(df["total_amount"].sum(skipna=True))
    total_orders = len(df)
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0.0
    top_category = (
        df.groupby("category")["total_amount"]
        .sum()
        .idxmax()
    )
    return {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
        "top_category": str(top_category),
    }


def aggregate_by_time(df: pd.DataFrame, granularity: str) -> pd.DataFrame:
    valid = df.dropna(subset=["date"]).copy()
    valid = valid.set_index("date")
    resampled = valid["total_amount"].resample(granularity).sum().reset_index()
    resampled.columns = ["period", "sales"]
    return resampled.sort_values("period").reset_index(drop=True)


def aggregate_by_category(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("category")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"total_amount": "total_sales"})
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )
    return result


def aggregate_by_region(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("region")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"total_amount": "total_sales"})
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )
    return result
