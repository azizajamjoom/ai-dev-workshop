<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 → 1.0.0 (MINOR — new project constitution, all principles added from blank template)

Modified principles: N/A (first fill)

Added sections:
  - I. Data-First Design
  - II. Layered Dashboard UX
  - III. Comprehensive Metrics Coverage
  - IV. Open Access & Session Privacy
  - V. Cloud-Ready Deployment
  - Technology Stack
  - Development Workflow
  - Governance

Templates requiring updates:
  ✅ .specify/templates/plan-template.md — Constitution Check section is generic; principles apply as-is
  ✅ .specify/templates/spec-template.md — no constitution-specific constraints; template is compatible
  ✅ .specify/templates/tasks-template.md — task phases align with principle-driven structure

Deferred items: None
-->

# E-Commerce Analytics Dashboard Constitution

## Core Principles

### I. Data-First Design

All visualizations and metrics MUST derive exclusively from user-uploaded CSV or Excel files.
The app MUST NOT hardcode sample or synthetic data in any production code path.
File ingestion MUST validate the presence of required columns and coerce data types before
any chart or KPI is rendered. Invalid or unparseable uploads MUST surface a clear, actionable
error message rather than silently producing incorrect output.

**Rationale**: The entire dashboard's value depends on accurate representation of the user's
own data. Silent failures or hardcoded fallbacks would undermine trust in every metric shown.

### II. Layered Dashboard UX

The dashboard MUST provide two distinct view layers accessible from the same session:

- **Executive Layer**: High-level KPIs, summary charts, and trend indicators — minimal
  interaction required, optimized for quick decision-making.
- **Analyst Layer**: Granular filters, date-range selectors, drill-down tables, and
  downloadable subsets of data — designed for detailed exploration.

Each layer MUST be independently navigable (e.g., via sidebar navigation or tabs).
No layer may depend on the other being visited first.

**Rationale**: A mixed audience (executives and analysts) has fundamentally different
interaction patterns. Forcing one path degrades the experience for both groups.

### III. Comprehensive Metrics Coverage

The dashboard MUST cover all three metric domains in dedicated sections:

1. **Revenue & Sales Trends** — total revenue, sales volume over time, growth rates,
   period-over-period comparisons.
2. **Product Performance** — top-selling products, category breakdown, revenue by SKU,
   return rates if data available.
3. **Customer Analytics** — customer count, repeat purchase rate, average order value,
   customer lifetime value estimate, acquisition trend.

Each domain MUST be self-contained: a user navigating only to one domain MUST see
complete and meaningful information without visiting the others.

**Rationale**: Agreed scope from project requirements. Omitting any domain is a
regression, not a simplification.

### IV. Open Access & Session Privacy

The app requires no authentication. Uploaded files MUST be treated as ephemeral:
data MUST NOT persist beyond the active Streamlit session (no writes to disk, no
caching across sessions, no logging of file contents).

The UI MUST display a visible data privacy notice informing users that uploaded data
is processed in-memory and not stored.

**Rationale**: Open access is a deliberate choice. Without authentication, the only
protection for sensitive business data is a strict no-persistence policy and informed
user consent.

### V. Cloud-Ready Deployment

The app MUST be deployable to Streamlit Community Cloud with zero manual server
configuration. Concretely:

- All Python dependencies MUST be listed and pinned in `requirements.txt`.
- No local filesystem paths or machine-specific configurations may be hardcoded.
- Any configuration values (e.g., app title, expected column names) MUST be
  externalized to `config.toml` or Streamlit's secrets management — never
  hardcoded in source files.
- The app MUST start cleanly from a fresh `streamlit run app.py` with no
  pre-existing state.

**Rationale**: Streamlit Community Cloud is the target runtime. Divergence between
local and cloud environments is the primary source of deployment failures.

## Technology Stack

- **Language**: Python 3.11+
- **Framework**: Streamlit
- **Data Processing**: pandas, openpyxl (Excel support)
- **Visualization**: Plotly (interactive charts preferred over static matplotlib)
- **Deployment**: Streamlit Community Cloud
- **Dependency Management**: `requirements.txt` with pinned versions

Deviations from this stack MUST be justified in the relevant plan's Complexity
Tracking section and MUST NOT introduce build steps incompatible with Streamlit
Community Cloud's build environment.

## Development Workflow

- Features are specified in `/specs/[###-feature-name]/spec.md` before implementation begins.
- The Constitution Check gate in each `plan.md` MUST be reviewed and signed off before
  Phase 0 research proceeds.
- All user-facing changes MUST be validated against both the Executive Layer and
  Analyst Layer (Principle II) before marking a task complete.
- Uploaded-data edge cases (empty files, missing columns, non-numeric values in
  numeric columns) MUST be handled per Principle I before a feature is considered done.
- Commits MUST be atomic: one logical change per commit, with a descriptive message.

## Governance

This constitution supersedes all other informal practices, README guidance, or verbal
agreements. When a conflict exists between this document and any other artifact,
this document takes precedence.

**Amendment procedure**:
1. Propose the change with rationale in a PR description or spec note.
2. Increment `CONSTITUTION_VERSION` per semantic versioning rules defined in the
   template governance policy (MAJOR = principle removal/redefinition,
   MINOR = new principle or section, PATCH = wording/clarification).
3. Update `LAST_AMENDED_DATE` to the date of the amendment.
4. Propagate changes to all dependent templates (plan, spec, tasks) and note
   any affected files in the Sync Impact Report comment at the top of this file.

All implementation plans (`plan.md`) MUST include a Constitution Check section
that explicitly verifies compliance with all five principles before work begins.

**Version**: 1.0.0 | **Ratified**: 2026-05-09 | **Last Amended**: 2026-05-09
