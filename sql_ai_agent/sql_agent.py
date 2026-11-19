
from sql_ai_agent.api_handler import GroqAPI


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

    def ask_question(self, question):
        # Generate SQL using Groq
        query = self.groq.send_prompt(question)

        # Execute SQL using DuckDB
        result = self.connection.execute(query).df()

        return result
