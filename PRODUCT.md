# Product Note

**Additional Client Problem Addressed**
Beyond reactive support, B2B platforms struggle with identifying systemic issues before clients churn. I addressed this by building the **Proactive Issue Detection Dashboard**. This feature acts as an internal tool for Account Managers, aggregating structured ticket data to identify recurring themes (e.g., carrier faults) and flagging high-priority tickets approaching SLA breaches.

**Future Capabilities**
If continuing development on ParcelPilot, I would build:
*   **Webhook Integration:** Live connections to carriers (FedEx, UPS) for real-time tracking updates without needing manual ticket creation.
*   **Sentiment Analysis:** Tagging incoming tickets with frustration scores to automatically route angry customers to senior human agents.

**Intentional Omissions**
*   **True Authentication (OAuth/JWT):** For demo purposes, I implemented a sidebar role-simulator rather than a full login flow. 
*   **Email Dispatch:** The escalation tool records the action in a database but does not actually fire emails via SMTP/SendGrid to avoid spamming during testing.

**Success Metric**
**Escalation Deflection Rate:** The percentage of support interactions successfully resolved by the AI (e.g., citing a policy or calculating a refund) without requiring a tool-call to escalate the ticket to a human agent.
