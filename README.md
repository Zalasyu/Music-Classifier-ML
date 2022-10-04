# Project Organization

├── Makefile <- Makefile with commands like `make data` or `make train` 
├── README.md <- The top-level README for developers using this project. 
├── data
│ ├── external <- Data from third party sources.
│ ├── interim <- Intermediate data that has been transformed.
│ ├── processed <- The final, canonical data sets for modeling.
│ └── raw <- The original, immutable data dump.
│
│
├── models <- Trained and serialized models, model predictions, or
│ model summaries
│
│
├── reports <- Generated analysis as HTML, PDF, LaTeX, etc.
│ └── figures <- Generated graphics and figures to be used in reporting
│
├── pyproject.toml <- The requirements file for reproducing environment.
│
├── src <- Source code for use in this project.
│ ├── **init**.py <- Makes src a Python module
│ │
│ ├── data <- Scripts to download or generate data
│ │ └── make_dataset.py
│ │
│ ├── features <- Scripts to turn raw data into features for modeling
│ │ └── build_features.py
│ │
│ ├── models <- Scripts to train models and then use trained models to make
│ │ │ predictions
│ │ ├── predict_model.py
│ │ └── train_model.py
│ │
│ └── visualization <- Scripts to create exploratory and results oriented visualizati

# CRISP-DM Process Model

https://web.archive.org/web/20220401041957/https://www.the-modeling-agency.com/crisp-dm.pdf

## Business Understanding

### Objectives

1. Build a dataset containg song metadata and their various genres and spectrograph info.
2. Develop a pipeline to import audio clips from datasets
3. Create a web app front-end (can run on desktop).
4. Host the program as a web server.
5. Develop a program to run a user-submitted audio clip against the model and print results witha ccuracy metrics
6. Content based recommender system for music similar to audio clip
   - Train a neural network

### Situation

The user will enter a song clip, then receive a formatted top-n list of genres sorted by confidence value in descending order.

### Data Mining Goals

## Technologies, Libraries, Tools

- Poetry: Project Dependency Management Tool
- Pytorch: Machine Learning
- Librosa: Audio and Music Proccessing
- Matplotlib: Data Visualization
- Numpy: General purpose array-processing
- Pandas: Data analysis and manipulation tool
- Morgan: logger
- Pytest: Test framework

## Data Understanding

### Datasets

- GTZAN Genre Collection by G. Tzanetakis and P. Cook
- Million Song Dataset by LabROSA and The Echonest

### Data Description

### Exploratory Data Analysis

### Data Quality Analysis

## Data Preparation

### Select Data

### Clean Data

### Construct Data

### Integrate Data

### Format Data

## Modeling

### Select Modeling Techniques

### Generate Test Design

### Build Model

### Assess Model

## Evaluation

### Evaluate Results

### Review Process

### Next Steps

## Deployment

### Plan Deployment

### Plan Monitoring and Maintenance

### Produce Final Report

### Review Project
