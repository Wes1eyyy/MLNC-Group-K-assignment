# Archive Directory

## Purpose
This directory contains the original exploratory Python scripts that were created during initial data exploration.

## Contents

### Original EDA Scripts:
These scripts were created for initial data exploration and feature statistics calculation. They have been superseded by the structured notebooks in the `notebooks/` directory.

- `winrate.py` - Calculate team win rates
- `home & away winrate.py` - Home and away win rate analysis
- `no. of goals.py` - Goal statistics
- `no. of shots.py` - Shot statistics
- `no. of shots on target.py` - Shots on target analysis
- `fouls.py` - Foul statistics
- `yellow card.py` - Yellow card analysis
- `red card.py` - Red card analysis
- `corner.py` - Corner statistics
- `recent.py` - Recent form analysis
- `teamtoteam.py` - Head-to-head statistics
- `main.py` - Comprehensive feature extraction script

## Note

These files are kept for reference but are not part of the main project workflow. All functionality has been reorganized into:

1. **Notebooks** (`notebooks/` directory) - For exploratory analysis and documentation
2. **Source modules** (`src/` directory) - For reusable functions

The current project structure follows software engineering best practices with:
- Modular, reusable code
- Clear separation of concerns
- Comprehensive documentation
- Version control friendly organization

## Migration Status

The functionality from these scripts has been incorporated into:
- `notebooks/01_EDA.ipynb` - Data exploration
- `notebooks/02_feature_engineering.ipynb` - Feature creation
- `src/feature_engineering.py` - Reusable feature functions
- `src/data_processing.py` - Data handling functions
