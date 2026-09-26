# BimmerDoc AI - Architectural & System Design Blueprint

## 1. Core Tech Stack & Frameworks
- **Language:** Python 3.x (Modern backend standards)
- **API Framework:** FastAPI (Asynchronous REST endpoints and Server-Sent Events streaming)
- **Agent Orchestration:** LangGraph (Deterministic state machine; explicit nodes and edges for controlled agent execution loops)
- **LLM Provider & Orchestration:** OpenAI (`gpt-4o-mini` via `langchain-openai` for cost-effective tool calling and structured reasoning)
- **Data & Storage:** PostgreSQL with `pgvector` extension for hybrid vector search (RAG) over technical service bulletins and repair documentation.
- **Cloud & Secrets:** AWS Secrets Manager (`bimmerdoc/openai-key`) accessed securely via `boto3[crt]` and local OS credential chains (`~/.aws/credentials`).

## 2. Key Design Patterns & Architectural Constraints
- **State Management:** All agent progress, symptoms, tool outputs, and execution states are tracked through a central Pydantic-backed `AgentState` dictionary (`state.py`).
- **Structured Outputs:** Pydantic schemas (`schemas.py`) are strictly enforced during LLM generation and tool execution to guarantee zero-hallucination data payloads.
- **Security & Least Privilege:** No `.env` files or hardcoded API keys are permitted in version control. Credentials are injected dynamically at runtime via `secrets.py` from AWS Secrets Manager.
- **Asynchronous Streaming:** Long-running agent reasoning loops communicate back to clients using Server-Sent Events (SSE) over FastAPI, ensuring low-latency interactive feedback.
- **Directory Structure & Separation of Concerns:**
  - **Root:** Global configuration, state definitions, schemas, and runtime orchestrators (`state.py`, `schemas.py`, `secrets.py`).
  - **`nodes/`:** Modular, self-contained LangGraph execution steps (e.g., `input_normalizer.py`).

## 3. Core Agent Workflow & Tools
1. **Input Normalization Node:** Parses raw user symptoms, OBD-II trouble codes, or BMW hex codes into structured entities.
2. **Knowledge Base RAG Tool:** Queries vectorized technical documentation and community troubleshooting consensus for the target chassis (e.g., 2018 BMW 440i / B58 engine).
3. **Parts Sourcing & Cross-Reference Tool:** Resolves component failures to exact OEM part numbers and Tier-1 supplier alternatives.