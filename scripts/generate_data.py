import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42
NUM_ROWS = 1000
FIXTURE_ROWS = 20

CATEGORIES = ["Electronics", "Accessories", "Audio", "Wearables", "Smart Home"]
REGIONS = ["North", "South", "East", "West"]
PRODUCTS = {
    "Electronics": ["Laptop Pro", "Tablet X", "Smartphone Ultra", "Smart TV 55\"", "Gaming Console"],
    "Accessories": ["USB-C Hub", "Phone Case", "Screen Protector", "Laptop Stand", "Keyboard Cover"],
    "Audio": ["Wireless Headphones", "Bluetooth Speaker", "Earbuds Pro", "Soundbar", "Studio Microphone"],
    "Wearables": ["Smartwatch Series 5", "Fitness Tracker", "AR Glasses", "Smart Ring", "Health Monitor"],
    "Smart Home": ["Smart Thermostat", "Security Camera", "Smart Bulb Pack", "Voice Assistant", "Smart Lock"],
}
PRICE_RANGES = {
    "Electronics": (299.99, 1499.99),
    "Accessories": (9.99, 79.99),
    "Audio": (29.99, 349.99),
    "Wearables": (49.99, 499.99),
    "Smart Home": (29.99, 249.99),
}

START_DATE = date(2024, 1, 1)
END_DATE = date(2024, 12, 31)


def generate_rows(n: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    rows = []
    date_range = (END_DATE - START_DATE).days

    for i in range(1, n + 1):
        category = rng.choice(CATEGORIES)
        product = rng.choice(PRODUCTS[category])
        lo, hi = PRICE_RANGES[category]
        unit_price = round(rng.uniform(lo, hi), 2)
        quantity = rng.randint(1, 5)
        total_amount = round(unit_price * quantity, 2)
        txn_date = START_DATE + timedelta(days=rng.randint(0, date_range))
        region = rng.choice(REGIONS)

        rows.append({
            "date": txn_date.isoformat(),
            "order_id": f"ORD-{i:06d}",
            "product": product,
            "category": category,
            "region": region,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": total_amount,
        })

    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["date", "order_id", "product", "category", "region", "quantity", "unit_price", "total_amount"]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    repo_root = Path(__file__).parent.parent

    rows = generate_rows(NUM_ROWS, SEED)
    full_path = repo_root / "data" / "sales-data.csv"
    write_csv(full_path, rows)
    print(f"Generated {len(rows)} rows → {full_path}")

    fixture_path = repo_root / "tests" / "fixtures" / "sample.csv"
    write_csv(fixture_path, rows[:FIXTURE_ROWS])
    print(f"Generated {FIXTURE_ROWS} rows → {fixture_path}")
