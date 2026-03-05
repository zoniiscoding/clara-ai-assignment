import os
import json
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    filename=os.path.join(BASE_DIR, "logs", "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

ACCOUNTS_FOLDER = os.path.join(BASE_DIR, "outputs", "accounts")


def generate_agent(account_id):

    memo_path = os.path.join(ACCOUNTS_FOLDER, account_id, "v1", "account_memo.json")

    with open(memo_path, "r", encoding="utf-8") as f:
        memo = json.load(f)

    services = memo.get("services_supported", [])

    system_prompt = f"""
You are an AI phone receptionist for {memo['company_name']}.

Your role is to answer incoming service calls professionally and collect
only the information required for routing and dispatch.

Services supported include: {', '.join(services)}.

BUSINESS HOURS FLOW:
1. Greet the caller politely.
2. Ask the purpose of the call.
3. Collect the caller's name.
4. Collect the caller's phone number.
5. Collect the service address if needed.
6. Confirm the requested service.
7. Attempt to transfer the call to dispatch.
8. If transfer fails, apologize and inform the caller someone will follow up shortly.
9. Ask if the caller needs anything else.
10. Close the call politely.

AFTER HOURS FLOW:
1. Greet the caller.
2. Ask the purpose of the call.
3. Determine if the situation is an emergency.
4. If emergency, collect name, phone number, and address immediately.
5. Attempt transfer to the on-call technician.
6. If transfer fails, assure the caller that dispatch will follow up shortly.
7. If not an emergency, record the request for next business day follow-up.
8. Ask if the caller needs anything else.
9. Close the call.

Never mention internal tools or system functions to the caller.
Be concise and professional.
"""

    agent_spec = {

        "agent_name": f"{memo['company_name']} AI Receptionist",

        "version": "v1",

        "voice_style": "professional and calm",

        "system_prompt": system_prompt,

        "key_variables": {
            "timezone": memo["business_hours"]["timezone"],
            "business_hours": memo["business_hours"],
            "office_address": memo["office_address"],
            "services_supported": memo["services_supported"],
            "emergency_definition": memo["emergency_definition"]
        },

        "tool_invocation_placeholders": [
            "create_service_request",
            "transfer_call_to_dispatch"
        ],

        "call_transfer_protocol": {
            "attempt_transfer": True,
            "timeout_seconds": memo["call_transfer_rules"]["timeout_seconds"],
            "retry_attempts": memo["call_transfer_rules"]["retry_attempts"]
        },

        "fallback_protocol": memo["call_transfer_rules"]["fallback_message"]
    }

    agent_path = os.path.join(ACCOUNTS_FOLDER, account_id, "v1", "agent_spec.json")

    with open(agent_path, "w", encoding="utf-8") as f:
        json.dump(agent_spec, f, indent=4)

    logging.info(f"Generated agent spec for account: {account_id}")
    print(f"Generated agent for {account_id}")


def process_accounts():

    accounts = os.listdir(ACCOUNTS_FOLDER)

    for account in accounts:

        if not os.path.isdir(os.path.join(ACCOUNTS_FOLDER, account)):
            continue

        generate_agent(account)


if __name__ == "__main__":
    process_accounts()