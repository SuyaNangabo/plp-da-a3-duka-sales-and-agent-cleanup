import pandas as pd


def clean_agent_data(txns, agents, suspect_amount=250000):
    """Clean the agent transactions extract.

    Removes duplicate transactions, standardises txn_type, converts amount
    and txn_date, imputes missing amounts with the median, flags IQR
    outliers and suspected entry errors, and merges in the agent county.

    Returns (clean_df, log).
    """
    log = []

    # Uniqueness: one row per transaction ID
    out = txns.drop_duplicates(subset="txn_id", keep="first").copy()
    log.append(f"Uniqueness: removed {len(txns) - len(out)} duplicate transactions")

    # Consistency: exactly two transaction types
    before = (~out["txn_type"].isin(["Deposit", "Withdrawal"])).sum()
    out["txn_type"] = out["txn_type"].str.strip().str.title()
    log.append(f"Consistency: standardised txn_type in {before} rows")

    # Validity: amount to numbers, N/A and blanks become missing
    out["amount"] = pd.to_numeric(out["amount"], errors="coerce")

    # Outliers: IQR method on the real amounts, before imputation
    q1, q3 = out["amount"].quantile([0.25, 0.75])
    upper = q3 + 1.5 * (q3 - q1)
    out["is_outlier"] = out["amount"] > upper
    out["suspected_entry_error"] = out["amount"] == suspect_amount
    log.append(f"Accuracy: flagged {out['is_outlier'].sum()} IQR outliers "
               f"above KES {upper:,.0f}")
    log.append(f"Accuracy: flagged {out['suspected_entry_error'].sum()} amounts of "
               f"KES {suspect_amount:,} as suspected entry errors")

    # Completeness: flag first, then fill with the median
    out["amount_imputed"] = out["amount"].isna()
    median = out.loc[~out["suspected_entry_error"], "amount"].median()
    out["amount"] = out["amount"].fillna(median)
    log.append(f"Completeness: imputed {out['amount_imputed'].sum()} missing or "
               f"invalid amounts with the median of KES {median:,.0f}")

    # Validity: one ISO date format
    bad_dates = out["txn_date"].astype(str).str.contains("/").sum()
    out["txn_date"] = pd.to_datetime(out["txn_date"].astype(str).str.replace("/", "-"))
    log.append(f"Validity: fixed {bad_dates} dates written with /")

    # Merge with the agent register
    out = out.merge(agents[["agent_id", "county"]], on="agent_id",
                    how="left", indicator=True)
    out["unknown_agent"] = out["_merge"] == "left_only"
    out["county"] = out["county"].fillna("Unknown")
    out = out.drop(columns="_merge")
    log.append(f"Validity: {out['unknown_agent'].sum()} transactions have agents "
               "missing from the register, kept with county Unknown")

    return out, log
