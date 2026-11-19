
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

    def ask_question(self, question, max_retries=3):

        # Generate SQL using Groq
        query = self.groq.send_prompt(question)
        # query = "SELECT InvalidColumn FROM retail_sales"

        for attempt in range(max_retries):

            try:
                print(f"Attempt {attempt+1}: Executing SQL....")

                # Execute SQL using DuckDB
                result = self.connection.execute(query).df()

                print("Query executed successfully!")

                return result

            except Exception as e:

                print(f"SQL Error: {e}")

                if attempt == max_retries - 1:
                    raise Exception("Maximum retries reached. SQL execution failed.")

                print("Asking Groq to correct the SQL...")

                query = self.groq.fix_sql(
                    question=question,
                    wrong_query=query,
                    error_message=str(e)
                )
