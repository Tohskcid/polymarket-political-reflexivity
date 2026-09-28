#!/usr/bin/env python3
"""Build analysis-ready national time series and state-level panel datasets from raw data."""

import datetime
import hashlib
import json
from pathlib import Path
import pandas as pd
import numpy as np

def ts_to_date(ts: int) -> str:
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%Y-%m-%d")

def main():
    root = Path(__file__).resolve().parent.parent.parent
    raw_dir = root / "data" / "raw"
    processed_dir = root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    print("1. Loading raw data...")
    with open(raw_dir / "polymarket_national_daily.json", "r", encoding="utf-8") as f:
        poly_nat = json.load(f)

    with open(raw_dir / "polymarket_swing_states_daily.json", "r", encoding="utf-8") as f:
        poly_states = json.load(f)

    with open(raw_dir / "campaign_shocks_timeline.json", "r", encoding="utf-8") as f:
        events = json.load(f)

    polls_raw = pd.read_csv(raw_dir / "fivethirtyeight_polls_2024.csv")
    polls_2024 = polls_raw[polls_raw["cycle"] == 2024].copy()

    # Process National Polymarket Data
    print("2. Processing National Polymarket data...")
    rep_series = {ts_to_date(x["t"]): x["p"] for x in poly_nat["party_rep"]}
    dem_series = {ts_to_date(x["t"]): x["p"] for x in poly_nat["party_dem"]}
    trump_series = {ts_to_date(x["t"]): x["p"] for x in poly_nat.get("trump", [])}
    harris_series = {ts_to_date(x["t"]): x["p"] for x in poly_nat.get("harris", [])}
    biden_series = {ts_to_date(x["t"]): x["p"] for x in poly_nat.get("biden", [])}

    all_dates = sorted(set(rep_series.keys()) | set(dem_series.keys()) | set(trump_series.keys()))
    dates_2024 = [d for d in all_dates if "2024-01-01" <= d <= "2024-11-06"]

    nat_rows = []
    for d in dates_2024:
        p_rep = rep_series.get(d, np.nan)
        p_dem = dem_series.get(d, np.nan)
        p_trump = trump_series.get(d, np.nan)
        p_harris = harris_series.get(d, np.nan)
        p_biden = biden_series.get(d, np.nan)

        poly_margin = (p_rep - p_dem) if (pd.notna(p_rep) and pd.notna(p_dem)) else np.nan

        nat_rows.append({
            "date": d,
            "poly_rep": p_rep,
            "poly_dem": p_dem,
            "poly_trump": p_trump,
            "poly_harris": p_harris,
            "poly_biden": p_biden,
            "poly_margin": poly_margin
        })

    df_nat_poly = pd.DataFrame(nat_rows)

    # Process National Polling Data from 538 using pct_estimate
    print("3. Processing FiveThirtyEight national polling averages...")
    nat_polls = polls_2024[polls_2024["state"] == "National"].copy()
    
    piv = nat_polls.pivot_table(
        index="date", 
        columns="candidate", 
        values="pct_estimate", 
        aggfunc="mean"
    )
    piv.columns.name = None
    pivot_polls = piv.reset_index()

    pivot_polls["poll_trump"] = pivot_polls["Trump"] if "Trump" in pivot_polls.columns else np.nan
    pivot_polls["poll_biden"] = pivot_polls["Biden"] if "Biden" in pivot_polls.columns else np.nan
    pivot_polls["poll_harris"] = pivot_polls["Harris"] if "Harris" in pivot_polls.columns else np.nan

    dem_candidates = []
    for _, r in pivot_polls.iterrows():
        d = r["date"]
        if d >= "2024-07-21":
            val = r["poll_harris"] if pd.notna(r["poll_harris"]) else r["poll_biden"]
        else:
            val = r["poll_biden"] if pd.notna(r["poll_biden"]) else r["poll_harris"]
        dem_candidates.append(val)

    pivot_polls["poll_dem"] = dem_candidates
    pivot_polls["poll_margin"] = pivot_polls["poll_trump"] - pivot_polls["poll_dem"]

    # Merge National Polymarket + Polling
    df_nat = pd.merge(df_nat_poly, pivot_polls[["date", "poll_trump", "poll_dem", "poll_margin"]], on="date", how="left")

    # Forward-fill minor gaps and post-Sep 12 window
    df_nat["poll_trump"] = df_nat["poll_trump"].ffill()
    df_nat["poll_dem"] = df_nat["poll_dem"].ffill()
    df_nat["poll_margin"] = df_nat["poll_margin"].ffill()

    # Add Event Shocks
    event_dates = {e["date"]: e["event"] for e in events}
    df_nat["event"] = df_nat["date"].map(event_dates).fillna("")
    df_nat["is_debate"] = df_nat["date"].isin(["2024-06-27", "2024-09-10"]).astype(int)
    df_nat["is_assassination"] = (df_nat["date"] == "2024-07-13").astype(int)
    df_nat["is_biden_exit"] = (df_nat["date"] == "2024-07-21").astype(int)
    df_nat["is_whale_surge"] = (df_nat["date"] >= "2024-10-05").astype(int)

    # First differences
    df_nat["d_poly_margin"] = df_nat["poly_margin"].diff()
    df_nat["d_poll_margin"] = df_nat["poll_margin"].diff()

    # Save National Dataset
    nat_csv = processed_dir / "national_daily_analysis.csv"
    df_nat.to_csv(nat_csv, index=False)
    print(f"  Saved national analysis dataset to {nat_csv} ({len(df_nat)} rows)")

    # Process State-Level Panel Dataset
    print("\n4. Processing Swing States Panel Data...")
    state_abbr_to_name = {
        "PA": "Pennsylvania",
        "MI": "Michigan",
        "WI": "Wisconsin",
        "GA": "Georgia",
        "AZ": "Arizona",
        "NV": "Nevada",
        "NC": "North Carolina"
    }

    panel_rows = []
    for st, sname in state_abbr_to_name.items():
        st_info = poly_states[st]
        st_dem = {ts_to_date(x["t"]): x["p"] for x in st_info["dem_history"]}
        st_rep = {ts_to_date(x["t"]): x["p"] for x in st_info["rep_history"]}

        st_polls = polls_2024[polls_2024["state"] == sname].copy()
        if not st_polls.empty:
            piv_st = st_polls.pivot_table(index="date", columns="candidate", values="pct_estimate", aggfunc="mean")
            piv_st.columns.name = None
            piv_st = piv_st.reset_index()

            piv_st["poll_trump"] = piv_st["Trump"] if "Trump" in piv_st.columns else np.nan
            piv_st["poll_biden"] = piv_st["Biden"] if "Biden" in piv_st.columns else np.nan
            piv_st["poll_harris"] = piv_st["Harris"] if "Harris" in piv_st.columns else np.nan

            dem_st_vals = []
            for _, r in piv_st.iterrows():
                d = r["date"]
                if d >= "2024-07-21":
                    val = r["poll_harris"] if pd.notna(r["poll_harris"]) else r["poll_biden"]
                else:
                    val = r["poll_biden"] if pd.notna(r["poll_biden"]) else r["poll_harris"]
                dem_st_vals.append(val)

            piv_st["poll_dem"] = dem_st_vals
            piv_st["poll_margin"] = piv_st["poll_trump"] - piv_st["poll_dem"]
            poll_dict = {r["date"]: (r["poll_trump"], r["poll_dem"], r["poll_margin"]) for _, r in piv_st.iterrows()}
        else:
            poll_dict = {}

        common_st_dates = sorted(set(st_rep.keys()) | set(st_dem.keys()))
        for d in common_st_dates:
            p_r = st_rep.get(d, np.nan)
            p_d = st_dem.get(d, np.nan)
            pm = (p_r - p_d) if (pd.notna(p_r) and pd.notna(p_d)) else np.nan
            
            p_trump, p_dem, pl_m = poll_dict.get(d, (np.nan, np.nan, np.nan))
            competitiveness = 1.0 - abs(pm) if pd.notna(pm) else np.nan

            panel_rows.append({
                "date": d,
                "state": st,
                "state_name": sname,
                "poly_rep": p_r,
                "poly_dem": p_d,
                "poly_margin": pm,
                "poll_trump": p_trump,
                "poll_dem": p_dem,
                "poll_margin": pl_m,
                "competitiveness": competitiveness
            })

    df_panel = pd.DataFrame(panel_rows)
    # Forward fill state polls
    df_panel["poll_trump"] = df_panel.groupby("state")["poll_trump"].ffill()
    df_panel["poll_dem"] = df_panel.groupby("state")["poll_dem"].ffill()
    df_panel["poll_margin"] = df_panel.groupby("state")["poll_margin"].ffill()

    # Differences by state
    df_panel["d_poly_margin"] = df_panel.groupby("state")["poly_margin"].diff()
    df_panel["d_poll_margin"] = df_panel.groupby("state")["poll_margin"].diff()

    panel_csv = processed_dir / "swing_states_panel.csv"
    df_panel.to_csv(panel_csv, index=False)
    print(f"  Saved swing states panel dataset to {panel_csv} ({len(df_panel)} rows across 7 states)")

    # Compute checksums for processed data
    print("\n5. Computing SHA-256 Checksums for data/processed/...")
    proc_checksums = {}
    for p in [nat_csv, panel_csv]:
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        proc_checksums[p.name] = h
        print(f"  {p.name}: {h}")

    with open(processed_dir / "checksums.sha256", "w", encoding="utf-8") as f:
        for fname, h in proc_checksums.items():
            f.write(f"{h}  {fname}\n")

if __name__ == "__main__":
    main()
