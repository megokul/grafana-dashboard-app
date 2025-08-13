INSERT INTO banking_data (
    timestamp, uniq_id, trans_type, amount, amount_crr, account_holder_name,
    card_presense, merchant_category, card_type, card_id, account_id,
    account_blacklisted, rules_triggered, rules_explanation, decision
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
