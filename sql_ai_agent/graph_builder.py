from langgraph.graph import StateGraph, START, END

from sql_ai_agent.graph_state import AgentState
from sql_ai_agent.graph_nodes import (
    generate_sql_node,
    execute_sql_node,
    correct_sql_node
)


def build_sql_graph(groq, connection, max_attempts=3):

    # create the graph
    workflow = StateGraph(AgentState)

    workflow.add_node(
        "generate_sql", 
        lambda state: generate_sql_node(state, groq)
    )

    workflow.add_node(
        "execute_sql",
        lambda state: execute_sql_node(state, connection)
    )

    workflow.add_node(
        "correct_sql",
        lambda state: correct_sql_node(state, groq)
    )

    workflow.add_edge(START, "generate_sql")
    workflow.add_edge("generate_sql","execute_sql")

    # Decide whether to retry or finish
    def check_result(state):
        if state["error"] is None:
            return "end"

        if state["retry_count"] < max_attempts - 1:
            return "correct"

        return "end"

    workflow.add_conditional_edges(
        "execute_sql",
        check_result,
        {
            "correct": "correct_sql",
            "end": END
        }
    )

    # Correct SQL -> Execute SQL again
    workflow.add_edge("correct_sql", "execute_sql")

    # Compile the graph
    return workflow.compile()
