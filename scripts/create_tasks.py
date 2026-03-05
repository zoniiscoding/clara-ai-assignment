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
TASKS_FOLDER = os.path.join(BASE_DIR, "tasks")

os.makedirs(TASKS_FOLDER, exist_ok=True)

accounts = os.listdir(ACCOUNTS_FOLDER)

for account in accounts:

    account_path = os.path.join(ACCOUNTS_FOLDER, account)

    if not os.path.isdir(account_path):
        continue

    task = {
        "account_id": account,
        "task_name": "Review AI Agent Configuration",
        "description": "Verify generated agent spec and account memo.",
        "status": "pending",
        "priority": "medium"
    }

    task_file = os.path.join(TASKS_FOLDER, f"{account}_task.json")

    with open(task_file, "w") as f:
        json.dump(task, f, indent=4)

    print(f"Task created for {account}")