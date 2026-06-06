"""
generate_mock_data.py
Seeds all three data sources with realistic but intentionally messy data:
  - Shopify API data  → data/raw/shopify_data.json
  - PoS CSV          → data/raw/pos_transactions.csv
  - Loyalty API data  → data/raw/loyalty_data.json

Messiness introduced on purpose:
  • Mixed date formats (ISO, US, EU, epoch)
  • Inconsistent phone formats
  • Duplicate customers across sources (same person, different IDs)
  • Missing fields (None / empty string)
  • Inconsistent name casing
  • Typos in email addresses (intentionally seeded duplicates)
"""
import json
import random
import csv
from pathlib import Path
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

NUM_BASE_CUSTOMERS    = 80
NUM_OVERLAP           = 30
NUM_SHOPIFY_ONLY      = 20
NUM_POS_ONLY          = 15
NUM_LOYALTY_ONLY      = 15
NUM_POS_TRANSACTIONS  = 200


# ── Helpers ──────────────────────────────────────────────────────────────────

def random_date_str(start_year=2020):
    """Return a date string in one of several inconsistent formats."""
    d = fake.date_between(start_date=f"-{2024-start_year}y", end_date="today")
    fmt = random.choice([
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%d %b %Y",
        "%B %d, %Y",
    ])
    return d.strftime(fmt)


def messy_phone():
    """Return a phone number in an inconsistent format."""
    digits = "".join([str(random.randint(0,9)) for _ in range(10)])
    fmt = random.choice([
        f"+1{digits}",
        f"({digits[:3]}) {digits[3:6]}-{digits[6:]}",
        f"{digits[:3]}-{digits[3:6]}-{digits[6:]}",
        f"{digits}",
        f"1-{digits[:3]}-{digits[3:6]}-{digits[6:]}",
        None,
    ])
    return fmt


def messy_name(name: str) -> str:
    """Randomly mangle casing."""
    choice = random.random()
    if choice < 0.2:
        return name.upper()
    elif choice < 0.4:
        return name.lower()
    return name.title()


def maybe_none(value, probability=0.12):
    """Randomly drop a field value."""
    return None if random.random() < probability else value


# ── Build customer pool ───────────────────────────────────────────────────────

print("⚙  Generating base customer pool...")
base_customers = []
for i in range(NUM_BASE_CUSTOMERS):
    first = fake.first_name()
    last  = fake.last_name()
    base_customers.append({
        "first_name": first,
        "last_name":  last,
        "email":      fake.email(),
        "phone":      messy_phone(),
        "dob":        fake.date_of_birth(minimum_age=18, maximum_age=75).strftime("%Y-%m-%d"),
        "city":       fake.city(),
        "state":      fake.state_abbr(),
        "zip":        fake.zipcode(),
    })

overlap_customers  = base_customers[:NUM_OVERLAP]
shopify_extra      = [{"first_name": fake.first_name(), "last_name": fake.last_name(),
                        "email": fake.email(), "phone": messy_phone(),
                        "dob": fake.date_of_birth(minimum_age=18, maximum_age=75).strftime("%Y-%m-%d"),
                        "city": fake.city(), "state": fake.state_abbr(), "zip": fake.zipcode()}
                       for _ in range(NUM_SHOPIFY_ONLY)]
pos_extra          = [{"first_name": fake.first_name(), "last_name": fake.last_name(),
                        "email": fake.email(), "phone": messy_phone(),
                        "dob": fake.date_of_birth(minimum_age=18, maximum_age=75).strftime("%Y-%m-%d"),
                        "city": fake.city(), "state": fake.state_abbr(), "zip": fake.zipcode()}
                       for _ in range(NUM_POS_ONLY)]
loyalty_extra      = [{"first_name": fake.first_name(), "last_name": fake.last_name(),
                        "email": fake.email(), "phone": messy_phone(),
                        "dob": fake.date_of_birth(minimum_age=18, maximum_age=75).strftime("%Y-%m-%d"),
                        "city": fake.city(), "state": fake.state_abbr(), "zip": fake.zipcode()}
                       for _ in range(NUM_LOYALTY_ONLY)]


# ── Shopify Data ──────────────────────────────────────────────────────────────

print("🛍  Generating Shopify data...")
shopify_customers = []
shopify_orders    = []

for idx, c in enumerate(overlap_customers + shopify_extra, start=1):
    shopify_id = f"SHP-{idx:05d}"
    shopify_customers.append({
        "id":         shopify_id,
        "first_name": messy_name(maybe_none(c["first_name"], 0.05) or ""),
        "last_name":  messy_name(maybe_none(c["last_name"],  0.05) or ""),
        "email":      maybe_none(c["email"], 0.08),
        "phone":      maybe_none(c["phone"], 0.20),
        "created_at": random_date_str(2021),
        "addresses": [{
            "city":     maybe_none(c["city"]),
            "province": maybe_none(c["state"]),
            "zip":      maybe_none(c["zip"]),
            "country":  "US",
        }],
        "tags": random.sample(["vip", "wholesale", "newsletter", "returning", "at-risk"], k=random.randint(0,3)),
        "orders_count":    random.randint(1, 25),
        "total_spent":     str(round(random.uniform(20, 2000), 2)),
        "note":            maybe_none(fake.sentence(), 0.7),
    })
    for _ in range(random.randint(1, 5)):
        shopify_orders.append({
            "id":            f"ORD-{fake.uuid4()[:8].upper()}",
            "customer_id":   shopify_id,
            "email":         c["email"],
            "created_at":    random_date_str(2021),
            "financial_status": random.choice(["paid", "pending", "refunded"]),
            "total_price":   str(round(random.uniform(10, 500), 2)),
            "line_items": [{
                "title":    fake.bs().title(),
                "quantity": random.randint(1, 4),
                "price":    str(round(random.uniform(5, 150), 2)),
            } for _ in range(random.randint(1, 4))],
        })

shopify_data = {"customers": shopify_customers, "orders": shopify_orders}
with open(RAW_DIR / "shopify_data.json", "w") as f:
    json.dump(shopify_data, f, indent=2)
print(f"   ✓ {len(shopify_customers)} customers, {len(shopify_orders)} orders")


# ── PoS CSV ───────────────────────────────────────────────────────────────────

print("🏪  Generating PoS CSV data...")
pos_pool = overlap_customers + pos_extra
pos_rows = []
for _ in range(NUM_POS_TRANSACTIONS):
    c = random.choice(pos_pool)
    txn_date = random_date_str(2021)
    pos_rows.append({
        "transaction_id":  f"POS-{fake.uuid4()[:8].upper()}",
        "customer_email":  maybe_none(c["email"], 0.10),
        "customer_phone":  maybe_none(c["phone"], 0.25),
        "customer_name":   (f"{c['last_name']}, {c['first_name']}"
                            if random.random() < 0.3
                            else messy_name(f"{c['first_name']} {c['last_name']}")),
        "transaction_date": txn_date,
        "amount":          round(random.uniform(5, 300), 2),
        "payment_method":  random.choice(["cash", "card", "contactless", "CARD", "Cash"]),
        "store_id":        f"STORE-{random.randint(1,5):02d}",
        "items_count":     random.randint(1, 8),
        "discount_applied": random.choice(["Y", "N", "yes", "no", "1", "0", ""]),
    })

with open(RAW_DIR / "pos_transactions.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=pos_rows[0].keys())
    writer.writeheader()
    writer.writerows(pos_rows)
print(f"   ✓ {len(pos_rows)} PoS transactions")


# ── Loyalty Data ──────────────────────────────────────────────────────────────

print("🎖  Generating Loyalty data...")
loyalty_members = []
for idx, c in enumerate(overlap_customers + loyalty_extra, start=1):
    tier_pts = {"Bronze": (0, 999), "Silver": (1000, 4999), "Gold": (5000, 19999), "Platinum": (20000, 99999)}
    tier      = random.choice(list(tier_pts.keys()))
    pts_range = tier_pts[tier]
    loyalty_members.append({
        "member_id":       f"LYL-{idx:06d}",
        "email_address":   maybe_none(c["email"], 0.06),
        "mobile_number":   maybe_none(c["phone"], 0.18),
        "given_name":      messy_name(maybe_none(c["first_name"], 0.04) or ""),
        "surname":         messy_name(maybe_none(c["last_name"],  0.04) or ""),
        "birth_date":      maybe_none(random_date_str(1950), 0.15),
        "points_balance":  random.randint(*pts_range),
        "tier":            tier,
        "enrolled_date":   random_date_str(2019),
        "last_activity":   random_date_str(2022),
        "opt_in_email":    random.choice([True, False, "true", "false", 1, 0]),
        "opt_in_sms":      random.choice([True, False, "true", "false", 1, 0]),
        "referral_code":   fake.lexify("????-####").upper(),
    })

loyalty_data = {"members": loyalty_members}
with open(RAW_DIR / "loyalty_data.json", "w") as f:
    json.dump(loyalty_data, f, indent=2)
print(f"    {len(loyalty_members)} loyalty members")

print("\n   Mock data generated successfully!")
print(f"    Files written to {RAW_DIR.resolve()}")
