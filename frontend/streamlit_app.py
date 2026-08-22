import sys
import os
from pathlib import Path
import streamlit as st
import asyncio

# Add project root directory to sys.path so 'app' can be found
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Corrected Imports (No '.py' in module names, no missing functions)
from app.agent.agent import execute_agent_turn
from app.analytics.proactive import analyze_proactive_issues
from app.data.repository import get_escalations

st.set_page_config(page_title="ParcelPilot Support Agent", layout="wide", page_icon="📦")

# Sidebar - User Context & Role Selector
st.sidebar.title("🔐 Access Control Simulator")
role = st.sidebar.selectbox("Active Role", ["SUPPORT_AGENT", "CUSTOMER", "ADMIN"])
account_id = None

if role == "CUSTOMER":
    account_choice = st.sidebar.selectbox(
        "Simulate Customer Account",
        ["ACCT-001 (Northstar Logistics)", "ACCT-002 (LumenWorks)", "ACCT-003 (Beacon Retail)"]
    )
    account_id = account_choice.split(" ")[0]

user_context = {
    "role": role,
    "account_id": account_id,
    "user_id": f"sim_{role.lower()}_01",
    "session_id": "streamlit_session"
}

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Context:** `{role}`")
if account_id:
    st.sidebar.markdown(f"**Account ID:** `{account_id}`")

# Demo Scenario Fast-Click Buttons
st.sidebar.subheader("🎯 Demo Scenarios")
scenarios = [
    "Can Northstar cancel ORD-1001 without a cancellation fee? Explain why.",
    "A pickup is three hours late because of carrier fault. Should I get a service credit?",
    "Show me the latest tickets for my account.",
    "Why was ticket TKT-501 raised and what is its SLA?",
    "Escalate ticket TKT-501 due to severe production outage.",
    "Show me Northstar's orders."  # Test authorization failure when logged in as ACCT-002
]

clicked_prompt = None
for s in scenarios:
    if st.sidebar.button(s, key=f"btn_{s}"):
        clicked_prompt = s

# Main Layout Tabs
tab_chat, tab_proactive, tab_escalations = st.tabs(["💬 AI Support Agent", "📊 Proactive Issue Detection", "⚡ Escalation DB"])

with tab_chat:
    st.header("ParcelPilot AI Support Agent")
    st.caption("Logistics AI Assistant with Document Precedence, Data Authorization, and Safe Confirmations.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    input_text = st.chat_input("Ask a support, policy, or operational question...") or clicked_prompt

    if input_text:
        st.session_state.messages.append({"role": "user", "content": input_text})
        with st.chat_message("user"):
            st.markdown(input_text)

        with st.chat_message("assistant"):
            with st.status("Executing Multi-Step Agent Workflow...", expanded=True) as status:
                st.write("🔎 Determining tool execution requirements...")
                response_text, tool_events, _ = asyncio.run(
                    execute_agent_turn(input_text, user_context, st.session_state.messages[:-1])
                )
                for ev in tool_events:
                    st.write(f"⚡ **Tool executed:** `{ev['tool']}`")
                status.update(label="Response generated with evidence", state="complete")

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

with tab_proactive:
    st.header("Internal Proactive Issue Detection")
    analytics = analyze_proactive_issues()
    st.info(f"Dataset Reference Snapshot: {analytics['snapshot_reference']}")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Recurring Customer Issues")
        for subj, count in analytics["recurring_issues"].items():
            st.metric(label=subj, value=f"{count} ticket(s)")

    with col2:
        st.subheader("Critical P1 / P2 Tickets")
        st.dataframe(analytics["high_priority_approaching_sla"], use_container_width=True)

with tab_escalations:
    st.header("Escalations Table (SQLite Mock State)")
    escalations = get_escalations()
    if escalations:
        st.dataframe(escalations, use_container_width=True)
    else:
        st.write("No escalated tickets yet.")