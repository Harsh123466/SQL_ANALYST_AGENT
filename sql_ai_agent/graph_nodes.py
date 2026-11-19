from sql_ai_agent.sql_validator import validate_sql


def generate_sql_node(state, groq):
    """Generate SQL from the user's question."""

    query = groq.send_prompt(state["question"])
    # query = "SELECT InvalidColumn FROM retail_sales"

    return {
        "query": query,
        "error": None,
        "result": None,
        "retry_count": 0
    }


def execute_sql_node(state, connection):
    """Validate and execute the generated SQL."""

    try:
        query = state["query"]
        validate_sql(query)

        result = connection.execute(query).df()

        return{
            "result":result,
            "error":None
        }
    except Exception as e:
        return {
            "result": None,
            "error": str(e)
        }


def correct_sql_node(state, groq):
    """Ask Groq to correct SQL after an execution error."""

    corrected_query = groq.fix_sql(
        question=state["question"],
        wrong_query=state["query"],
        error_message=state["error"]
    )
    print(f"attempt: {state['retry_count']+1}")

    return {
        "query": corrected_query,
        "retry_count": state['retry_count'] + 1,
        "error": None
    }