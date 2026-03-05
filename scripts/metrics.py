import os
import json
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCOUNTS_FOLDER = os.path.join(BASE_DIR, "outputs", "accounts")

logging.basicConfig(
    filename=os.path.join(BASE_DIR, "logs", "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def generate_metrics():

    total_accounts = 0
    total_services = 0
    total_emergencies = 0

    accounts = os.listdir(ACCOUNTS_FOLDER)

    for account in accounts:

        memo_path = os.path.join(
            ACCOUNTS_FOLDER,
            account,
            "v1",
            "account_memo.json"
        )

        if not os.path.exists(memo_path):
            continue

        with open(memo_path) as f:
            memo = json.load(f)

        total_accounts += 1
        total_services += len(memo["services_supported"])
        total_emergencies += len(memo["emergency_definition"])

    report = {
        "accounts_processed": total_accounts,
        "total_services_detected": total_services,
        "total_emergency_triggers": total_emergencies
    }

    logging.info(f"Generated metrics report: {report}")

    print("Pipeline Metrics:")
    print(report)


if __name__ == "__main__":
    generate_metrics()