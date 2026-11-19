
import duckdb
import pandas as pd

# Connect to database
db = duckdb.connect("sales.duckdb")

# Load CSV files
retail_sales = pd.read_csv(
    "data/Red30 Tech US online retail sales.csv"
)

regional_sales = pd.read_csv(
    "data/Red30 Tech US sales by region.csv"
)

# Create permanent tables
db.execute("""
    CREATE OR REPLACE TABLE retail_sales AS
    SELECT * FROM retail_sales
""")

db.execute("""
    CREATE OR REPLACE TABLE regional_sales AS
    SELECT * FROM regional_sales
""")

# Verify tables
print(db.execute("SHOW TABLES").df())

print("Retail rows:", db.execute(
    "SELECT COUNT(*) FROM retail_sales"
).fetchone()[0])

print("Regional rows:", db.execute(
    "SELECT COUNT(*) FROM regional_sales"
).fetchone()[0])

db.close()
