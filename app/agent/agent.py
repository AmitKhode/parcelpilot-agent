import json
from typing import Dict, Any, List, Tuple
from openai import AsyncOpenAI
from app.config import settings
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.state import confirmation_manager
from app.tools.document_search import search_documents
from app.tools.data_lookup import get_order_details, get_ticket_details, list_customer_orders, list_customer_tickets
from app.tools.calculator import calculate
from app.tools.escalation import propose_escalation, execute_confirmed_escalation

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Searches ParcelPilot SOPs, support policies, known issues, and customer agreements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query keywords"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_details",
            "description": "Retrieves operational details for a specific order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "e.g. ORD-1001"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ticket_details",
            "description": "Retrieves operational details for a specific support ticket.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string", "description": "e.g. TKT-501"}
                },
                "required": ["ticket_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_customer_tickets",
            "description": "Lists support tickets for an account.",
            "parameters": {
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Optional account ID"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Safely evaluates a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Arithmetic expression"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "propose_escalation",
            "description": "Proposes a ticket escalation. ALWAYS requires user confirmation before execution.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string", "description": "e.g. TKT-501"},
                    "reason": {"type": "string", "description": "Reason for escalation"},
                    "urgency": {"type": "string", "enum": ["Low", "Medium", "High", "Critical"]}
                },
                "required": ["ticket_id", "reason", "urgency"]
            }
        }
    }
]

async def execute_agent_turn(
    user_message: str,
    user_context: Dict[str, Any],
    history: List[Dict[str, Any]]
) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]]]:
    session_id = user_context.get("session_id", "default_session")
    tool_events = []

    # 1. Check if user is confirming or denying a pending state-changing action
    pending_action = confirmation_manager.get_pending(session_id)
    clean_msg = user_message.strip().lower()

    if pending_action:
        if clean_msg in ["yes", "confirm", "yes, confirm", "proceed", "sure"]:
            res = execute_confirmed_escalation(pending_action)
            confirmation_manager.clear(session_id)
            tool_events.append({"tool": "execute_confirmed_escalation", "status": "executed"})
            return (
                f"### Action Completed\n\n**{res['message']}**\n- Ticket ID: `{pending_action['ticket_id']}`\n- Reason: {pending_action['reason']}\n- Urgency: {pending_action['urgency']}",
                tool_events,
                history + [{"role": "user", "content": user_message}, {"role": "assistant", "content": res["message"]}]
            )
        elif clean_msg in ["no", "cancel", "deny", "abort"]:
            confirmation_manager.clear(session_id)
            return (
                "### Action Cancelled\nThe requested escalation was aborted. No state changes were made.",
                tool_events,
                history + [{"role": "user", "content": user_message}, {"role": "assistant", "content": "Action cancelled."}]
            )

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [{"role": "user", "content": user_message}]

    # 2. Call LLM with tool definitions
    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        tools=TOOL_DEFINITIONS,
        tool_choice="auto",
        temperature=0.0
    )

    resp_msg = response.choices[0].message

    # 3. Handle Tool Calls
    if resp_msg.tool_calls:
        messages.append(resp_msg)
        for tool_call in resp_msg.tool_calls:
            fname = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            tool_events.append({"tool": fname, "args": args})

            if fname == "search_documents":
                result = search_documents(query=args.get("query"))
            elif fname == "get_order_details":
                result = get_order_details(order_id=args.get("order_id"), user_context=user_context)
            elif fname == "get_ticket_details":
                result = get_ticket_details(ticket_id=args.get("ticket_id"), user_context=user_context)
            elif fname == "list_customer_tickets":
                result = list_customer_tickets(account_id=args.get("account_id"), user_context=user_context)
            elif fname == "calculate":
                result = calculate(expression=args.get("expression"))
            elif fname == "propose_escalation":
                result = propose_escalation(
                    ticket_id=args.get("ticket_id"),
                    reason=args.get("reason"),
                    urgency=args.get("urgency"),
                    user_context=user_context
                )
            else:
                result = f"Error: Tool {fname} not found."

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": fname,
                "content": json.dumps(result) if isinstance(result, (dict, list)) else str(result)
            })

        # Second turn: synthesize final response with tool evidence
        final_resp = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=0.0
        )
        final_content = final_resp.choices[0].message.content
        return final_content, tool_events, messages

    return resp_msg.content, tool_events, messages + [resp_msg]