# Research: ShopSmart Sales Analytics Dashboard

**Branch**: `001-analytics-dashboard` | **Date**: 2026-05-09

---

## Decision 1: `st.cache_data` with File Uploader

**Decision**: Decorate the data-loading function with `@st.cache_data`. Pass the raw
bytes from the uploaded file (via `file.getvalue()`) as the cache key argument, not the
`UploadedFile` object itself.

**Rationale**: Streamlit's `@st.cache_data` hashes function arguments to determine cache
validity. `UploadedFile` objects are not reliably hashable across reruns, but `bytes`
objects are. Passing `file.getvalue()` ensures the cache invalidates exactly when the
file content changes. For the fallback path (no upload), the function receives `None`
and loads from `data/sales-data.csv`, which is also hashable and cache-stable.

**Alternatives considered**:
- `st.session_state` — gives manual control but requires explicit invalidation logic;
  adds complexity for no measurable benefit at this data size (~1,000 rows).
- No caching — acceptable at 1,000 rows but creates unnecessary recomputation on every
  widget interaction (e.g., toggling the granularity toggle).

---

## Decision 2: Plotly Express vs Plotly Graph Objects

**Decision**: Use Plotly Express (`plotly.express`) for all charts.

**Rationale**: Plotly Express provides a high-level API that accepts pandas DataFrames
directly, produces fully interactive charts (hover tooltips, zoom, pan) with minimal
code, and covers all required chart types: `px.line` for sales trend, `px.bar` for
category and regional breakdowns. The resulting charts are identical in capability to
Graph Objects for this feature's requirements.

**Alternatives considered**:
- Plotly Graph Objects — more verbose and lower-level; appropriate when customisation
  beyond Express defaults is needed. No such requirement exists here.
- Matplotlib / Altair — static or less interactive; ruled out by constitution (Principle V:
  Plotly as the standard).

---

## Decision 3: Column Validation Strategy

**Decision**: Define a `REQUIRED_COLUMNS` constant in `data.py` listing all eight expected
column names. `validate_columns()` returns the list of missing column names. The UI
layer in `app.py` calls this function immediately after loading and halts rendering if
the list is non-empty, displaying a `st.error()` message that names each missing column.

**Rationale**: Separating validation from loading keeps `data.py` pure (no Streamlit
imports) and makes the validation logic unit-testable in isolation.

**Alternatives considered**:
- Validate inside the load function and raise an exception — couples loading to
  validation; harder to unit test the two concerns separately.
- Schema libraries (pandera, pydantic) — appropriate for production pipelines; adds
  a dependency for a task achievable with a five-line function.

---

## Decision 4: Sample Data Generation

**Decision**: `scripts/generate_data.py` uses the `faker` library and Python's `random`
module to produce deterministic output (fixed random seed) of ~1,000 rows covering
12 months of dates, 5 categories, and 4 regions matching the PRD specification. The
same script writes a 20-row fixture to `tests/fixtures/sample.csv` for use in pytest.

**Rationale**: A fixed seed ensures reproducible KPI values, allowing the PRD's expected
output table (`Total Orders: 482`, `Total Sales: ~$650k–$700k`) to be validated by tests.
Using the same script for both datasets guarantees the fixture has the same schema as
the full dataset.

**Alternatives considered**:
- Hand-authored fixture CSV — error-prone; schema drift likely as columns evolve.
- NumPy random without seed — non-deterministic; tests would need tolerance ranges
  rather than exact assertions.

---

## Decision 5: Streamlit Community Cloud Deployment Requirements

**Decision**: The repo root must contain `requirements.txt` with pinned versions. A
`.streamlit/config.toml` file sets the app title and theme. No `packages.txt` or
system-level dependencies are required. The entry point is `app.py` at the repo root.

**Key pinned versions (minimum)**:
```
streamlit>=1.35.0
plotly>=5.20.0
pandas>=2.2.0
openpyxl>=3.1.0
faker>=25.0.0
pytest>=8.0.0
```

**Rationale**: Streamlit Community Cloud auto-detects `requirements.txt` at the root.
Pinning minor versions prevents silent breakage from upstream updates while allowing
patch releases. `openpyxl` is required by pandas for Excel support (Principle V). No
secrets or environment variables are needed for this open-access app.

**Alternatives considered**:
- `pyproject.toml` with Poetry — not natively supported by Streamlit Community Cloud
  without a custom build; unnecessary complexity.
- Unpinned versions — violates Constitution Principle V (Cloud-Ready Deployment).

---

## Decision 6: pytest Structure for `data.py`

**Decision**: Single test file `tests/test_data.py`. Tests load the fixture CSV
(`tests/fixtures/sample.csv`) and assert computed KPI values, column validation
results, and aggregation shapes. No mocking; all tests use the real pandas logic.

**Test cases to cover**:
1. `test_load_data_from_path` — loads fixture, asserts row count and column names.
2. `test_validate_columns_pass` — valid DataFrame returns empty missing list.
3. `test_validate_columns_fail` — DataFrame missing columns returns correct names.
4. `test_compute_kpis` — asserts total_sales, total_orders, avg_order_value, top_category types and mathematical relationships.
5. `test_aggregate_by_time_monthly` — asserts output has one row per calendar month.
6. `test_aggregate_by_time_daily` — asserts output has one row per unique date.
7. `test_aggregate_by_category` — asserts output sorted descending, all categories present.
8. `test_aggregate_by_region` — asserts output sorted descending, all regions present.

**Alternatives considered**:
- Mocking pandas DataFrames — rejected (constitution precedent: real data tests only).
- Streamlit testing framework (`streamlit.testing`) — out of scope for this plan;
  testing the UI rendering layer was not selected in user Q&A.
