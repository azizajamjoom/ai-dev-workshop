# Contract: data.py Public Interface

**Module**: `data.py` (project root)
**Consumer**: `app.py` (Streamlit UI layer)
**Date**: 2026-05-09

This contract defines every function that `app.py` may call. `data.py` MUST NOT import
`streamlit` — it is a pure data layer. All display logic stays in `app.py`.

---

## Constants

```python
REQUIRED_COLUMNS: list[str]
# ["date", "order_id", "product", "category", "region",
#  "quantity", "unit_price", "total_amount"]

SAMPLE_DATA_PATH: str
# Relative path to the bundled sample dataset: "data/sales-data.csv"
```

---

## Functions

### `load_data`

```python
def load_data(file_bytes: bytes | None) -> pd.DataFrame
```

**Purpose**: Load and minimally clean a CSV dataset.

| Parameter    | Type           | Description                                          |
|--------------|----------------|------------------------------------------------------|
| `file_bytes` | `bytes \| None` | Raw bytes from an uploaded file, or `None` to load the sample dataset |

**Returns**: `pd.DataFrame` with `date` column parsed as `datetime64`.

**Behaviour**:
- If `file_bytes` is `None`, reads `SAMPLE_DATA_PATH`.
- If `file_bytes` is provided, reads from `io.BytesIO(file_bytes)`.
- Parses `date` column with `pd.to_datetime(..., errors="coerce")`.
- Coerces `total_amount`, `unit_price`, `quantity` to numeric with `errors="coerce"`.
- Does **not** drop invalid rows — that is the caller's responsibility after validation.

**Decorated with**: `@st.cache_data` in `app.py` wrapping call, OR applied directly
in `data.py` — implementation choice, but caching MUST be present.

---

### `validate_columns`

```python
def validate_columns(df: pd.DataFrame) -> list[str]
```

**Purpose**: Check that all required columns are present.

**Returns**: List of missing column names. Empty list means the DataFrame is valid.

**Behaviour**: Compares `df.columns` against `REQUIRED_COLUMNS`. Case-sensitive.

---

### `compute_kpis`

```python
def compute_kpis(df: pd.DataFrame) -> dict[str, float | int | str]
```

**Purpose**: Compute the four summary KPIs.

**Returns**:
```python
{
    "total_sales": float,       # sum of total_amount
    "total_orders": int,        # row count
    "avg_order_value": float,   # total_sales / total_orders
    "top_category": str,        # category with highest total_amount sum
}
```

**Pre-condition**: `validate_columns(df)` must return `[]` before calling this function.
Rows where `total_amount` is NaN are excluded from the sum.

---

### `aggregate_by_time`

```python
def aggregate_by_time(df: pd.DataFrame, granularity: str) -> pd.DataFrame
```

**Purpose**: Produce a time series of total sales for the trend line chart.

| Parameter     | Type  | Values              |
|---------------|-------|---------------------|
| `granularity` | `str` | `"D"` or `"ME"` (month-end) |

**Returns**: `pd.DataFrame` with columns `["period", "sales"]`, sorted ascending by
`period`. Rows with NaT dates are excluded before resampling.

---

### `aggregate_by_category`

```python
def aggregate_by_category(df: pd.DataFrame) -> pd.DataFrame
```

**Purpose**: Total sales per product category for the category bar chart.

**Returns**: `pd.DataFrame` with columns `["category", "total_sales"]`, sorted
descending by `total_sales`.

---

### `aggregate_by_region`

```python
def aggregate_by_region(df: pd.DataFrame) -> pd.DataFrame
```

**Purpose**: Total sales per geographic region for the regional bar chart.

**Returns**: `pd.DataFrame` with columns `["region", "total_sales"]`, sorted descending
by `total_sales`.

---

## Error Handling Contract

| Situation                         | `data.py` behaviour              | `app.py` responsibility          |
|-----------------------------------|----------------------------------|----------------------------------|
| `file_bytes=None`, sample missing | Raises `FileNotFoundError`       | Show `st.error()`, halt          |
| Malformed CSV (parse error)       | Raises `pd.errors.ParserError`   | Show `st.error()`, halt          |
| Missing columns                   | `validate_columns` returns list  | Show `st.error()`, halt          |
| NaN in numeric columns            | Rows silently excluded in aggs   | Show `st.warning()` with count   |
| Empty DataFrame (0 valid rows)    | `compute_kpis` raises `ZeroDivisionError` | Show `st.error()`       |
