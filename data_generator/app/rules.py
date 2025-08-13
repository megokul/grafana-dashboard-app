import pandas as pd
from typing import Dict, List, Any


def run_rules(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Evaluate rules for a single-row transaction DataFrame.

    Required columns:
        - amount (numeric)
        - account_blacklisted (bool)
        - trans_type (str): e.g., 'Real_time_transaction' or others

    Returns:
        dict: Single transaction with rules_triggered, rules_explanation, decision
    """
    if df.shape[0] != 1:
        raise ValueError("run_rules expects a single-row DataFrame.")

    row = df.iloc[0]
    amount = float(row["amount"])
    is_blacklisted = bool(row["account_blacklisted"])
    trans_type = str(row["trans_type"])

    rules_triggered: List[str] = []
    rules_explanation: List[str] = []
    decision = "Approved"

    # If not a real-time transaction → no rules triggered
    if trans_type != "Real_time_transaction":
        rules_triggered.append("No Rules Triggered")
    else:
        # Blacklisted account → immediate reject
        if is_blacklisted:
            rules_triggered.append("Rule2")
            rules_explanation.append("Account/card is blacklisted.")
            decision = "Rejected"

        # Amount too high → reject
        if amount >= 100:
            rules_triggered.append("Rule1")
            rules_explanation.append("Transaction amount exceeds $100 limit.")
            decision = "Rejected"

        if not rules_triggered:
            rules_triggered.append("No Rules Triggered")

    out = row.to_dict()
    out["rules_triggered"] = rules_triggered
    out["rules_explanation"] = rules_explanation
    out["decision"] = decision
    return out
