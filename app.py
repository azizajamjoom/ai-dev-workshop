import streamlit as st
import plotly.express as px
import data

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

# ── T013: File uploader ────────────────────────────────────────────────────────
st.title("ShopSmart Sales Dashboard")

uploaded_file = st.file_uploader("Upload sales CSV", type=["csv"])
st.caption(
    "Your data is processed in-memory and is not stored or shared. "
    "It is discarded when your session ends."
)


# ── T014: Load data with caching ───────────────────────────────────────────────
@st.cache_data
def load(file_bytes: bytes | None):
    return data.load_data(file_bytes)


file_bytes = uploaded_file.getvalue() if uploaded_file is not None else None
df = load(file_bytes)

# ── T015: Column validation gate ──────────────────────────────────────────────
missing = data.validate_columns(df)
if missing:
    st.error(f"Uploaded file is missing required columns: {', '.join(missing)}")
    st.stop()

nan_count = int(df["total_amount"].isna().sum())
if nan_count:
    st.warning(
        f"{nan_count} row(s) have non-numeric values in 'total_amount' and are "
        "excluded from calculations."
    )

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_overview, tab_data = st.tabs(["Overview", "Data"])

# ── T016: KPI cards ───────────────────────────────────────────────────────────
with tab_overview:
    kpis = data.compute_kpis(df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sales", f"${kpis['total_sales']:,.0f}")
    c2.metric("Total Orders", f"{kpis['total_orders']:,}")
    c3.metric("Avg Order Value", f"${kpis['avg_order_value']:,.2f}")
    c4.metric("Top Category", kpis["top_category"])

    st.divider()

    # ── T017: Sales trend chart ────────────────────────────────────────────────
    granularity_label = st.radio(
        "Trend granularity", ["Monthly", "Daily"], horizontal=True
    )
    granularity_code = "ME" if granularity_label == "Monthly" else "D"
    ts = data.aggregate_by_time(df, granularity_code)

    fig_trend = px.line(
        ts,
        x="period",
        y="sales",
        title="Sales Trend Over Time",
        labels={"period": "Date", "sales": "Total Sales ($)"},
    )
    fig_trend.update_traces(hovertemplate="Date: %{x}<br>Sales: $%{y:,.0f}<extra></extra>")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()

    # ── T018 + T019: Category and Region bar charts ────────────────────────────
    col_cat, col_reg = st.columns(2)

    with col_cat:
        cat_df = data.aggregate_by_category(df)
        fig_cat = px.bar(
            cat_df,
            x="category",
            y="total_sales",
            title="Sales by Category",
            labels={"category": "Category", "total_sales": "Total Sales ($)"},
        )
        fig_cat.update_traces(
            hovertemplate="Category: %{x}<br>Sales: $%{y:,.0f}<extra></extra>"
        )
        fig_cat.update_layout(xaxis={"categoryorder": "total descending"})
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_reg:
        reg_df = data.aggregate_by_region(df)
        fig_reg = px.bar(
            reg_df,
            x="region",
            y="total_sales",
            title="Sales by Region",
            labels={"region": "Region", "total_sales": "Total Sales ($)"},
        )
        fig_reg.update_traces(
            hovertemplate="Region: %{x}<br>Sales: $%{y:,.0f}<extra></extra>"
        )
        fig_reg.update_layout(xaxis={"categoryorder": "total descending"})
        st.plotly_chart(fig_reg, use_container_width=True)

# ── T020: Data tab ─────────────────────────────────────────────────────────────
with tab_data:
    st.subheader("Explore & Export Data")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_categories = st.multiselect(
            "Filter by Category",
            options=sorted(df["category"].dropna().unique()),
            default=[],
        )
    with col_f2:
        selected_regions = st.multiselect(
            "Filter by Region",
            options=sorted(df["region"].dropna().unique()),
            default=[],
        )

    filtered = df.copy()
    if selected_categories:
        filtered = filtered[filtered["category"].isin(selected_categories)]
    if selected_regions:
        filtered = filtered[filtered["region"].isin(selected_regions)]

    st.caption(f"Showing {len(filtered):,} of {len(df):,} rows")
    st.dataframe(filtered, use_container_width=True)

    st.download_button(
        label="Download CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="shopmart-sales-filtered.csv",
        mime="text/csv",
    )
