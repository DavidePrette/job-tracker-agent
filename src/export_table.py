import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = "data/jobs.db"
OUT_PATH = Path("data/tracked_jobs.csv")


def export_jobs_table() -> None:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT
            first_seen,
            last_seen,
            organization,
            title,
            location,
            posted_date,
            matched_keywords,
            relevance_score,
            url
        FROM jobs
        ORDER BY first_seen DESC, relevance_score DESC, organization ASC
    """, conn)
    conn.close()

    print(f"Rows in jobs table: {len(df)}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"Exported cumulative job table to {OUT_PATH}")


if __name__ == "__main__":
    export_jobs_table()