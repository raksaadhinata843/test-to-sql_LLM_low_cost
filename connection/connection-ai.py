import duckdb
import os
from google import genai

def text_to_sql_chat():
    # 1. Koneksi ke MotherDuck
    md_token = os.environ.get('MD_TOKEN')
    con = duckdb.connect(f'md:?md_token={md_token}')
    
    # 2. Ambil Schema 
    schema_info = con.execute("DESCRIBE silver_company_profiles").fetchall()
    
    # 3. Setup LLM
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    model_id = "gemini-2.0-flash"

    user_question = "Ada berapa banyak perusahaan yang terdaftar di exchange NASDAQ?"

    # 4. Crafting the Prompt
    prompt = f"""
    You are a SQL expert. Given the following table schema in MotherDuck:
    Table: silver_company_profiles
    Columns: {schema_info}
    
    Write a DuckDB SQL query to answer this question: {user_question}
    Return ONLY the SQL query, no explanation, no backticks.
    """

    # 5. LLM Generate SQL
    sql_query = model.generate_content(prompt).text.strip()
    print(f"Generated SQL: {sql_query}")

    # 6. Jalankan di MotherDuck
    try:
        result = con.execute(sql_query).fetchall()
        print(f"Answer: {result}")
    except Exception as e:
        print(f"SQL Error: {e}")

if __name__ == "__main__":
    text_to_sql_chat()
