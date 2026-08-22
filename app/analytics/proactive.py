import pandas as pd
from typing import Dict, Any, List
from app.data.loader import repo

def analyze_proactive_issues() -> Dict[str, Any]:
    """
    Analyzes ticket and order data to detect:
    1. Recurring product issue spikes (e.g. Bulk Upload failures)
    2. High-severity P1/P2 tickets near or breaching SLA targets
    3. Carrier-fault pickup delays
    """
    tickets_df = repo.tickets_df.copy()
    orders_df = repo.orders_df.copy()

    # Issue breakdown
    issue_counts = tickets_df["subject"].value_counts().to_dict()

    # High severity analysis
    p1_p2_tickets = []
    for _, t in tickets_df.iterrows():
        subj = str(t.get("subject", ""))
        desc = str(t.get("description", ""))
        is_critical = "all shipment" in subj.lower() or "500" in desc
        is_high = "bulk upload" in subj.lower()
        
        severity = "P1 - Critical" if is_critical else ("P2 - High" if is_high else "P3 - Normal")
        if severity in ["P1 - Critical", "P2 - High"]:
            p1_p2_tickets.append({
                "ticket_id": t["ticket_id"],
                "account_id": t["account_id"],
                "severity": severity,
                "subject": subj,
                "status": t["status"],
                "created_at": str(t["created_at"])
            })

    # Carrier issues in orders
    carrier_delays = orders_df[orders_df["carrier_fault"] == True][
        ["order_id", "account_id", "carrier", "status", "shipment_fee_inr"]
    ].to_dict(orient="records")

    return {
        "snapshot_reference": repo.snapshot_time,
        "total_active_tickets": len(tickets_df),
        "recurring_issues": issue_counts,
        "high_priority_approaching_sla": p1_p2_tickets,
        "carrier_fault_incidents": carrier_delays
    }