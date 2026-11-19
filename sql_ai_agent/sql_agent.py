from sql_ai_agent.api_handler import GroqAPI
from sql_ai_agent.sql_validator import validate_sql
from sql_ai_agent.graph_builder import build_sql_graph
from sql_ai_agent.answer_generator import generate_answer
from sql_ai_agent.chart_selector import select_chart


class SqlAgent:
    def __init__(self, api_key, base_url, model, tbl_name, connection):
        self.connection = connection

        self.groq = GroqAPI(
            api_key=api_key,
            base_url=base_url,
            model=model,
            tbl_name=tbl_name,
            connection=connection
        )

        self.graph = build_sql_graph(
            groq=self.groq,
            connection=self.connection,
            max_attempts=3
        )

    def ask_question(self, question):

        initial_state = {
            "question": question,
            "query": "",
            "error": None,
            "result": None,
            "retry_count": 0,
            "status": "pending",
            "execution_history": []
        }

        final_state = self.graph.invoke(initial_state)

        print("\nExecution History:")

        for item in final_state["execution_history"]:
            print(item)

        if final_state["error"]:
            raise Exception(
                f"SQL execution failed: {final_state['error']}"
            )

        result = final_state["result"]

        answer = generate_answer(
            groq=self.groq,
            question=question,
            result=result
        )

        chart_decision = select_chart(
            groq=self.groq,
            question=question,
            result=result
        )

        return {
            "question": question,
            "sql": final_state["query"],
            "result": result,
            "answer": answer,
            "chart": chart_decision,
            "execution_history": final_state["execution_history"]
        }
