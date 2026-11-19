
import pandas as pd


def generate_answer(groq, question, result):

    # Convert DataFrame into text
    result_text = result.to_string(index=False)

    prompt = f"""
    You are an AI Data Analyst.

    Answer the user's business question using only the
    SQL query result provided below.

    User Question:
    {question}

    SQL Query Result:
    {result_text}

    Instructions:
    1. Give a concise and clear business explanation.
    2. Highlight important findings.
    3. Include relevant numbers.
    4. Do not invent or assume information.
    5. If the result is empty, clearly say no records were found.
    6. Keep the answer under 150 words.

    Business Answer:
    """

    response = groq.client.chat.completions.create(
        model=groq.model,
        messages=[
            {
                "role": "system",
                "content": "You are a professional business data analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    if not answer:
        raise ValueError("Groq returned an empty answer.")

    return answer.strip()
