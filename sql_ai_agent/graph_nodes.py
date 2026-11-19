from sql_ai_agent.sql_validator import validate_sql


def generate_sql_node(state, groq):
    """Generate SQL from the user's question."""

    query = groq.send_prompt(state["question"])
    # query = "SELECT * FROM retail_sales"

    return {
        "query": query,
        "error": None,
        "result": None,
        "retry_count": 0
    }


def execute_sql_node(state, connection):
    """Validate and execute the generated SQL."""

    attempt = state["retry_count"] + 1
    print(f"\nExecution attempt: {attempt}")

    history = state.get("execution_history", [])

    try:
        query = state["query"]

        safe_query = validate_sql(query)

        print("Original SQL:", query)
        print("Validated SQL:", safe_query)

        result = connection.execute(safe_query).df()

        history = history + [{
            "attempt": attempt,
            "query": safe_query,
            "status": "success",
            "error": None
        }]

        print("SQL executed successfully!")

        return{
            "result":result,
            "error":None,
            "status": "success",
            "execution_history": history
        }
    except Exception as e:

        history = history + [{
            "attempt": attempt,
            "query": safe_query,
            "status": "failed",
            "error": str(e)
        }]

        print(f"SQL execution failed: {e}")

        return {
            "result": None,
            "error": str(e),
            "status": "failed",
            "execution_history": history
        }



def correct_sql_node(state, groq):
    """Ask Groq to correct SQL after an execution error."""

    corrected_query = groq.fix_sql(
        question=state["question"],
        wrong_query=state["query"],
        error_message=state["error"]
    )

    return {
        "query": corrected_query,
        "retry_count": state['retry_count'] + 1,
        "error": None
    }