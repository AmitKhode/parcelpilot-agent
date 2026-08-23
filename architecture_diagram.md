# ParcelPilot Agent Architecture Diagram

```mermaid
graph TD
    A[User / Customer] -->|Query| B(Streamlit UI)
    B --> C{Confirmation State Machine}
    
    C -->|Pending Action Yes/No| D[Execute or Abort Tool]
    C -->|New Query| E[OpenAI ReAct Agent]
    
    E <-->|Function Calling| F[Tool Execution Engine]
    
    F -->|search_documents| G[(ChromaDB: Vector Docs)]
    F -->|get_order / get_ticket| H[(Pandas: Excel Data)]
    F -->|calculate| I[AST Math Parser]