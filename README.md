# Diversity Matters: Perceived Inclusion and Discrimination by Brazilian Tech Professionals

This repository contains all the codes, data, ICFs and resources used in the study.

[![DOI](https://zenodo.org/badge/823398782.svg)](https://doi.org/10.5281/zenodo.15885217)

Access the full paper [here](results/Diversity4SEBR.pdf)

## Abstract

This study investigates perceived inclusion and discrimination by Brazilian tech professionals. Through a survey of 220 participants across Brazil, placed on Google Forms, we examine the challenges faced by underrepresented groups, the strategies companies employ, and the gaps in current practices.

## Repository Structure

- `/data`: Contains raw and processed data collected from the survey.
- `/scripts`: Analysis scripts organized by research question:
  - `/participant_characterization`: Demographic characterization scripts
  - `/RQ1`: Bias recognition analysis scripts
  - `/RQ2`: Demographic profile analysis scripts
  - `/RQ3`: Company characteristics analysis scripts
  - `/RQ4`: Team and leadership level analysis scripts
  - `/RQ5`: Diversity and inclusion definitions and word cloud scripts
  - `/RQ6`: Discrimination and prejudice definitions and word cloud scripts
  - `/RQ7`: Additional analysis scripts
  - `requirements.txt`: Required Python libraries
- `/survey`: The survey questionnaire used in the study and the ICF. Available versions: Portuguese and English.
- `/results`: Analysis results organized by research question:
  - `/participant_characterization`: Full characterization of survey respondents
  - `/RQ1`: Analysis of bias recognition
  - `/RQ2`: Analysis by demographic profile
  - `/RQ3`: Analysis by company characteristics
  - `/RQ4`: Analysis at team and leadership levels
  - `/RQ5`: Diversity and inclusion definitions and word clouds
  - `/RQ6`: Discrimination and prejudice definitions and word clouds
  - `/RQ7`: Additional analyses
  - `/papers`: Full paper in PDF version

## Reproducing the Study

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/aisepucrio/Diversity4BRSE.git
   cd Diversity4BRSE
   ```

2. **Install dependencies**
   ```bash
   pip install -r scripts/requirements.txt
   ```

3. **Run the analysis scripts**

   **Option A: Batch Execution (Recommended)**
   
   Use the main orchestrator script to run multiple analyses at once:
   
   ```bash
   # Run all analyses
   python scripts/main.py --all
   
   # Run specific research questions
   python scripts/main.py --rq1 --rq2 --rq3
   
   # Run characterization and specific RQs
   python scripts/main.py --characterization --rq4 --rq5
   
   # Run with minimal output
   python scripts/main.py --all --quiet
   
   # See all available options
   python scripts/main.py --help
   ```
   
   **Available flags:**
   - `--all` - Run all scripts
   - `--characterization` - Participant characterization
   - `--rq1` - Bias recognition analysis
   - `--rq2` - Discrimination perceptions by demographic profile
   - `--rq3` - Discrimination perceptions by company characteristics
   - `--rq4` - Diversity perception at team and leadership levels
   - `--rq5` - Diversity and inclusion definitions and word clouds
   - `--rq6` - Discrimination and prejudice definitions and word clouds
   - `--quiet` - Minimize output (show only summary)

   **Option B: Individual Script Execution**
   
   Run scripts individually if needed:
   
   ```bash
   # Participant Characterization
   python scripts/participant_characterization/characterization.py
   
   # Research Questions
   python scripts/RQ1/coding_bias.py
   python scripts/RQ2/profile.py
   python scripts/RQ3/company.py
   python scripts/RQ4/leaders.py
   python scripts/RQ4/teams.py
   python scripts/RQ5/coding_inclusion_diversity.py
   python scripts/RQ5/diversitycloud.py
   python scripts/RQ6/coding_discrimination_prejudice.py
   python scripts/RQ6/discriminationcloud.py
   ```

## Contributing

We welcome contributions from the community! Here's how you can help:

- 📝 **Participate in our survey**: [Survey (PT)](https://forms.gle/n9wLZbP2Nd2nRhUD9) | [Survey (EN)](https://forms.gle/21LsnDiqJqDLoihW8)
- 🐛 **Report issues**: Open an issue if you find bugs or have suggestions
- 🔧 **Submit improvements**: Create a pull request with your enhancements

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as permitted under the terms of this license.