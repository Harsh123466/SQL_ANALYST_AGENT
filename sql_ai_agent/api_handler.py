from openai import OpenAI
from sql_ai_agent import prompt_handler as ph


class GroqAPI:
    def __init__(self, api_key, base_url, model, tbl_name, connection, max_token=5000):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.tbl_name = tbl_name
        self.connection = connection
        self.max_token = max_token

        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.system = ph.system_prompt(connection=self.connection, tbl_name=tbl_name)

    def send_prompt(self, question):
        self.user = ph.user_prompt(question=question)

        self.response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system.system},
                {"role": "user", "content": self.user},
            ],
            max_completion_tokens=self.max_token
        )

        content = self.response.choices[0].message.content

        return content