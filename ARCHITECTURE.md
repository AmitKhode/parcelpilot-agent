# Architecture Note

**Agent Design**
The core agent relies on an LLM utilizing a ReAct (Reasoning and Acting) loop, heavily augmented by function calling (Tool Use). It maintains conversation state and evaluates user input against a strict system prompt. A critical component of the design is the **Confirmation State Machine**, which intercepts any state-changing tool calls (like ticket escalations) and suspends execution until explicit human confirmation is received.

**Tool Design**
Tools are strictly typed and isolated. 
*   **Read-Only Tools:** `get_order_details`, `get_ticket_details`, `search_documents`.
*   **State-Changing Tools:** `propose_escalation`, `execute_confirmed_escalation`.
*   **Compute Tools:** `calculate` (Uses AST parsing to safely evaluate math without arbitrary code execution risks).
All data-layer tools enforce Multi-Tenant Access Control, intercepting the `account_id` from the user context to prevent cross-tenant data leakage.

**Document and Structured-Data Handling**
*   **Structured Data:** Managed via `pandas`, treating the provided Excel workbook as an in-memory datastore.
*   **Unstructured Data (Documents):** Handled via a local ChromaDB vector store. Documents are chunked, embedded, and retrieved based on semantic similarity to the user's query.

**Source Reliability and Conflict Handling**
The agent's system prompt enforces a strict hierarchical precedence to resolve conflicting information:
1. Customer-Specific Agreements (Highest priority)
2. Current SOPs
3. Product Guides
4. Deprecated Policies (Lowest priority)
If a conflict arises, the agent explicitly cites the source it is relying on and explains the override logic.

**Major Technical Trade-offs**
*   **In-Memory Data vs. Relational DB:** I utilized Pandas to parse the Excel file directly for simplicity and portability in this assessment. In a production environment, this would be migrated to a proper PostgreSQL/CRM backend.
*   **Synchronous vs. Asynchronous:** While the Streamlit UI handles asynchronous calls well, some local data lookups are synchronous. Future iterations would fully async the database drivers for high concurrency.
