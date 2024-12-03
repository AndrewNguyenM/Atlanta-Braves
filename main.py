import pandas as pd
import sqlite3
import requests

# Fetch data from StatsAPI
def fetch_statsapi_data():
    url = "https://statsapi.mlb.com/api/v1/stats?stats=season&group=pitching&playerPool=all&season=2018&teamId=144"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    players = [
        {
            "playerId": rec["player"]["id"],
            "playerName": rec["player"]["fullName"],
            **rec["stat"]
        }
        for rec in data["stats"][0]["splits"]
    ]
    return pd.DataFrame(players)

# Normalize names for consistent comparison
def normalize_name(name):
    parts = name.split(", ")
    return f"{parts[1]} {parts[0]}" if len(parts) > 1 else name

# Compare API data with database and generate reports
def reconcile_and_report(api_df, db_path, full_output_csv, diff_output_csv):
    # Load database data
    conn = sqlite3.connect(db_path)
    db_df = pd.read_sql_query("SELECT * FROM PITCHBYPITCH", conn)
    conn.close()

    # Normalize names for comparison
    api_df["normalizedName"] = api_df["playerName"].apply(normalize_name)
    db_df["normalizedName"] = db_df["PitcherName"].apply(normalize_name)

    # Merge the two DataFrames
    merged = api_df.merge(
        db_df,
        on="normalizedName",
        how="outer",
        suffixes=("_api", "_db"),
        indicator=True
    )

    # Add columns to identify stat discrepancies (if relevant columns exist)
    for stat in ["ERA", "strikeouts", "inningsPitched"]:  # Example stats to check
        if stat in api_df.columns and stat in db_df.columns:
            merged[f"{stat}_discrepancy"] = merged[f"{stat}_api"] != merged[f"{stat}_db"]

    # Save the full reconciliation report to CSV
    merged.to_csv(full_output_csv, index=False)

    # Filter rows with discrepancies or mismatches
    discrepancies = merged[
        (merged["_merge"] != "both") |  # Rows that don't match on normalized names
        merged.filter(like="_discrepancy").any(axis=1)  # Rows with stat discrepancies
    ]

    # Save discrepancies to a separate CSV
    discrepancies.to_csv(diff_output_csv, index=False)

    # Analyze findings and summarize
    summary = {
        "total_api_records": len(api_df),
        "total_db_records": len(db_df),
        "both_records": len(merged[merged["_merge"] == "both"]),
        "api_only_records": len(merged[merged["_merge"] == "left_only"]),
        "db_only_records": len(merged[merged["_merge"] == "right_only"])
    }

    print("Reconciliation Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")

    # Interesting findings
    print("\nInteresting Findings:")
    if summary["api_only_records"] > 0:
        print(f"Found {summary['api_only_records']} players in the API but not in the database.")
    if summary["db_only_records"] > 0:
        print(f"Found {summary['db_only_records']} players in the database but not in the API.")
    stat_discrepancies = [
        col for col in merged.columns if col.endswith("_discrepancy")
    ]
    if stat_discrepancies:
        print("Found discrepancies in the following stats:")
        print(", ".join(stat_discrepancies))

    return summary

# Main execution
api_data = fetch_statsapi_data()
full_output_csv = "reconciliation_report.csv"
diff_output_csv = "discrepancy_report.csv"
db_path = "/Users/andrewnguyen/Desktop/Braves/db01/main" # Please adjust to file path of the db on your local PC
summary = reconcile_and_report(api_data, db_path, full_output_csv, diff_output_csv)

