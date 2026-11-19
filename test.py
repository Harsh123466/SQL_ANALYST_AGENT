import os
import duckdb
import pandas as pd

from dotenv import load_dotenv
from sql_ai_agent.sql_agent import SqlAgent
from sql_ai_agent.chart_generator import generate_chart
from sql_ai_agent.display import display_result
from sql_ai_agent.chart_selector import select_chart


load_dotenv()

# Create DuckDB connection
db = duckdb.connect("sales.duckdb", read_only=True)

# Initialize Groq API
agent = SqlAgent(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    model=os.getenv("GROQ_MODEL"),
    tbl_name="retail_sales",
    connection=db
)

# Ask question
response = agent.ask_question(
    "Show the top 5 products by revenue"
)

display_result(response)

print("\nChart Decision:")
print(response["chart"])

generate_chart(
    response["result"],
    chart_type=response["chart"]["chart_type"]
)