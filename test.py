import os
import duckdb
import pandas as pd

from dotenv import load_dotenv
from sql_ai_agent.sql_agent import SqlAgent

load_dotenv()

# Create DuckDB connection
db = duckdb.connect("sales.duckdb")

# Initialize Groq API
agent = SqlAgent(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    model=os.getenv("GROQ_MODEL"),
    tbl_name="retail_sales",
    connection=db
)

# Ask question
result = agent.ask_question(
    "Show total sales by product category"
)

print(result)