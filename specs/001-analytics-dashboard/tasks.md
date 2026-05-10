---
description: "Task list for ShopSmart Sales Analytics Dashboard"
---

# Tasks: ShopSmart Sales Analytics Dashboard

**Input**: Design documents from `specs/001-analytics-dashboard/`
**Prerequisites**: plan.md ✅ spec.md ✅ research.md ✅ data-model.md ✅ contracts/ ✅

**Tests**: Included in Phase 4 (written after implementation, per user decision).

**Organization**: Phase-based (Infrastructure → Data Layer → UI Layer → Tests → Deployment).
User story labels applied to all implementation tasks for traceability.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US5)
- Exact file paths included in every task description

## Path Conventions

Single project layout — all source files at repository root:
- `app.py`, `data.py` at root
- `data/`, `scripts/`, `tests/` at root

---

## Phase 1: Infrastructure

**Purpose**: Project skeleton, pinned dependencies, app configuration, and sample data
generation. Every subsequent phase can run the app as soon as this phase is complete.

- [x] T001 Create directory structure: `data/`, `scripts/`, `tests/fixtures/`, `.streamlit/` at repository root
- [x] T002 [P] Create `requirements.txt` with pinned versions: streamlit>=1.35, plotly>=5.20, pandas>=2.2, openpyxl>=3.1, faker>=25, pytest>=8.0
- [x] T003 [P] Create `.streamlit/config.toml` with app title "ShopSmart Sales Dashboard" and a clean light theme
- [x] T004 Create `scripts/generate_data.py` that generates `data/sales-data.csv` (~1,000 rows, fixed random seed, 12-month date range, 5 categories, 4 regions, columns: date/order_id/product/category/region/quantity/unit_price/total_amount) and also writes a 20-row slice to `tests/fixtures/sample.csv`
- [x] T005 Run `python scripts/generate_data.py` and verify both `data/sales-data.csv` and `tests/fixtures/sample.csv` are created with correct schemas

**Checkpoint**: `streamlit run app.py` will fail (app.py not yet created), but sample data exists and dependencies are installable via `pip install -r requirements.txt`.

---

## Phase 2: Data Layer

**Purpose**: Implement `data.py` — the pure data module. No Streamlit imports allowed here.
All functions in the `contracts/data-module.md` contract must be implemented.

**⚠️ CRITICAL**: `app.py` depends on every function in this phase. Complete this phase before Phase 3.

- [x] T006 Create `data.py` with `REQUIRED_COLUMNS` list constant and `SAMPLE_DATA_PATH = "data/sales-data.csv"` constant
- [x] T007 [P] Implement `load_data(file_bytes: bytes | None) -> pd.DataFrame` in `data.py`: reads from `SAMPLE_DATA_PATH` when `file_bytes` is None, otherwise from `io.BytesIO(file_bytes)`; parses `date` column with `errors="coerce"`; coerces numeric columns with `errors="coerce"`
- [x] T008 [P] Implement `validate_columns(df: pd.DataFrame) -> list[str]` in `data.py`: returns list of column names from `REQUIRED_COLUMNS` absent in `df.columns`; empty list means valid
- [x] T009 Implement `compute_kpis(df: pd.DataFrame) -> dict` in `data.py`: returns `total_sales` (float), `total_orders` (int), `avg_order_value` (float), `top_category` (str); NaN rows excluded from sum (depends on T007, T008)
- [x] T010 [P] Implement `aggregate_by_time(df: pd.DataFrame, granularity: str) -> pd.DataFrame` in `data.py`: sets `date` as index, resamples using `"D"` or `"ME"`, sums `total_amount`, returns columns `["period", "sales"]` sorted ascending; drops NaT rows before resampling
- [x] T011 [P] Implement `aggregate_by_category(df: pd.DataFrame) -> pd.DataFrame` in `data.py`: groups by `category`, sums `total_amount`, returns columns `["category", "total_sales"]` sorted descending
- [x] T012 [P] Implement `aggregate_by_region(df: pd.DataFrame) -> pd.DataFrame` in `data.py`: groups by `region`, sums `total_amount`, returns columns `["region", "total_sales"]` sorted descending

**Checkpoint**: All six `data.py` functions are importable and callable with a pandas DataFrame. No Streamlit or UI code exists yet.

---

## Phase 3: UI Layer

**Purpose**: Build `app.py` — the full Streamlit UI wired to `data.py`. Each task maps to
one or more user stories from the spec.

**Goal**: A running dashboard at `http://localhost:8501` with Overview and Data tabs, all
charts rendering from sample data, file uploader visible, and privacy notice displayed.

**Independent Test**: Run `streamlit run app.py`, navigate to Overview tab — all four KPI
cards and all three charts are visible with correct values. Navigate to Data tab — table
and Download CSV button work.

### Implementation

- [x] T013 Create `app.py` skeleton: `st.set_page_config(page_title="ShopSmart Sales Dashboard")`, import `data`, define two `st.tabs(["Overview", "Data"])`, add a `st.file_uploader` at the top accepting `.csv` files
- [x] T014 [US5] Wire file uploader in `app.py`: decorate `load_data` call with `@st.cache_data`; pass `uploaded_file.getvalue()` when a file is present, `None` otherwise; store result in a local `df` variable
- [x] T015 [US5] Add column validation gate in `app.py`: call `validate_columns(df)` immediately after load; if missing columns exist, show `st.error()` listing them and `st.stop()`; add data privacy notice using `st.caption()` below the file uploader
- [x] T016 [US1] Implement 4 KPI cards in `app.py` Overview tab: call `compute_kpis(df)`; display Total Sales (`st.metric`, formatted `$X,XXX,XXX`), Total Orders (`st.metric`), Average Order Value (`st.metric`, currency-formatted), Top Category (`st.metric`) in a `st.columns(4)` layout
- [x] T017 [US2] Implement sales trend chart in `app.py` Overview tab: add `st.radio` toggle for "Daily" / "Monthly" granularity; call `aggregate_by_time(df, granularity)`; render `px.line` chart with x="period", y="sales", hover tooltips, axis labels; display with `st.plotly_chart(use_container_width=True)`
- [x] T018 [P] [US3] Implement sales by category bar chart in `app.py` Overview tab: call `aggregate_by_category(df)`; render `px.bar` with x="category", y="total_sales", sorted descending, hover tooltips; display with `st.plotly_chart(use_container_width=True)` in left column of `st.columns(2)`
- [x] T019 [P] [US3] Implement sales by region bar chart in `app.py` Overview tab: call `aggregate_by_region(df)`; render `px.bar` with x="region", y="total_sales", sorted descending, hover tooltips; display with `st.plotly_chart(use_container_width=True)` in right column of `st.columns(2)`
- [x] T020 [US4] Implement Data tab in `app.py`: render `st.dataframe(df)` with column filters using `st.multiselect` for category and region; add `st.download_button` that exports the filtered DataFrame as CSV via `df.to_csv(index=False).encode("utf-8")`

**Checkpoint**: `streamlit run app.py` renders a complete, functional dashboard. KPI values
match the expected output in `quickstart.md`. Both tabs are independently navigable.

---

## Phase 4: Tests

**Purpose**: pytest unit tests for all `data.py` functions. Tests run against
`tests/fixtures/sample.csv` (the 20-row fixture generated in Phase 1).

**Goal**: `pytest tests/` passes with 8 tests, 0 failures.

**Independent Test**: Run `pytest tests/ -v` — all test names visible, all green.

### Implementation

- [x] T021 Create `tests/test_data.py` with a `@pytest.fixture` named `sample_df` that calls `data.load_data(None)` after monkeypatching `data.SAMPLE_DATA_PATH` to `"tests/fixtures/sample.csv"`
- [x] T022 [P] Implement `test_load_data_from_path` in `tests/test_data.py`: asserts `sample_df` has 20 rows, all 8 required columns present, `date` column dtype is datetime
- [x] T023 [P] Implement `test_validate_columns_pass` in `tests/test_data.py`: asserts `validate_columns(sample_df)` returns `[]`
- [x] T024 [P] Implement `test_validate_columns_fail` in `tests/test_data.py`: drops `total_amount` column from a copy of `sample_df`, asserts `validate_columns(df_missing)` returns `["total_amount"]`
- [x] T025 [P] Implement `test_compute_kpis` in `tests/test_data.py`: asserts `kpis["total_orders"] == 20`, `kpis["total_sales"] > 0`, `kpis["avg_order_value"] == kpis["total_sales"] / 20`, `kpis["top_category"]` is a non-empty string
- [x] T026 [P] Implement `test_aggregate_by_time_monthly` in `tests/test_data.py`: asserts output columns are `["period", "sales"]`, all `sales` values >= 0, sum > 0, sorted ascending
- [x] T027 [P] Implement `test_aggregate_by_time_daily` in `tests/test_data.py`: asserts output columns are `["period", "sales"]`, sum > 0, sorted ascending, row count >= unique transaction dates
- [x] T028 [P] Implement `test_aggregate_by_category` in `tests/test_data.py`: asserts output columns are `["category", "total_sales"]`, rows are sorted descending by `total_sales`, all 5 category values present
- [x] T029 [P] Implement `test_aggregate_by_region` in `tests/test_data.py`: asserts output columns are `["region", "total_sales"]`, rows are sorted descending by `total_sales`, all 4 region values present
- [x] T030 Run `pytest tests/ -v` and confirm all 8 tests pass with 0 failures

**Checkpoint**: All tests green. `data.py` is fully verified against the data contract.

---

## Phase 5: Deployment

**Purpose**: Push the project to GitHub and deploy to Streamlit Community Cloud.
Verify the live public URL renders the dashboard correctly.

**Goal**: A publicly accessible URL serving the ShopSmart dashboard from Streamlit Community Cloud.

- [x] T031 Commit all project files (`app.py`, `data.py`, `requirements.txt`, `.streamlit/config.toml`, `data/sales-data.csv`, `scripts/generate_data.py`, `tests/`) to git with message `feat: initial ShopSmart sales analytics dashboard`
- [x] T032 Push branch `001-analytics-dashboard` to GitHub remote and open a pull request targeting `main`; merge after review
- [x] T033 On [share.streamlit.io](https://share.streamlit.io): click "New app", connect the GitHub repo, select branch `main`, set main file path to `app.py`, click Deploy
- [x] T034 Once deployed, open the public `*.streamlit.app` URL and verify: Overview tab shows 4 KPI cards, trend chart with toggle, category and region charts; Data tab shows table and Download CSV button; no errors in the browser console
- [x] T035 Run through the `quickstart.md` validation checklist: verify Total Orders ≈ 482, Top Category is Electronics or Audio, all 4 regions appear in the region chart

**Checkpoint**: Dashboard is live, publicly accessible, and all acceptance criteria from the spec are met.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Infrastructure)**: No dependencies — start immediately
- **Phase 2 (Data Layer)**: Requires Phase 1 complete (needs `data/sales-data.csv` to exist for manual testing)
- **Phase 3 (UI Layer)**: Requires Phase 2 complete — every `app.py` function calls `data.py`
- **Phase 4 (Tests)**: Requires Phase 2 complete — tests only cover `data.py`; can run in parallel with Phase 3
- **Phase 5 (Deployment)**: Requires Phase 3 + Phase 4 complete

### User Story Dependencies

| Story | Depends on | Can start after |
|-------|------------|-----------------|
| US5 (Data Loading) | Phase 2 complete | T012 |
| US1 (KPI Cards) | US5 wired in app.py | T015 |
| US2 (Trend Chart) | US5 wired in app.py | T015 |
| US3 (Bar Charts) | US5 wired in app.py | T015 |
| US4 (Data Tab) | US5 wired in app.py | T015 |

### Within Each Phase

- All `[P]`-marked tasks within a phase can start simultaneously
- T009 depends on T007 + T008 (compute_kpis needs load + validate to be defined)
- T016–T020 all depend on T013–T015 (UI skeleton + data wiring must exist first)

### Parallel Opportunities

```bash
# Phase 1 — run T002 and T003 in parallel:
Task: "Create requirements.txt"
Task: "Create .streamlit/config.toml"

# Phase 2 — run after T006:
Task: "Implement load_data"        # T007
Task: "Implement validate_columns" # T008
Task: "Implement aggregate_by_time"    # T010
Task: "Implement aggregate_by_category" # T011
Task: "Implement aggregate_by_region"   # T012

# Phase 3 — after T015:
Task: "Category bar chart"  # T018
Task: "Region bar chart"    # T019

# Phase 4 — after T021:
Tasks T022–T029 (all 8 unit tests) can run in parallel
```

---

## Implementation Strategy

### MVP First (US1 + US5 only)

1. Complete Phase 1: Infrastructure
2. Complete Phase 2: Data Layer (all functions)
3. Complete T013–T016: App skeleton + data loading + KPI cards
4. **STOP and VALIDATE**: Four KPI cards show correct values from sample data
5. Demo to stakeholders if needed

### Incremental Delivery

1. Phase 1 + Phase 2 → foundation ready
2. T013–T016 → US5 + US1 working (MVP — KPI cards live)
3. T017 → US2 working (trend chart with toggle)
4. T018–T019 → US3 working (category + region charts)
5. T020 → US4 working (Data tab + CSV download)
6. Phase 4 → all tests green
7. Phase 5 → deployed and publicly accessible

---

## Notes

- `[P]` = different files or independent logic, no unsatisfied dependencies
- `[USN]` label maps every implementation task to its user story for spec traceability
- `data.py` MUST NOT import `streamlit` — pure data layer per contract
- `@st.cache_data` is applied in `app.py` wrapping the `load_data` call, keyed on `file.getvalue()` bytes
- Run `streamlit run app.py` after T020 as the final manual validation before Phase 4
