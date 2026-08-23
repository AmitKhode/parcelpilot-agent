# AI Tool Usage

In building this assessment, I maintained full ownership over the system architecture, business logic, and security workflows. I utilized Large Language Models (ChatGPT / Gemini) strictly as productivity multipliers to accelerate standard development tasks. 

**Where I relied on my own engineering:**
*   **System Architecture:** Designing the ReAct loop and tool orchestration.
*   **State Management:** Architecting the Two-Phase Confirmation flow to safely pause and resume tool execution.
*   **Security & Authorization:** Building the Multi-Tenant Access Control logic to ensure data isolation based on the user context.
*   **Source Hierarchy:** Defining the strict rule engine for resolving conflicts between Customer Agreements and standard SOPs.

**Where I utilized AI assistance:**
*   **Boilerplate & UI:** Scaffolding the initial Streamlit layout and syntax for the multi-tab dashboard.
*   **Debugging:** Rapidly diagnosing specific package dependency errors (e.g., resolving the pandas `openpyxl` engine requirement for modern Excel handling).
*   **Scenario Generation:** Helping write realistic dummy data and test prompts for the sidebar simulator.

Using AI for these routine tasks allowed me to focus my time entirely on the core architectural challenges of the agent.