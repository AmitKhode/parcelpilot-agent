#### `ARCHITECTURE.md`
```markdown
# ParcelPilot Agent Architecture

## 1. Agent Design & Orchestrator
The agent uses OpenAI Function Calling with strict system instructions that decouple business logic into deterministic Python tools (`document_search`, `data_lookup`, `calculator`, `propose_escalation`). 

## 2. Multi-Tier Source Hierarchy & Conflict Resolution
When policies conflict:
- **Contract Overrides**: The system tags document chunks with an `authority` score (Customer Agreement = 1, SOP = 2, Product Guide = 3, Deprecated = 5).
- If Northstar requests cancellation, the agent cites `05_Northstar_Logistics_Enterprise_Agreement.pdf` which overrides the general INR 250 cancellation fee in `03_Cancellation_and_Service_Credit_SOP_v4.pdf`.

## 3. Data Authorization Layer
Authorization is enforced at the function entry point within `app/data/loader.py`, never delegated to LLM prompt adherence. If a `CUSTOMER` role user asks for another account's data, an `AuthorizationError` is raised and caught immediately.

## 4. Confirmation Safety State Machine
State-changing tools transition through explicit states:
`REQUEST` -> `PROPOSED` -> `WAITING_FOR_CONFIRMATION` -> `CONFIRMED` -> `EXECUTE` -> `SUCCESS`.
The agent will refuse to execute an escalation until the user provides an affirmative response.