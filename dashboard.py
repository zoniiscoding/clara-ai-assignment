import streamlit as st
import os
import json

ACCOUNTS_FOLDER = "outputs/accounts"

st.title("Clara AI Automation Dashboard")

accounts = os.listdir(ACCOUNTS_FOLDER)

total_accounts = len(accounts)
total_services = 0
total_emergencies = 0

for account in accounts:

    account_path = os.path.join(ACCOUNTS_FOLDER, account)

    v1_path = os.path.join(account_path, "v1", "account_memo.json")
    v2_path = os.path.join(account_path, "v2", "account_memo.json")
    diff_path = os.path.join(account_path, "diff.json")

    if not os.path.exists(v1_path):
        continue

    with open(v1_path) as f:
        v1 = json.load(f)

    total_services += len(v1["services_supported"])
    total_emergencies += len(v1["emergency_definition"])

st.subheader("Pipeline Summary")

st.write("Accounts processed:", total_accounts)
st.write("Total services detected:", total_services)
st.write("Emergency triggers detected:", total_emergencies)

st.divider()

for account in accounts:

    account_path = os.path.join(ACCOUNTS_FOLDER, account)

    v1_path = os.path.join(account_path, "v1", "account_memo.json")
    v2_path = os.path.join(account_path, "v2", "account_memo.json")
    diff_path = os.path.join(account_path, "diff.json")

    if not os.path.exists(v1_path):
        continue

    with open(v1_path) as f:
        v1 = json.load(f)

    st.header(f"Account: {account}")

    st.subheader("Services Supported")
    st.write(v1["services_supported"])

    st.subheader("Emergency Definitions")
    st.write(v1["emergency_definition"])

    st.subheader("Business Hours (v1)")
    st.write(v1["business_hours"])

    if os.path.exists(v2_path):

        with open(v2_path) as f:
            v2 = json.load(f)

        st.subheader("Business Hours (v2)")
        st.write(v2["business_hours"])

    if os.path.exists(diff_path):

        with open(diff_path) as f:
            diff = json.load(f)

        st.subheader("Changes Detected")
        st.json(diff)

    st.divider()