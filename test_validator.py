
from sql_ai_agent.sql_validator import validate_sql

queries = [
    "SELECT * FROM retail_sales",
    "SELECT SUM(OrderTotal) FROM retail_sales",
    "DELETE FROM retail_sales",
    "DROP TABLE retail_sales"
]

for query in queries:
    try:
        validate_sql(query)
        print("ALLOWED:", query)

    except ValueError as e:
        print("BLOCKED:", query, "|", e)
