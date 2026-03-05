# Clara AI Automation Pipeline

This document describes the end-to-end workflow used to automate the generation
and updating of AI phone agents for service businesses.

---

# Pipeline Overview

The system processes demo calls and onboarding calls to automatically generate
and update Retell AI agent configurations.

The workflow runs locally with zero external cost.

---

# Pipeline A: Demo Call → Preliminary Agent

Input:
Demo call transcript

Processing Steps:

1. Transcript ingestion
2. Information extraction
3. Account memo generation
4. Agent configuration generation
5. Task creation for review

Output:

outputs/accounts/<account_id>/v1/
    account_memo.json
    agent_spec.json

---

# Pipeline B: Onboarding → Agent Update

Input:
Onboarding call transcript

Processing Steps:

1. Extract updated information
2. Apply changes to existing memo
3. Generate updated agent configuration
4. Compare v1 and v2
5. Generate change reports

Output:

outputs/accounts/<account_id>/v2/
    account_memo.json
    agent_spec.json

Additional artifacts:

diff.json
changes.md

---

# Pipeline Execution

The full pipeline can be executed with a single command:

py run_pipeline.py

Execution order:

1. extract_demo.py
2. generate_agent.py
3. create_tasks.py
4. update_agent.py
5. diff_viewer.py
6. metrics.py

---

# Data Flow Diagram

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

# Storage Structure

outputs/accounts/<account_id>/

v1/
    account_memo.json
    agent_spec.json

v2/
    account_memo.json
    agent_spec.json

diff.json
changes.md

---

# Observability

The system includes:

• Logging (logs/pipeline.log)  
• Metrics reporting  
• Dashboard visualization using Streamlit

---

# Zero Cost Design

The system uses:

• Local Python scripts  
• JSON storage  
• Streamlit dashboard  
• No paid APIs

This ensures the pipeline can run entirely on free infrastructure.