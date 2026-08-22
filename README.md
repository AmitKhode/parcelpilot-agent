# ParcelPilot AI Customer Support Agent

A production-grade, tool-augmented AI agent built for ParcelPilot's B2B logistics platform. It reasons dynamically over customer agreements, operational Excel records, and policy documents while enforcing strict source precedence, data-layer access control, and a confirmation safety state machine.

## Core Features
- **Dynamic Retrieval & Source Hierarchy**: Automatically resolves conflicts by enforcing Customer Agreement > Current SOP > Product Guides > Historical Tickets > Deprecated Policies.
- **Data-Layer Access Control**: Strict multi-tenant data isolation preventing customer role accounts from querying unauthorized customer data.
- **Two-Phase Confirmation Flow**: State-changing actions (e.g. ticket escalations) cannot be executed by the LLM without explicit human confirmation.
- **Safe Mathematical Calculator**: Built with AST parsing to eliminate arbitrary code execution.
- **Proactive Issue Detection**: Real-time analytical dashboard identifying recurring product issues, SLA breach risks, and carrier-fault anomalies.

## Quick Start (Local Setup)

1. Clone and create virtualenv:
```bash
git clone [https://github.com/AmitKhode/parcelpilot-agent.git](https://github.com/AmitKhode/parcelpilot-agent.git)
cd parcelpilot-agent

# Create virtual environment
python -m venv venv

# Activate on Mac/Linux:
source venv/bin/activate
# OR Activate on Windows:
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
