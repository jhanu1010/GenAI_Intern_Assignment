from fastapi import FastAPI, Request
import sqlite3
from llm_agent import get_sql_query_from_question
import os
import pandas as pd

app = FastAPI()

DATABASE = "ecommerce.db"
DATASETS = {
    "sales": "total_sales.csv",
    "eligibility": "eligibility.csv",
    "ads": "ad_sales.csv"
}

def load_csv_to_sqlite():
    conn = sqlite3.connect(DATABASE)
    for table, csv_file in DATASETS.items():
        df = pd.read_csv(csv_file)
        df.to_sql(table, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    print("✅ All datasets loaded into ecommerce.db")

@app.on_event("startup")
def startup_event():
    load_csv_to_sqlite()

@app.get("/")
async def root():
    return {"message": "Welcome to the AI SQL Agent"}

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question", "")
    sql_query = get_sql_query_from_question(question)
    
    if "Error" in sql_query:
        return {"error": sql_query}

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        conn.close()
        return {"query": sql_query, "result": [dict(zip(column_names, row)) for row in result]}
    except Exception as e:
        return {"error": str(e)}
