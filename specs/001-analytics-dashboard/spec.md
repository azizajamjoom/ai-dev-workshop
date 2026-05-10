# Feature Specification: ShopSmart Sales Analytics Dashboard

**Feature Branch**: `001-analytics-dashboard`
**Created**: 2026-05-09
**Status**: Draft
**Input**: PRD — E-Commerce Analytics Platform (ShopSmart)

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Executive KPI Overview (Priority: P1)

Sarah (Finance Manager) opens the dashboard before an executive meeting. She sees four
summary cards at the top of the Overview tab: Total Sales, Total Orders, Average Order
Value, and Top Category. All values reflect the loaded dataset with no additional steps
required.

**Why this priority**: KPI cards are the highest-visibility output of the dashboard and
the primary reason executives visit it. Everything else builds on top of this baseline.

**Independent Test**: Load the dashboard with the sample CSV. Verify that four KPI cards
appear on the Overview tab, each displaying a labelled, formatted value derived from the
data (e.g., Total Sales shown as `$XXX,XXX`).

**Acceptance Scenarios**:

1. **Given** the dashboard loads with a valid CSV, **When** the user views the Overview tab,
   **Then** four KPI cards are visible: Total Sales (currency-formatted), Total Orders
   (integer), Average Order Value (currency-formatted), and Top Category (text label).
2. **Given** a CSV is loaded, **When** values are computed, **Then** Total Sales equals
   the sum of the `total_amount` column and Average Order Value equals Total Sales ÷ Total Orders.
3. **Given** required columns are missing from the uploaded file, **When** the dashboard
   attempts to render, **Then** a clear error message names the missing columns and no
   KPI cards are shown.

---

### User Story 2 — Sales Trend Visualization (Priority: P2)

David (CEO) wants to understand whether ShopSmart is growing. He views the Sales Trend
chart on the Overview tab and switches between monthly and daily granularity using a
toggle to spot both long-term patterns and short-term spikes.

**Why this priority**: Trend data is the primary tool for strategic decision-making and
is referenced in every executive meeting.

**Independent Test**: Load the dashboard. Verify that a line chart appears on the Overview
tab, the toggle switches between daily and monthly views, and the chart updates to reflect
the selected granularity without reloading the page.

**Acceptance Scenarios**:

1. **Given** a valid CSV is loaded, **When** the user views the Overview tab, **Then**
   a line chart of sales over time is visible with interactive tooltips showing the exact
   value and date for each data point.
2. **Given** the trend chart is visible, **When** the user selects "Monthly" on the
   granularity toggle, **Then** the chart aggregates sales by calendar month.
3. **Given** the trend chart is visible, **When** the user selects "Daily" on the
   granularity toggle, **Then** the chart shows one data point per day without aggregation.

---

### User Story 3 — Category & Regional Breakdown (Priority: P2)

James (Marketing Director) and Maria (Regional Manager) need to allocate resources by
product category and geographic region. They view two bar charts side-by-side on the
Overview tab, each sorted from highest to lowest sales value.

**Why this priority**: Category and regional charts directly drive budget and staffing
decisions for two distinct user groups and require no analyst interaction to be useful.

**Independent Test**: Load the dashboard. Verify that two bar charts appear on the
Overview tab — one for category sales and one for regional sales — each sorted
descending by value, with interactive tooltips.

**Acceptance Scenarios**:

1. **Given** a valid CSV is loaded, **When** the user views the Overview tab, **Then**
   a bar chart shows sales by product category, sorted highest to lowest, with all
   categories in the dataset represented.
2. **Given** a valid CSV is loaded, **When** the user views the Overview tab, **Then**
   a bar chart shows sales by geographic region, sorted highest to lowest, with all
   regions in the dataset represented.
3. **Given** the user hovers over any bar, **Then** a tooltip shows the exact category
   or region name and its total sales value.

---

### User Story 4 — Analyst Data Explorer (Priority: P3)

An analyst needs to verify numbers or export a filtered slice of the data. They switch
to the Data tab, apply column filters to narrow the dataset, and download the result as
a CSV file.

**Why this priority**: The Analyst Layer satisfies the constitution's layered UX
requirement and supports power users without cluttering the executive view.

**Independent Test**: Navigate to the Data tab. Verify that a filterable, sortable data
table is visible and a "Download CSV" button exports the currently displayed rows.

**Acceptance Scenarios**:

1. **Given** a valid CSV is loaded, **When** the user clicks the Data tab, **Then** a
   table displays all rows from the loaded dataset with column headers matching the source file.
2. **Given** the Data tab is active, **When** the user applies a filter (e.g., selects
   a specific region), **Then** the table updates to show only matching rows.
3. **Given** the table is filtered, **When** the user clicks "Download CSV", **Then**
   a CSV file containing only the currently visible rows is downloaded to their browser.

---

### User Story 5 — Flexible Data Loading (Priority: P1)

Any stakeholder can load the dashboard with their own CSV export or use the built-in
sample dataset. A file uploader is visible at the top of the page; if no file is
uploaded the sample dataset at `data/sales-data.csv` loads automatically.

**Why this priority**: Data loading is a prerequisite for every other story; an unclear
or broken loading experience blocks all other functionality.

**Independent Test**: Open the dashboard without uploading a file — verify the sample
data loads and all charts render. Then upload a different valid CSV — verify the
dashboard re-renders with the new data.

**Acceptance Scenarios**:

1. **Given** no file has been uploaded, **When** the dashboard loads, **Then** the
   sample dataset is loaded automatically and all charts and KPIs render correctly.
2. **Given** the file uploader is visible, **When** the user uploads a CSV with the
   required columns, **Then** all charts and KPIs update to reflect the new data.
3. **Given** a file is uploaded, **When** it is missing one or more required columns,
   **Then** a descriptive error message is displayed listing the missing columns and
   no charts are rendered.
4. **Given** the dashboard is running, **When** it is closed or the session ends,
   **Then** no uploaded data is retained — the next session starts fresh with the
   sample dataset.

---

### Edge Cases

- What happens when the CSV has no rows (headers only)? → Dashboard displays a "no data" message; no charts or KPIs are rendered.
- What happens when a numeric column (e.g., `total_amount`) contains non-numeric values? → Affected rows are skipped and a warning banner shows how many rows were excluded.
- What happens when the date column contains unparseable date strings? → Affected rows are excluded from trend charts with a visible warning; KPI cards still render from valid rows.
- What happens if the uploaded file is an Excel file (.xlsx) instead of CSV? → The uploader accepts only CSV; an unsupported-format message is shown.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The dashboard MUST display four KPI cards on the Overview tab: Total Sales (sum of `total_amount`), Total Orders (count of rows), Average Order Value (Total Sales ÷ Total Orders), and Top Category (category with highest total sales).
- **FR-002**: The dashboard MUST display a line chart of sales over time on the Overview tab with a toggle to switch between daily and monthly granularity.
- **FR-003**: The dashboard MUST display a bar chart of sales by product category, sorted descending by value, on the Overview tab.
- **FR-004**: The dashboard MUST display a bar chart of sales by geographic region, sorted descending by value, on the Overview tab.
- **FR-005**: All charts MUST include interactive tooltips showing exact values on hover.
- **FR-006**: The dashboard MUST provide a file uploader; if no file is uploaded, it MUST automatically load the sample dataset from `data/sales-data.csv`.
- **FR-007**: The dashboard MUST validate that required columns (`date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, `total_amount`) are present before rendering any output; absent columns MUST be listed in an error message.
- **FR-008**: The dashboard MUST have a Data tab containing a filterable, sortable table of all loaded rows.
- **FR-009**: The Data tab MUST include a "Download CSV" button that exports the currently filtered rows.
- **FR-010**: Currency values MUST be formatted as `$X,XXX,XXX` and large integers MUST use comma separators.
- **FR-011**: A data privacy notice MUST be visible on the page informing users that uploaded data is processed in-memory and not stored.
- **FR-012**: The dashboard MUST NOT persist any uploaded data beyond the active session.

### Key Entities

- **Transaction**: A single sales record with date, order ID, product, category, region, quantity, unit price, and total amount.
- **KPI**: A single aggregated metric (Total Sales, Total Orders, Average Order Value, Top Category) derived from all transactions in the loaded dataset.
- **Time Series**: Transactions aggregated by day or calendar month for trend visualization.
- **Category Aggregate**: Total sales grouped by product category.
- **Region Aggregate**: Total sales grouped by geographic region.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A stakeholder can load the dashboard and read all four KPI values within 30 seconds of opening the URL — no training or instructions required.
- **SC-002**: Switching the trend chart granularity (daily ↔ monthly) takes effect immediately with no page reload.
- **SC-003**: A user can navigate from the Overview tab to the Data tab, apply a filter, and download a CSV in under 2 minutes without assistance.
- **SC-004**: Uploading a valid CSV replaces all dashboard data (KPIs, charts, table) within 5 seconds of file selection.
- **SC-005**: An invalid CSV (missing required columns) surfaces a readable error message within 3 seconds; no partial or misleading output is shown.
- **SC-006**: The dashboard is accessible via a public Streamlit Community Cloud URL with no installation required for end users.
- **SC-007**: 80% of first-time users can identify the Top Category and the highest-revenue region without any written instructions (measured via user acceptance testing).

## Assumptions

- The CSV data source uses the column schema defined in the PRD (`date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, `total_amount`). Uploads with different column names will fail validation and require manual mapping — column remapping is out of scope for this release.
- Date values in the CSV follow ISO 8601 format (`YYYY-MM-DD`). Other formats may be partially supported but are not guaranteed.
- The dashboard is intended for desktop browsers; mobile layout optimisation is Phase 2.
- All stakeholders access the same public URL; no role-based views or access restrictions exist in this release.
- "Download CSV" produces a file containing only the columns from the original dataset (no derived columns appended).
- Excel (.xlsx) file uploads are out of scope; only `.csv` files are accepted.
- The `data/sales-data.csv` sample file is bundled with the deployed app and always available as a fallback.
