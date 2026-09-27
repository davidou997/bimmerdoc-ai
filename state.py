from typing import TypedDict, Annotated, List, Optional
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Represents the state of an agent.
    """

    # Input provided by client
    raw_input: str

    # Data extracted from input normalizer node
    detected_fault_codes: List[str]
    symptom_category: Optional[str]
    operating_condition: Optional[str]
    perceived_location: Optional[str]

    # State variables
    retrieved_context: List[str] # List of context retrieved from the knowledge base (RAG)
    diagnostic_candidates: List[dict] # List of potential diagnostic solutions
    part_recommendations: List[dict] # List of recommended parts