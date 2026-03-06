import os
import json
import logging
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ensure logs folder exists
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

INPUT_FOLDER = os.path.join(BASE_DIR, "data", "demo_calls")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs", "accounts")


def extract_info(transcript_text, account_id):

    text = transcript_text.lower()

    services = []
    emergency = []

    # -------------------------------
    # Service detection
    # -------------------------------

    if "ev charger" in text:
        services.append("EV charger installation")

    if "hot tub" in text:
        services.append("hot tub electrical hookup")

    if "panel change" in text or "panel upgrade" in text:
        services.append("electrical panel upgrades")

    if "troubleshoot" in text:
        services.append("electrical troubleshooting")

    if "renovation" in text:
        services.append("electrical renovations")

    if "commercial" in text:
        services.append("commercial electrical work")

    if "residential" in text:
        services.append("residential electrical work")

    # Generic service keywords (works across industries)

    if "install" in text:
        services.append("installation services")

    if "repair" in text:
        services.append("repair services")

    if "maintenance" in text:
        services.append("maintenance services")

    # Fallback
    if not services:
        services.append("general service work")

    # -------------------------------
    # Emergency detection
    # -------------------------------

    if "gas station" in text or "pump" in text:
        emergency.append("gas station pump failures")

    if "emergency" in text:
        emergency.append("general emergency service")

    # -------------------------------
    # Business hours detection
    # -------------------------------

    business_hours = {
        "days": "unknown",
        "start": "unknown",
        "end": "unknown",
        "timezone": "unknown"
    }

    hours_match = re.search(
        r"\b\d{1,2}\s?(am|pm)\s?(to|-)\s?\d{1,2}\s?(am|pm)\b", text
    )

    if hours_match:
        hours_text = hours_match.group()

        if "to" in hours_text:
            start, end = hours_text.split("to")
        else:
            start, end = hours_text.split("-")

        business_hours["start"] = start.strip()
        business_hours["end"] = end.strip()

    # -------------------------------
    # Company name detection
    # -------------------------------

    company_name = "Unknown Company"

    name_match = re.search(
        r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*\s(?:Electric|Electrical|Services|Solutions))",
        transcript_text
    )

    if name_match:
        company_name = name_match.group()

    # -------------------------------
    # Address detection
    # -------------------------------

    office_address = ""

    address_match = re.search(
        r"\d+\s[A-Za-z]+\s(?:Street|St|Road|Rd|Avenue|Ave)",
        transcript_text
    )

    if address_match:
        office_address = address_match.group()

    # -------------------------------
    # Account memo
    # -------------------------------

    account_memo = {

        "account_id": account_id,

        "company_name": company_name,

        "business_hours": business_hours,

        "office_address": office_address,

        "services_supported": list(set(services)),

        "emergency_definition": list(set(emergency)),

        "emergency_routing_rules": [],

        "non_emergency_routing_rules": [],

        "call_transfer_rules": {
            "timeout_seconds": 20,
            "retry_attempts": 1,
            "fallback_message": "We could not reach dispatch. Someone will call you back shortly."
        },

        "integration_constraints": [],

        "after_hours_flow_summary": "",

        "office_hours_flow_summary": "",

        "questions_or_unknowns": [
            "Exact business hours",
            "Service area coverage",
            "Pricing structure",
            "Dispatch workflow"
        ],

        "notes": ""
    }

    return account_memo


def process_demo_calls():

    files = os.listdir(INPUT_FOLDER)

    for file in files:

        if not file.endswith(".txt"):
            continue

        filepath = os.path.join(INPUT_FOLDER, file)

        with open(filepath, "r", encoding="utf-8") as f:
            transcript = f.read()

        account_id = file.replace(".txt", "")

        account_folder = os.path.join(OUTPUT_FOLDER, account_id, "v1")
        memo_path = os.path.join(account_folder, "account_memo.json")

        # Idempotency check
        if os.path.exists(memo_path):
            logging.info(f"Skipping {account_id}, already processed")
            print(f"Skipping {account_id}, already processed")
            continue

        os.makedirs(account_folder, exist_ok=True)

        extracted = extract_info(transcript, account_id)

        with open(memo_path, "w", encoding="utf-8") as f:
            json.dump(extracted, f, indent=4)

        logging.info(f"Processed demo transcript: {file}")
        print(f"Processed {file}")


if __name__ == "__main__":
    process_demo_calls()