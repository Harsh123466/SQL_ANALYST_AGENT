from typing import TypedDict, Optional
import pandas as pd


class AgentState(TypedDict):
    question: str
    query: str
    error: Optional[str]
    result: Optional[pd.DataFrame]
    retry_count: int
    status: str
    execution_history: list