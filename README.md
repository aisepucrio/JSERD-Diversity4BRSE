# Diversity, Equity, and Inclusion in Software Engineering: Perceptions from Professionals in Brazil

[![DOI](https://zenodo.org/badge/1167492051.svg)](https://doi.org/10.5281/zenodo.21850292)

This repository contains the data, analysis scripts, questionnaires, and replication materials for the study on perceived inclusion, discrimination, and unconscious bias among Brazilian tech professionals.

📄 **[Read the Full Paper (PDF)](results/JSERD-Diversity4SEBR.pdf)** | 🔗 **[Zenodo Artifact](https://doi.org/10.5281/zenodo.21850292)**

---

## Overview

Through a nationwide survey of 220 tech professionals in Brazil, this study investigates workplace inequities across intersecting demographic identities and organizational settings. We examine how practitioners conceptualize diversity and inclusion, how discrimination is experienced or silenced, and the persistent gaps between team-level representation and leadership advancement.

---

## Repository Structure

The project is organized by Research Question (**RQ1-RQ7**) as presented in the paper:

```text
├── data/                             # Raw and anonymized survey datasets
├── survey/                           # Questionnaire & Informed Consent Forms (PT/EN)
├── scripts/
│   ├── main.py                       # CLI Orchestrator to execute analyses
│   ├── participant_characterization/ # Demographic & professional profiling
│   ├── RQ1/                          # Diversity & Inclusion definitions
│   ├── RQ2/                          # Prejudice & Discrimination definitions
│   ├── RQ3/                          # Fairness perceptions by demographic profile
│   ├── RQ4/                          # Fairness perceptions by organizational setting
│   ├── RQ5/                          # Recognize, Narrate, and Silence analysis
│   ├── RQ6/                          # Inclusion in development teams vs. leadership
│   └── RQ7/                          # Unconscious bias awareness analysis
└── results/                          # Generated figures, tables, and the full paper in PDF
```

---

## Reproducing the Study

### 1. Prerequisites & Setup

Ensure you have **Python 3.11+** and **Git** installed.

```bash
git clone https://github.com/aisepucrio/JSERD-Diversity4BRSE.git
cd JSERD-Diversity4BRSE
pip install -r scripts/requirements.txt
```

### 2. Execution Methods

You can run the full analytical pipeline via the main orchestrator or execute specific modules individually.

#### Option A: CLI Orchestrator (Recommended)

```bash
# Run the entire pipeline (all RQs + characterization)
python scripts/main.py --all

# Run specific modules only
python scripts/main.py --characterization --rq1 --rq2

# Run all with compact summary output
python scripts/main.py --all --quiet
```

**Available CLI Flags:**
* `--all`: Execute all scripts
* `--characterization`: Participant demographic profiling
* `--rq1`: Diversity and inclusion definitions & word clouds
* `--rq2`: Prejudice and discrimination definitions & word clouds
* `--rq3`: Equity perceptions by demographic profile
* `--rq4`: Equity perceptions by company size, sector, and work model
* `--rq5`: Workplace discrimination: Recognize, Narrate, and Silence
* `--rq6`: Representation in development teams vs. leadership roles
* `--rq7`: Self-awareness of unconscious bias
* `--quiet`: Suppress verbose logs and show summary only

#### Option B: Individual Script Execution

```bash
# Characterization
python scripts/participant_characterization/characterization.py

# Research Questions
python scripts/RQ1/coding_inclusion_diversity.py
python scripts/RQ1/diversitycloud.py
python scripts/RQ2/coding_discrimination_prejudice.py
python scripts/RQ2/discriminationcloud.py
python scripts/RQ3/profile.py
python scripts/RQ4/company.py
python scripts/RQ5/intersection.py
python scripts/RQ6/teams.py
python scripts/RQ6/leaders.py
python scripts/RQ7/coding_bias.py
```

---

## Contributing

We welcome community feedback and improvements:
* 📝 **Participate in our survey**: [Português](https://forms.gle/n9wLZbP2Nd2nRhUD9) | [English](https://forms.gle/21LsnDiqJqDLoihW8)
* 🐛 **Report Issues**: Open a GitHub issue for bugs or methodological suggestions.
* 🔧 **Pull Requests**: Submit PRs for code optimizations or documentation improvements.

---

## License

This project is licensed under the **[MIT License](LICENSE)**.
