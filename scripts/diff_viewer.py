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


def compare_dicts(old, new):
    diff = {}

    for key in old:
        if key not in new:
            continue

        if old[key] != new[key]:
            diff[key] = {
                "old": old[key],
                "new": new[key]
            }

    return diff


def generate_changes_md(account, diff, account_path):

    lines = []
    lines.append(f"# Changes for account: {account}\n")

    if not diff:
        lines.append("No changes detected.\n")

    for field, values in diff.items():

        lines.append(f"## {field}")

        lines.append(f"- old: {values['old']}")
        lines.append(f"- new: {values['new']}\n")

    changes_path = os.path.join(account_path, "changes.md")

    with open(changes_path, "w") as f:
        f.write("\n".join(lines))


def run_diff():

    accounts = os.listdir(ACCOUNTS_FOLDER)

    for account in accounts:

        account_path = os.path.join(ACCOUNTS_FOLDER, account)

        v1_path = os.path.join(account_path, "v1", "account_memo.json")
        v2_path = os.path.join(account_path, "v2", "account_memo.json")

        if not os.path.exists(v1_path) or not os.path.exists(v2_path):
            continue

        with open(v1_path) as f:
            v1 = json.load(f)

        with open(v2_path) as f:
            v2 = json.load(f)

        diff = compare_dicts(v1, v2)

        diff_path = os.path.join(account_path, "diff.json")

        with open(diff_path, "w") as f:
            json.dump(diff, f, indent=4)

        generate_changes_md(account, diff, account_path)

        logging.info(f"Generated diff report for account: {account}")
        print(f"Diff generated for {account}")


if __name__ == "__main__":
    run_diff()