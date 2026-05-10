import pytest
import pandas as pd
import data


FIXTURE_PATH = "tests/fixtures/sample.csv"
FIXTURE_ROWS = 20


@pytest.fixture
def sample_df(monkeypatch):
    monkeypatch.setattr(data, "SAMPLE_DATA_PATH", FIXTURE_PATH)
    return data.load_data(None)


# T022
def test_load_data_from_path(sample_df):
    assert len(sample_df) == FIXTURE_ROWS
    assert list(data.REQUIRED_COLUMNS) == [
        "date", "order_id", "product", "category",
        "region", "quantity", "unit_price", "total_amount",
    ]
    for col in data.REQUIRED_COLUMNS:
        assert col in sample_df.columns
    assert pd.api.types.is_datetime64_any_dtype(sample_df["date"])


# T023
def test_validate_columns_pass(sample_df):
    assert data.validate_columns(sample_df) == []


# T024
def test_validate_columns_fail(sample_df):
    df_missing = sample_df.drop(columns=["total_amount"])
    assert data.validate_columns(df_missing) == ["total_amount"]


# T025
def test_compute_kpis(sample_df):
    kpis = data.compute_kpis(sample_df)
    assert kpis["total_orders"] == FIXTURE_ROWS
    assert kpis["total_sales"] > 0
    assert abs(kpis["avg_order_value"] - kpis["total_sales"] / FIXTURE_ROWS) < 0.01
    assert isinstance(kpis["top_category"], str)
    assert len(kpis["top_category"]) > 0


# T026
def test_aggregate_by_time_monthly(sample_df):
    result = data.aggregate_by_time(sample_df, "ME")
    assert list(result.columns) == ["period", "sales"]
    # resample fills all calendar months in range (including zero-sales gaps)
    assert all(result["sales"] >= 0)
    assert result["sales"].sum() > 0
    assert result["period"].is_monotonic_increasing


# T027
def test_aggregate_by_time_daily(sample_df):
    result = data.aggregate_by_time(sample_df, "D")
    assert list(result.columns) == ["period", "sales"]
    # resample fills every calendar day in range, not just transaction days
    assert result["sales"].sum() > 0
    assert result["period"].is_monotonic_increasing
    assert len(result) >= sample_df["date"].dropna().dt.normalize().nunique()


# T028
def test_aggregate_by_category(sample_df):
    result = data.aggregate_by_category(sample_df)
    assert list(result.columns) == ["category", "total_sales"]
    sales = result["total_sales"].tolist()
    assert sales == sorted(sales, reverse=True)
    expected = {"Electronics", "Accessories", "Audio", "Wearables", "Smart Home"}
    assert expected.issubset(set(result["category"]))


# T029
def test_aggregate_by_region(sample_df):
    result = data.aggregate_by_region(sample_df)
    assert list(result.columns) == ["region", "total_sales"]
    sales = result["total_sales"].tolist()
    assert sales == sorted(sales, reverse=True)
    expected = {"North", "South", "East", "West"}
    assert expected.issubset(set(result["region"]))
