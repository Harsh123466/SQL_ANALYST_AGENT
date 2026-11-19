import os
import duckdb
import pandas as pd

from dotenv import load_dotenv
from sql_ai_agent.api_handler import GroqAPI

load_dotenv()

# Create DuckDB connection
db = duckdb.connect("sales.duckdb")

# Load datasets
retail_sales = pd.read_csv(
    "data/Red30 Tech US online retail sales.csv"
)

regional_sales = pd.read_csv(
    "data/Red30 Tech US sales by region.csv"
)

# Register datasets
db.register("retail_sales", retail_sales)
db.register("regional_sales", regional_sales)

# Initialize Groq API
groq = GroqAPI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    model=os.getenv("GROQ_MODEL"),
    tbl_name="retail_sales",
    connection=db
)

# Ask question
query = groq.send_prompt(
    "Show the first 5 rows from retail_sales"
)

print(query)

print("Generated SQL:")
print(query)

result = db.execute(query).df()

print("\nQuery Result:")
print(result)