# Quickstart: ShopSmart Sales Analytics Dashboard

## Prerequisites

- Python 3.11 or later
- Git

## Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd <repo-directory>

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate sample data and test fixture
python scripts/generate_data.py
# Creates: data/sales-data.csv (~1,000 rows)
# Creates: tests/fixtures/sample.csv (20 rows, same schema)
```

## Run the Dashboard

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

- The **Overview** tab shows KPI cards, sales trend chart, and category/region bar charts.
- The **Data** tab shows a filterable table and a "Download CSV" button.
- Use the file uploader at the top to load your own CSV, or leave it empty to use the sample data.

## Run Tests

```bash
pytest tests/
```

Expected output: 8 tests pass, 0 failures.

## Deploy to Streamlit Community Cloud

1. Push the repository to GitHub (ensure `data/sales-data.csv` and `requirements.txt` are committed).
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**.
3. Select the repository, branch (`main`), and set the main file to `app.py`.
4. Click **Deploy**. The app will be publicly accessible at a `*.streamlit.app` URL.

No environment variables or secrets are required.

## Validate Against Expected Output

After generating sample data and running the dashboard, the Overview tab should show
approximately:

| KPI               | Expected Value           |
|-------------------|--------------------------|
| Total Sales       | $650,000 – $700,000      |
| Total Orders      | ~482                     |
| Avg Order Value   | ~$1,350 – $1,450         |
| Top Category      | Electronics or Audio     |
