import os
import json
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    filename=os.path.join(BASE_DIR, "logs", "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

INPUT_FOLDER = os.path.join(BASE_DIR, "data", "demo_calls")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs", "accounts")


def extract_info(transcript_text, account_id):

    text = transcript_text.lower()

    services = []
    emergency = []

    # Electrical-related services
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

    # General service keywords
    if "install" in text:
        services.append("installation services")

    if "repair" in text:
        services.append("repair services")

    if "maintenance" in text:
        services.append("maintenance services")

    # Emergency detection
    if "gas station" in text or "pump" in text:
        emergency.append("gas station pump failures")

    if "emergency" in text:
        emergency.append("general emergency service")

    # Fallback
    if not services:
        services.append("general service work")

    account_memo = {
        "account_id": account_id,
        "company_name": "Unknown Company",
        "business_hours": {
            "days": "unknown",
            "start": "unknown",
            "end": "unknown",
            "timezone": "unknown"
        },
        "office_address": "",
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

        with open(os.path.join(INPUT_FOLDER, file), "r", encoding="utf-8") as f:
            transcript = f.read()

        account_id = file.replace(".txt", "")

        extracted = extract_info(transcript, account_id)

        account_folder = os.path.join(OUTPUT_FOLDER, account_id, "v1")
        memo_path = os.path.join(account_folder, "account_memo.json")

        # Idempotency check
        if os.path.exists(memo_path):
            logging.info(f"Skipping {account_id}, already processed")
            print(f"Skipping {account_id}, already processed")
            continue

        os.makedirs(account_folder, exist_ok=True)

        with open(memo_path, "w", encoding="utf-8") as f:
            json.dump(extracted, f, indent=4)

        logging.info(f"Processed demo transcript: {file}")
        print(f"Processed {file}")


if __name__ == "__main__":
    process_demo_calls()