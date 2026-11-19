
from sqlglot import parse, exp

MAX_ROWS = 500

ALLOWED_TABLES = {
    "retail_sales",
    "regional_sales"
}


def validate_sql(query):
    statements = parse(query, read="duckdb")

    # Allow exactly one SQL statement
    if len(statements) != 1 or statements[0] is None:
        raise ValueError("Only one SQL statement is allowed.")

    statement = statements[0]

    # Allow only SELECT queries
    if not isinstance(statement, exp.Query):
        raise ValueError("Only read-only SELECT queries are allowed.")

    # Check table access
    tables = statement.find_all(exp.Table)

    for table in tables:
        table_name = table.name.lower()

        if table_name not in ALLOWED_TABLES:
            raise ValueError(
                f"Access to table '{table_name}' is not allowed."
            )

    # Enforce row limit
    if not statement.args.get("limit"):
        statement = statement.limit(MAX_ROWS)

    return statement.sql(dialect="duckdb")

