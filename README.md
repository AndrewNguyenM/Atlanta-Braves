
# StatsAPI Data Reconciliation Tool
This Python tool fetches pitching statistics data from the MLB StatsAPI and compares it with an existing SQLite database table (PITCHBYPITCH). The tool generates CSV files for a full reconciliation report and a detailed discrepancy report, highlighting any differences between the API data and the database.

## Features
1. **Fetch Data from StatsAPI**: The tool retrieves player pitching stats for a specific season and team from the StatsAPI.
2. **Compare API Data with SQLite Database**: Matches records using normalized player names and compares stats across the two datasets.
3. **Generate Reports**:
   - **`reconciliation_report.csv`**: A full report showing all players and stats from both sources, with a column indicating the data source (`both`, `API only`, or `DB only`).
   - **`discrepancy_report.csv`**: A focused report of only the differences between the two datasets, including mismatched stats and records exclusive to one source.
4. **Identify Data Source**: Each record in the reports includes an indicator of whether it originated from the API, database, or both.

## IMPORANT!!!

In the code there is a line that takes the database locally from your PC so the line where it says db_path = "change/path/to/file/locally" just change the file path to what it is on your pc.

**Make sure within SQLite to do `.mode column` for the proper column headers to appear**

---
## Requirements

- Python 3.8 or higher
- SQLite database with a `PITCHBYPITCH` table
- Libraries:
  - `pandas`
  - `sqlite3`
  - `requests`

## CSV files context
**`statsapi_reconciliation.py`**: Main script for fetching, comparing, and generating reports.

* **`reconciliation_report.csv`**:
  - Contains player ID, player name, all stats from the API and database, and a `_merge` column indicating the data source:
    - `"both"`: Exists in both API and database.
    - `"left_only"`: Exists only in the API.
    - `"right_only"`: Exists only in the database.

* **`discrepancy_report.csv`**:
  - Focuses on differences between the API and database.
  - Includes mismatched stats, as well as records exclusive to one source.


## Possible Future Improvements

* **Automated Data Audit**:
    - Set up a scheduler (e.g. `Airflow`, `AWS`, `Azure`) to have the script update on a day to day basis for the most up to date data.

* **More Descriptive Stats**:
    - Adding more data such as strikeouts to present to coaches so that they can be more informed to make the correct decisions

* **Visualization**:
    - Creating visualizations for coaches and players and other team members to help get everyone on the same page and help pushing business decisions



# Contact
If you have any questions feel free to reach out at nguye938@msu.edu

