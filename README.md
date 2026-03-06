# Clara AI Intern Assignment
## Zero-Cost Automation Pipeline: Demo Call → Retell Agent Draft → Onboarding Update → Agent Revision

## Overview

This project implements an automated pipeline that converts demo call transcripts into structured AI phone agent configurations and updates those agents after onboarding calls.

The system processes transcripts to:

1. Extract structured business information
2. Generate a preliminary AI receptionist configuration
3. Store versioned artifacts per account
4. Update agent configurations after onboarding
5. Track changes between versions
6. Generate operational metrics and review tasks

The entire system runs using **zero-cost tools**, satisfying the assignment constraint that no paid APIs or subscriptions may be used.

---

# Architecture

The pipeline is divided into two stages.

## Pipeline A — Demo Call → Preliminary Agent

Input:
Demo call transcript

Output:
- Structured Account Memo JSON
- Retell Agent Draft Specification
- Stored versioned artifacts
- Automatically generated review task

Process:

1. Transcript ingestion
2. Information extraction using rule-based NLP
3. Structured account memo generation
4. Agent configuration generation
5. Artifact storage
6. Task creation for agent review

Artifacts generated:

```
outputs/accounts/<account_id>/v1/
    account_memo.json
    agent_spec.json
```

---

## Pipeline B — Onboarding Call → Agent Update

Input:
Onboarding call transcript

Output:
- Updated account memo
- Updated agent configuration
- Versioned change history
- Diff report between versions

Process:

1. Onboarding transcript ingestion
2. Extraction of updated business details
3. Patch applied to existing account memo
4. Regeneration of agent configuration
5. Version increment (v1 → v2)
6. Diff generation
7. Change log creation

Artifacts generated:

```
outputs/accounts/<account_id>/v2/
    account_memo.json
    agent_spec.json

outputs/accounts/<account_id>/
    diff.json
    changes.md
```

---

# Project Structure

```
clara-ai-assignment/

data/
    demo_calls/
    onboarding_calls/

outputs/
    accounts/
        <account_id>/
            v1/
            v2/
            diff.json
            changes.md

logs/
    pipeline.log

scripts/
    extract_demo.py
    generate_agent.py
    update_agent.py
    diff_viewer.py
    create_tasks.py
    metrics.py

tasks/
    <account_id>_task.json

dashboard.py
run_pipeline.py
README.md
```

---

# Key Components

## Transcript Extraction

The extraction layer converts unstructured transcript text into structured business data including:

- services supported
- emergency triggers
- business hours
- routing rules
- operational constraints

This is implemented using **rule-based NLP**, ensuring:

- zero API cost
- deterministic behavior
- no hallucinated information

Missing data is explicitly flagged in:

```
questions_or_unknowns
```

---

## Agent Configuration Generation

The pipeline generates a **Retell Agent Draft Specification** including:

- agent name
- voice style
- system prompt
- routing variables
- transfer protocol
- fallback protocol

Example fields:

```
agent_name
system_prompt
key_variables
call_transfer_protocol
fallback_protocol
```

This specification can be directly used to configure a Retell AI phone agent.

---

## Versioning System

Each account maintains versioned agent artifacts.

```
v1 → generated from demo call
v2 → updated from onboarding call
```

Changes between versions are recorded using:

```
diff.json
changes.md
```

This enables clear traceability of agent modifications.

---

## Task Tracking

The pipeline automatically generates a review task for each generated agent configuration.

Because paid APIs were not allowed under the zero-cost constraint, this project implements a **mock task tracker** using JSON files stored in the `/tasks` directory.

Example:

```
tasks/demo1_task.json
```

Each task represents a review item that would normally be created in tools like Asana.

---

## Logging

The pipeline logs all processing steps for traceability.

Logs are stored in:

```
logs/pipeline.log
```

Example log events:

- transcript processing
- agent generation
- onboarding updates
- diff creation
- pipeline metrics

---

## Metrics

The system generates summary metrics after pipeline execution.

Example metrics:

```
accounts_processed
total_services_detected
total_emergency_triggers
```

These metrics help evaluate extraction performance across datasets.

---

## Dashboard (Bonus Feature)

A lightweight Streamlit dashboard is included to visualize pipeline results.

The dashboard displays:

- processed accounts
- detected services
- emergency triggers
- pipeline statistics

Run with:

```
py -m streamlit run dashboard.py
```

---

# Running the Pipeline

## Step 1 — Add transcripts

Place demo transcripts in:

```
data/demo_calls/
```

Place onboarding transcripts in:

```
data/onboarding_calls/
```

---

## Step 2 — Run pipeline

```
py run_pipeline.py
```

This executes:

1. Demo extraction
2. Agent generation
3. Task creation
4. Onboarding updates
5. Version diff generation
6. Metrics calculation

---

## Example Output

```
outputs/accounts/demo1/

v1/
    account_memo.json
    agent_spec.json

v2/
    account_memo.json
    agent_spec.json

diff.json
changes.md
```

---

# Zero-Cost Design

The project intentionally avoids paid APIs or services.

Design choices:

| Requirement | Implementation |
|-------------|---------------|
| LLM extraction | Rule-based NLP |
| Task tracking | JSON-based mock task system |
| Storage | Local JSON artifacts |
| Orchestration | Python scripts |
| Dashboard | Streamlit (free) |

This ensures the system is fully reproducible with no external dependencies.

---

# Idempotent Pipeline

The pipeline is designed to be **idempotent**.

Running the pipeline multiple times will not duplicate artifacts or corrupt existing outputs.

Existing accounts are skipped if already processed.

---

# Limitations

Current limitations include:

- rule-based extraction may miss uncommon phrasing
- service detection uses keyword matching
- routing rules require transcript mentions

These trade-offs were chosen to maintain the **zero-cost constraint**.

---

# Future Improvements

With production resources the system could be improved using:

- local open-source LLM extraction
- automated speech-to-text transcription
- direct Retell API integration
- real task management integration (Asana / Jira)
- improved entity recognition

---

# Demonstration

The project includes a Loom demo showing:

1. pipeline execution
2. generated outputs
3. agent version update
4. diff visualization

---

# Summary

This project demonstrates a fully automated pipeline that:

- converts demo calls into AI phone agent configurations
- updates agents based on onboarding calls
- tracks changes across versions
- generates operational metrics
- creates review tasks
- runs entirely with zero cost tools

The system is modular, reproducible, and designed to resemble a small production workflow.