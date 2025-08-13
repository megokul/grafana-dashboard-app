import random
from faker import Faker
import pandas as pd
from typing import Dict, Any, List, Tuple
from datetime import datetime

FAKER = Faker()

MERCHANT_CATEGORIES = [
    "Retail", "Electronics", "Clothing", "Groceries", "Pharmacy",
    "Entertainment", "Dining", "Travel", "Utilities", "Healthcare"
]

CARD_TYPES = {"visa": "visa", "mastercard": "mastercard"}


def generate_record() -> Dict[str, list]:
    """
    Generate a single synthetic transaction as dict-of-lists for 1-row DataFrame.
    """
    card_type = random.choice(list(CARD_TYPES.keys()))
    return {
        "uniq_id": [FAKER.uuid4()],
        "trans_type": [random.choice(["Real_time_transaction", "settlements", "dispute"])],
        "amount": [round(random.uniform(10.0, 1000.0), 2)],
        "amount_crr": [round(random.uniform(10.0, 1000.0), 2)],
        "account_holder_name": [FAKER.name()],
        "card_presense": [random.choice(["Present", "Not Present"])],
        "merchant_category": [random.choice(MERCHANT_CATEGORIES)],
        "card_type": [card_type],
        "card_id": [FAKER.credit_card_number(card_type=CARD_TYPES[card_type])],
        "account_id": [FAKER.uuid4()],
        "account_blacklisted": [random.choice([True, False])]
    }


def normalize_rule_field(value: Any, sep: str = ",") -> str:
    """
    Convert rule fields (which might be list/None/str) to a short string suitable for VARCHAR columns.
    """
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return sep.join([str(v) for v in value])
    return str(value)


def build_rows(batch_size: int, run_rules_func, timestamp: datetime) -> List[Tuple]:
    """
    Generate a batch of rows for insertion.
    """
    rows: List[Tuple] = []
    for _ in range(batch_size):
        df = pd.DataFrame(generate_record())
        rec = run_rules_func(df)

        rows.append((
            timestamp,
            rec["uniq_id"], rec["trans_type"], rec["amount"], rec["amount_crr"],
            rec["account_holder_name"], rec["card_presense"], rec["merchant_category"],
            rec["card_type"], rec["card_id"], rec["account_id"], rec["account_blacklisted"],
            normalize_rule_field(rec.get("rules_triggered"), ","),
            normalize_rule_field(rec.get("rules_explanation"), " | "),
            rec["decision"]
        ))
    return rows
