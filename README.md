# Clara AI Automation Pipeline

Zero-cost automation pipeline that converts demo call transcripts into AI phone agents and automatically updates them after onboarding calls.

This project was built for the Clara Answers Intern Assignment and demonstrates a fully reproducible workflow that processes transcripts, generates agent configurations, applies onboarding updates, and tracks version changes.

---

# Overview

The system automates the lifecycle of an AI receptionist agent:

Demo Call → Account Memo → Agent Draft → Onboarding Updates → Agent Revision

The pipeline runs locally with zero paid APIs and produces structured outputs for each account.

---

# Features

• Automatic transcript processing  
• Structured account memo generation  
• Retell AI agent draft generation  
• Onboarding-based agent updates  
• Versioning (v1 → v2)  
• JSON diff comparison  
• Human-readable change reports  
• Task creation for review  
• Logging and metrics  
• Streamlit monitoring dashboard  

---

# System Architecture

Demo Transcript  
      │  
      ▼  
Extraction Engine  
      │  
      ▼  
Account Memo (v1)  
      │  
      ▼  
Agent Spec Generator  
      │  
      ▼  
Retell Agent Draft  
      │  
      ▼  
Onboarding Update  
      │  
      ▼  
Account Memo (v2)  
      │  
      ▼  
Agent Spec (v2)  
      │  
      ▼  
Diff + Change Report  

---

# Project Structure

clara-ai-assignment

data  
  demo_calls  
  onboarding_calls  

scripts  
  extract_demo.py  
  generate_agent.py  
  update_agent.py  
  diff_viewer.py  
  metrics.py  
  create_tasks.py  

outputs  
  accounts/<account_id>  
    v1  
    v2  
    diff.json  
    changes.md  

workflows  
  pipeline_workflow.md  

tasks  

logs  

dashboard.py  
run_pipeline.py  
README.md  

---

# Pipeline A: Demo Call → Preliminary Agent

Input:  
Demo call transcript

Output:

account_memo.json  
agent_spec.json  
task tracker item  

Stored in:

outputs/accounts/<account_id>/v1/

---

# Pipeline B: Onboarding → Agent Update

Input:  
Onboarding call transcript

Output:

updated account memo  
updated agent configuration  
version diff  
changelog  

Stored in:

outputs/accounts/<account_id>/v2/

Additional files:

diff.json  
changes.md  

---

# Running the Pipeline

Place transcripts into:

data/demo_calls/  
data/onboarding_calls/

Run the full pipeline:

py run_pipeline.py

This executes:

1. Demo extraction  
2. Agent generation  
3. Task creation  
4. Onboarding update  
5. Diff generation  
6. Metrics reporting  

---

# Dashboard

A simple monitoring dashboard is included.

Run:

py -m streamlit run dashboard.py

The dashboard displays:

• processed accounts  
• detected services  
• emergency triggers  
• version updates  

---

# Data Privacy

Demo transcripts and onboarding recordings are not included in this repository.

Place dataset files locally in:

data/demo_calls/  
data/onboarding_calls/

This follows the assignment instruction to avoid publishing customer data publicly.

---

# Zero-Cost Design

The system runs entirely using free tools:

Python scripts  
Local JSON storage  
Streamlit dashboard  
No paid APIs  

This ensures the pipeline can run on any machine without cost.

---

# Future Improvements

With production access, the system could be extended with:

• LLM-based extraction for higher accuracy  
• direct Retell API integration  
• automated CRM integration  
• scalable database storage  
• automated call routing logic  

---

# Demo

A short Loom walkthrough demonstrates:

• pipeline execution  
• generated outputs  
• v1 → v2 updates  

(Provided with submission)