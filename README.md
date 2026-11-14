<p align="center">
  <img src="assets/eco-hero-banner.svg" alt="Eco-Hero Academy — Community Recycling Guide" width="100%">
</p>

<p align="center">
  <strong>Small choices. Cleaner communities.</strong><br>
  Learn everyday recycling basics through guides, challenges and achievements.
</p>

<p align="center">
  <a href="https://github.com/krlhsn/eco-hero-academy/actions/workflows/tests.yml"><img alt="Tests" src="https://github.com/krlhsn/eco-hero-academy/actions/workflows/tests.yml/badge.svg"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="Dependencies" src="https://img.shields.io/badge/dependencies-none-27a37b">
  <img alt="License MIT" src="https://img.shields.io/badge/license-MIT-7A5CFA">
</p>

---

## About

**Eco-Hero Academy** is a Python terminal application that makes learning about recycling more engaging. Explore material guides, ask the Eco Advisor, complete short challenges, review missed questions, build a profile and unlock achievement badges.

The project is designed to run locally, with no third-party Python dependencies.

## Features

| Feature | What it does |
|---|---|
| **Material guides** | Tips, common contaminants and a fun fact for nine material categories. |
| **Guide presets** | Two example regional presets, plus a general guide. |
| **Eco Advisor** | Helps with common questions about recycling, sorting and disposal. |
| **Eco-Challenge** | Five-question True/False and multiple-choice rounds with explanations. |
| **Adaptive review** | Brings up to two questions missed in the previous round into the next round. |
| **Player profiles** | Create, load and save progress locally in a JSON file. |
| **Achievement badges** | Seven achievements for participation, scores and topic exploration. |
| **Leaderboard** | Ranks profiles saved on the same computer. |

## Getting started

### Requirements

- Python 3.10 or newer
- No third-party Python dependencies

### 1. Download the project

    git clone https://github.com/krlhsn/eco-hero-academy.git
    cd eco-hero-academy

### 2. Run the application

    python main.py

Or run the single-file version directly:

    python eco_hero_academy.py

The single-file version is included for environments where you prefer to paste one complete script into a Python IDE.

### 3. Install the command-line entry point (optional)

    python -m pip install -e .
    eco-hero

### 4. Run the tests

    python -m unittest discover -s tests -v

## How to play

1. Choose **Manage Profiles**.
2. Create a profile or load an existing local profile.
3. Open a material guide, take an Eco-Challenge, ask the Eco Advisor, view your badges or change the guide preset.
4. Choose **Save & Log Out** to keep your progress.

The profile file is `eco_hero_profiles.json` in the current working directory. The leaderboard reads profiles from that same file; it is not shared online.

## Guide presets and local rules

The two named presets, **Eco-City Standard** and **Greenburg Initiative**, are fictional examples that demonstrate how guidance can vary. They are not real municipal programmes.

Recycling acceptance rules differ by location, provider and facility. The general tips are educational examples, not official disposal instructions. Check your local authority or waste provider before disposing of batteries, electronics, light bulbs, chemicals or other potentially hazardous items.

## Project structure

    eco-hero-academy/
    ├── .github/workflows/tests.yml
    ├── assets/eco-hero-banner.svg
    ├── docs/PROJECT_NOTES.md
    ├── eco_hero/
    │   ├── __init__.py
    │   ├── cli.py
    │   ├── data.py
    │   ├── engine.py
    │   ├── models.py
    │   └── storage.py
    ├── tests/
    ├── eco_hero_academy.py
    ├── main.py
    ├── pyproject.toml
    ├── .gitignore
    ├── CITATION.cff
    ├── CONTRIBUTING.md
    ├── LICENSE
    ├── PRIVACY.md
    └── SECURITY.md

## Privacy

Eco-Hero Academy runs locally. It does not upload profile information or synchronize progress. Saved profiles contain usernames, scores, viewed materials, badge progress and quiz history. There are no passwords or encryption, so use a nickname and avoid storing sensitive personal information. See [PRIVACY.md](PRIVACY.md).

## Development

The maintained application is in `eco_hero/`. The standalone `eco_hero_academy.py` file contains the complete application in one script.

Run the test suite with:

    python -m unittest discover -s tests -v

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidance.

## Author

**Kamrul Hassan**  
[GitHub](https://github.com/krlhsn) · [LinkedIn](https://www.linkedin.com/in/krlhsn/) · [ORCID](https://orcid.org/0009-0008-2990-1036)

## License

Released under the [MIT License](LICENSE).

---

<p align="center"><em>Be curious. Waste less. Help your community.</em></p>
