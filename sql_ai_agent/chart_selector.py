
import json


def select_chart(groq, question, result):

    columns = result.dtypes.astype(str).to_dict()

    prompt = f"""
    You are a data visualization expert.

    User question:
    {question}

    Result columns and data types:
    {columns}

    Sample result:
    {result.head(5).to_string(index=False)}

    Choose the most suitable chart type.

    Available chart types:
    - bar
    - line
    - pie
    - none

    Rules:
    1. Use bar for comparing categories.
    2. Use line for trends over time or ordered sequences.
    3. Use pie for proportions of a whole with a small number of categories.
    4. Use none when a chart is not useful.
    5. Do not choose pie for negative values.
    6. Return only valid JSON.

    Required JSON format:
    {{
        "chart_type": "bar",
        "reason": "Comparing revenue across products"
    }}
    """

    response = groq.client.chat.completions.create(
        model=groq.model,
        messages=[
            {
                "role": "system",
                "content": "Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    if not content:
        return {"chart_type": "none", "reason": "Empty LLM response"}

    try:
        decision = json.loads(content.strip())
    except json.JSONDecodeError:
        return {"chart_type": "none", "reason": "Invalid JSON"}

    allowed_types = {"bar", "line", "pie", "none"}

    if decision.get("chart_type") not in allowed_types:
        return {"chart_type": "none", "reason": "Unsupported chart type"}

    return decision
