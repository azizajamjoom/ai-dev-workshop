# Data Model: ShopSmart Sales Analytics Dashboard

**Branch**: `001-analytics-dashboard` | **Date**: 2026-05-09

---

## Source Schema: Transaction

The canonical record loaded from `data/sales-data.csv` or a user-uploaded file.

| Field          | Type    | Constraints                              | Example          |
|----------------|---------|------------------------------------------|------------------|
| `date`         | date    | ISO 8601 (YYYY-MM-DD); required          | `2024-01-15`     |
| `order_id`     | str     | Non-empty; unique per transaction        | `ORD-001234`     |
| `product`      | str     | Non-empty                                | `Wireless Headphones` |
| `category`     | str     | One of 5 known categories; non-empty     | `Electronics`    |
| `region`       | str     | One of 4 known regions; non-empty        | `North`          |
| `quantity`     | int     | ≥ 1                                      | `2`              |
| `unit_price`   | float   | > 0                                      | `49.99`          |
| `total_amount` | float   | > 0; should equal quantity × unit_price  | `99.98`          |

**REQUIRED_COLUMNS** (validation gate):
```
["date", "order_id", "product", "category", "region", "quantity", "unit_price", "total_amount"]
```

Rows with unparseable `date` values are dropped before time-series aggregation.
Rows with non-numeric `total_amount` are dropped before any aggregation. Both
exclusions emit a visible warning in the UI.

---

## Derived: KPISet

Computed from the full (validated) DataFrame. Passed to the Overview tab's KPI cards.

| Field             | Type   | Derivation                                |
|-------------------|--------|-------------------------------------------|
| `total_sales`     | float  | `df["total_amount"].sum()`                |
| `total_orders`    | int    | `len(df)`                                 |
| `avg_order_value` | float  | `total_sales / total_orders`              |
| `top_category`    | str    | Category with highest `total_amount` sum  |

---

## Derived: TimeSeries

Aggregated for the sales trend line chart. Shape depends on granularity selection.

| Field       | Type   | Daily mode          | Monthly mode              |
|-------------|--------|---------------------|---------------------------|
| `period`    | date   | Each unique date    | First day of each month   |
| `sales`     | float  | `total_amount` sum  | `total_amount` sum        |

Granularity is controlled by the UI toggle; `data.py` receives the string `"D"` (daily)
or `"M"` (monthly) and resamples accordingly using `df.resample()`.

---

## Derived: CategoryAggregate

Used by the Category bar chart on the Overview tab.

| Field         | Type   | Derivation                              |
|---------------|--------|-----------------------------------------|
| `category`    | str    | Unique values from `df["category"]`     |
| `total_sales` | float  | `df.groupby("category")["total_amount"].sum()` |

Result is sorted descending by `total_sales`.

---

## Derived: RegionAggregate

Used by the Regional bar chart on the Overview tab.

| Field         | Type   | Derivation                              |
|---------------|--------|-----------------------------------------|
| `region`      | str    | Unique values from `df["region"]`       |
| `total_sales` | float  | `df.groupby("region")["total_amount"].sum()` |

Result is sorted descending by `total_sales`.

---

## Reference Data

### Product Categories (5)
`Electronics`, `Accessories`, `Audio`, `Wearables`, `Smart Home`

### Geographic Regions (4)
`North`, `South`, `East`, `West`

---

## State Transitions

```
App Start
    │
    ▼
[No file uploaded]
    │  Automatic fallback
    ▼
Load data/sales-data.csv ──► Validate columns ──► Render dashboard
                                    │
                             [Columns missing]
                                    │
                                    ▼
                             Show st.error() — halt rendering

[User uploads file]
    │
    ▼
Read uploaded bytes ──► @st.cache_data ──► Validate columns ──► Render dashboard

[Session ends]
    │
    ▼
All in-memory state discarded — no persistence
```
