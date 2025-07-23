import os
from dotenv import load_dotenv
load_dotenv()

import openai
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_sql_query_from_question(question: str) -> str:
    prompt = f"""
You are a helpful assistant that converts English questions into SQL queries.
Assume the database is called 'ecommerce.db' and contains these tables:
- sales(product_id, quantity, revenue)
- products(product_id, product_name, cpc)
- ads(product_id, ad_spend)

Translate the following question into an SQL query. ONLY return the SQL code.

Question: {question}
SQL:
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
