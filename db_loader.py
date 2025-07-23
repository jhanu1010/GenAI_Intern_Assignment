import sqlite3
import pandas as pd

def load_csv_to_sqlite():
    conn = sqlite3.connect("ecommerce.db")

    pd.read_csv("ad_sales.csv").to_sql("ad_sales", conn, if_exists="replace", index=False)
    pd.read_csv("eligibility.csv").to_sql("eligibility", conn, if_exists="replace", index=False)
    pd.read_csv("total_sales.csv").to_sql("total_sales", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()
    print("✅ All datasets loaded into ecommerce.db")
