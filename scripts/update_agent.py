import os
import json
import re
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    filename=os.path.join(BASE_DIR, "logs", "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

ONBOARDING_FOLDER = os.path.join(BASE_DIR, "data", "onboarding_calls")
ACCOUNTS_FOLDER = os.path.join(BASE_DIR, "outputs", "accounts")


def extract_business_hours(text):

    text = text.lower()

    patterns = [
        r"\d{1,2}\s?(?:am|pm)?\s?-\s?\d{1,2}\s?(?:am|pm)?",
        r"\d{1,2}\s?(?:am|pm)?\s?to\s?\d{1,2}\s?(?:am|pm)?"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()

    return None


def update_memo(v1_memo, onboarding_text):

    updated = v1_memo.copy()

    hours_text = extract_business_hours(onboarding_text)

    if hours_text:

        if "to" in hours_text:
            parts = hours_text.split("to")
        elif "-" in hours_text:
            parts = hours_text.split("-")
        else:
            parts = []

        if len(parts) == 2:
            start = parts[0].strip()
            end = parts[1].strip()

            updated["business_hours"]["start"] = start
            updated["business_hours"]["end"] = end

            if "Exact business hours" in updated["questions_or_unknowns"]:
                updated["questions_or_unknowns"].remove("Exact business hours")

    return updated


def generate_agent_spec(memo, version):

    services = memo.get("services_supported", [])

    system_prompt = f"""
You are an AI phone receptionist for {memo['company_name']}.

Services supported include: {', '.join(services)}.

BUSINESS HOURS FLOW
- greet caller
- ask purpose
- collect name and phone
- collect job address if needed
- transfer to dispatch
- fallback if transfer fails
- confirm next steps
- close call

AFTER HOURS FLOW
- greet caller
- ask purpose
- determine if emergency
- if emergency collect name, phone, address
- attempt transfer
- fallback if transfer fails
- if non-emergency record request for next day
- close call

Never mention internal tools to callers.
"""

    agent_spec = {

        "agent_name": f"{memo['company_name']} AI Receptionist",

        "version": version,

        "voice_style": "professional and calm",

        "system_prompt": system_prompt,

        "key_variables": {
            "business_hours": memo["business_hours"],
            "services_supported": memo["services_supported"],
            "emergency_definition": memo["emergency_definition"]
        },

        "tool_invocation_placeholders": [
            "create_service_request",
            "transfer_call_to_dispatch"
        ],

        "call_transfer_protocol": memo["call_transfer_rules"],

        "fallback_protocol": memo["call_transfer_rules"]["fallback_message"]
    }

    return agent_spec


def process_onboarding():

    files = os.listdir(ONBOARDING_FOLDER)

    for file in files:

        if not file.endswith(".txt"):
            continue

        account_id = file.replace(".txt", "")

        onboarding_path = os.path.join(ONBOARDING_FOLDER, file)

        with open(onboarding_path, "r", encoding="utf-8") as f:
            onboarding_text = f.read()

        v1_memo_path = os.path.join(ACCOUNTS_FOLDER, account_id, "v1", "account_memo.json")

        with open(v1_memo_path, "r", encoding="utf-8") as f:
            v1_memo = json.load(f)

        v2_memo = update_memo(v1_memo, onboarding_text)

        v2_folder = os.path.join(ACCOUNTS_FOLDER, account_id, "v2")

        os.makedirs(v2_folder, exist_ok=True)

        memo_path = os.path.join(v2_folder, "account_memo.json")

        with open(memo_path, "w", encoding="utf-8") as f:
            json.dump(v2_memo, f, indent=4)

        agent_spec = generate_agent_spec(v2_memo, "v2")

        agent_path = os.path.join(v2_folder, "agent_spec.json")

        with open(agent_path, "w", encoding="utf-8") as f:
            json.dump(agent_spec, f, indent=4)

        changes_path = os.path.join(ACCOUNTS_FOLDER, account_id, "changes.md")

        with open(changes_path, "w", encoding="utf-8") as f:
            f.write("# Agent Update Log\n\n")
            f.write("Version updated from v1 to v2 based on onboarding call.\n")
            f.write("Updated fields:\n")
            f.write("- business_hours\n")

        logging.info(f"Updated account {account_id} from v1 to v2")
        print(f"Updated account {account_id} to v2")


if __name__ == "__main__":
    process_onboarding()