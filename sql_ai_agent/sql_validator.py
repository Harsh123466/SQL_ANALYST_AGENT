
from sqlglot import parse, exp


def validate_sql(query):
    statements = parse(query, read="duckdb")

    # Allow exactly one SQL statement
    if len(statements) != 1:
        raise ValueError("Only one SQL statement is allowed.")

    statement = statements[0]

    # Allow only SELECT queries
    if not isinstance(statement, exp.Query):
        raise ValueError("Only read-only SELECT queries are allowed.")

    return True
