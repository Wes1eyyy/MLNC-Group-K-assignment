# EPL Match Outcome Prediction

> Machine learning model for predicting English Premier League football match outcomes

**Course**: COMP0036 - Machine Learning for Natural and Computational Sciences
**Group**: K
**Academic Year**: 2025/26

---

## Overview

This project develops machine learning models to predict English Premier League (EPL) football match outcomes. Given historical match data from 2000-2024, we predict whether matches will result in a home win, draw, or away win.

## Task

Predict the outcomes of 10 EPL matches scheduled for **31 January 2026**.

**Target Variable**: `FTR` (Full Time Result)
- `H` - Home Win
- `D` - Draw
- `A` - Away Win

## Data

**Training Set**: ~9,600 EPL matches (2000-2024)
- Match details: Date, teams, referee
- Goals: Full-time and half-time scores
- Statistics: Shots, shots on target, corners, fouls
- Cards: Yellow and red cards

**Test Set**: 10 matches on 31 January 2026

## Methodology

The project focuses on:

1. **Exploratory Data Analysis**: Understanding patterns in historical match data
2. **Feature Engineering**: Creating predictive features from raw statistics (team form, head-to-head records, home advantage, etc.)
3. **Model Development**: Training and comparing multiple ML algorithms
4. **Model Evaluation**: Validation using appropriate train/test splits

External data sources may be used to enhance predictions (player stats, manager info, etc.), **excluding betting odds**.

## Benchmark

Professional bookmakers achieve ~53% accuracy in match prediction. This serves as the performance benchmark for the task.

**Note**: Assessment prioritizes methodology, understanding, and creativity over absolute accuracy.

## Deliverables

- **Report (PDF)**: Methodology, analysis, and findings
- **Notebook (`.ipynb`)**: Implementation with documentation
- **Predictions (CSV)**: Test set predictions
