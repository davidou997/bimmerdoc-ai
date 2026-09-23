import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from schemas import ExtractedEntities
from state import AgentState

# Load OPENAI_API_KEY from .env file
load_dotenv()

# Instantiate the model with zero temperature for deterministic outputs
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def input_normalizer_node(state: AgentState) -> dict:
    """
    Reads the raw input string from state and uses the LLM to extract 
    structured diagnostic entities.
    """
    raw_user_input = state.get("raw_input", "")
    
    # Bind Pydantic schema to force structured JSON extraction
    structured_llm = llm.with_structured_output(ExtractedEntities)
    
    extracted: ExtractedEntities = structured_llm.invoke(
        f"Extract diagnostic parameters from this driver query: {raw_user_input}"
    )
    
    # Return dictionary to update AgentState
    return {
        "detected_fault_codes": extracted.detected_fault_codes,
        "symptom_category": extracted.symptom_category,
        "operating_condition": extracted.operating_condition,
        "perceived_location": extracted.perceived_location
    }