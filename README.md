# Redrob Candidate Ranking System

## Overview

This project ranks AI/ML candidates from the Redrob dataset using a multi-stage filtering and scoring pipeline.

The system processes candidate profiles and removes invalid or honeypot profiles, applies recruiter instructed hard filters, scores candidates using multiple profile signals, and outputs the Top 100 candidates.

---
## Pipeline

1. Candidate Validation
- Signup date validation
- Salary range validation
- Job duration validation
- Skill consistency validation
- Graduation vs experience validation

2. Feature Extraction
- AI skill detection
- LLM/NLP detection
- Search/RAG detection
- Consulting background
- Production ML experience
- Preferred location
- Platform activity

3. Hard Filtering
- Non-technical roles removed
- Consulting-only profiles removed
- Pure research profiles removed
- Experience filtering

4. Candidate Scoring
- Experience
- AI skills
- Advanced AI skills
- Search / Retrieval
- NLP / LLM
- Platform signals
- Notice period
- Location preference

5. Ranking
- Scores normalized to [0,1]
- Deterministic sorting
- Top 100 exported

---

## Repository Structure

```
rank.py
validator.py
filter_f.py
filter_s.py
candidate_scorer.py

DevFusion.csv
DevFusion.xlsx

submission_metadata.yaml
validate_submission.py
README.md
```

---

## Requirements

```
pip install openpyxl
```

---

## Run

```
python rank.py
```

---

## Outputs

- DevFusion.csv
- DevFusion.xlsx
- top_candidates.jsonl
