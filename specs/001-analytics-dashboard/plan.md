# Implementation Plan: ShopSmart Sales Analytics Dashboard

**Branch**: `001-analytics-dashboard` | **Date**: 2026-05-09 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-analytics-dashboard/spec.md`

## Summary

Build a two-file Streamlit dashboard (`app.py` + `data.py`) that loads sales data from
a CSV file (uploaded by the user or auto-loaded from a bundled sample), validates the
schema, and renders an executive Overview tab (4 KPI cards, sales trend with daily/monthly
toggle, category bar chart, regional bar chart) plus an analyst Data tab (filterable table,
CSV download). Deployed to Streamlit Community Cloud with no authentication.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit ≥1.35, Plotly ≥5.20 (Express), pandas ≥2.2, openpyxl ≥3.1, faker ≥25 (data generation), pytest ≥8.0
**Storage**: CSV file (session-scoped in-memory; `data/sales-data.csv` as bundled fallback)
**Testing**: pytest — unit tests for `data.py` (8 test cases covering load, validate, compute, aggregate)
**Target Platform**: Streamlit Community Cloud (Linux, modern browsers)
**Project Type**: Data dashboard / web application
**Performance Goals**: Dashboard load < 5 seconds; chart render < 2 seconds after data load (PRD NFR-1)
**Constraints**: No authentication; no server-side persistence; single `requirements.txt`; no system packages
**Scale/Scope**: ~1,000 CSV rows; single concurrent user per session; no real-time data feed

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status | Notes |
|-----------|------|--------|-------|
| I. Data-First Design | All charts derive from loaded CSV; column validation runs before any render | ✅ PASS | `validate_columns()` in `data.py`; `st.error()` halts rendering on failure |
| II. Layered Dashboard UX | Overview tab (executive) + Data tab (analyst) independently navigable | ✅ PASS | Streamlit tabs; no cross-tab dependency |
| III. Comprehensive Metrics Coverage | Revenue trends, product performance, customer analytics all present | ✅ PASS | KPI cards (total sales, avg order value, top category) + trend chart + category/region charts |
| IV. Open Access & Session Privacy | No auth; no persistence; privacy notice displayed | ✅ PASS | No login; `st.cache_data` is session-scoped; privacy notice in UI |
| V. Cloud-Ready Deployment | `requirements.txt` pinned; no local paths; Streamlit Community Cloud entry point `app.py` | ✅ PASS | `SAMPLE_DATA_PATH` is a relative constant; no hardcoded absolute paths |

**All gates pass. Proceeding to implementation.**

## Project Structure

### Documentation (this feature)

```text
specs/001-analytics-dashboard/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── data-module.md   # data.py public interface contract
└── tasks.md             # Phase 2 output (/speckit-tasks — not yet created)
```

### Source Code (repository root)

```text
app.py                        # Streamlit UI entrypoint
data.py                       # Data loading, validation, aggregations
data/
└── sales-data.csv            # Generated sample dataset (~1,000 rows)
scripts/
└── generate_data.py          # Generates data/sales-data.csv + tests/fixtures/sample.csv
tests/
├── fixtures/
│   └── sample.csv            # 20-row test fixture (same schema as sample dataset)
└── test_data.py              # pytest unit tests for data.py
requirements.txt              # Pinned Python dependencies
.streamlit/
└── config.toml               # App title and theme configuration
```

**Structure Decision**: Two-file flat layout (`app.py` + `data.py`) at the repo root.
No `src/` package required — Streamlit's entry point is a single script, and the data
module is small enough that a package would add indirection without benefit. Tests live
in `tests/` to keep them separate from the app without requiring packaging.

## Complexity Tracking

> No Constitution Check violations. This section is intentionally empty.
