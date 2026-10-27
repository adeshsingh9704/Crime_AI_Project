# Crime AI Analytics System

Project Overview

The Crime AI Analytics System is a Python-based academic project designed to explore how machine learning, data analysis, image processing, and natural language processing techniques can be integrated into a unified crime analytics application.

The project provides a web-based interface for analyzing crime-related datasets, identifying geographical crime clusters, predicting crime categories, comparing images against reference images, and retrieving relevant legal information from stored case data.

The system follows a modular architecture in which Flask connects the backend modules with the web-based dashboard.

Objectives

- Analyze crime-related data using machine learning techniques.
- Identify geographical clusters in crime location data.
- Explore crime category prediction using a classification model.
- Compare uploaded images with stored reference images.
- Retrieve relevant information from a collection of legal cases.
- Present analytical results through a centralized web interface.

Key Modules

1. Crime Prediction

Uses a Random Forest classification model to predict crime categories from the available input features.

2. Crime Hotspot Analysis

Uses K-Means clustering to group geographical crime locations and explore spatial patterns.

3. Image Comparison

Uses OpenCV-based image comparison to compare an uploaded image with stored reference images. This is a basic image-similarity approach, not a production-grade facial recognition system.

4. Legal Information Retrieval

Uses TF-IDF vectorization and cosine similarity to retrieve relevant information from stored legal case records.

5. Web Dashboard and Backend

Uses Flask to connect the Python modules with the frontend, which is developed using HTML, CSS, and JavaScript. Leaflet can be used to display geographical data on an interactive map.

Technology Stack

- Programming Language: Python
- Backend Framework: Flask
- Machine Learning: Scikit-learn, Random Forest, K-Means
- Image Processing: OpenCV
- Text Processing: TF-IDF and cosine similarity
- Data Processing: Pandas and NumPy
- Frontend: HTML, CSS, JavaScript
- Mapping: Leaflet.js
- Data Storage: CSV datasets

System Architecture

The application follows a modular client-server workflow:

1. The user interacts with the web dashboard.
2. JavaScript sends requests to the Flask backend.
3. Flask routes requests to the appropriate Python module.
4. The selected module processes the available dataset or input.
5. The result is returned to the frontend for display.

Workflow: Frontend → Flask Backend → Python Modules → Dataset Processing → Results → Dashboard

Development Contribution

This project involves developing and integrating independent Python modules into a single web application. The work includes preparing and processing datasets, implementing machine learning and text-similarity techniques, integrating image-comparison functionality, connecting backend routes, and presenting results through a dashboard.

The project demonstrates practical experience with modular Python development, data processing, machine learning integration, and web application development.

Project Status

This project is an evolving academic prototype. Its modules and dashboard may be updated as development and testing continue.

Limitations and Responsible Use

- Results depend on the quality, size, and representativeness of the available datasets.
- Predictions and clusters are exploratory outputs and should not be treated as definitive crime-risk assessments.
- Image similarity results do not establish a person's identity or involvement in a crime.
- Legal information retrieval provides text similarity, not legal advice or authoritative legal interpretation.
- The system requires further validation, privacy safeguards, and security testing before any real-world deployment.

Future Enhancements

- Integrate larger, validated, and appropriately sourced datasets.
- Improve model evaluation and prediction reliability.
- Develop more robust image-matching methods with appropriate safeguards.
- Enhance interactive maps and analytical visualizations.
- Add secure authentication, access controls, and database integration.
- Improve automated testing, documentation, and deployment.

Disclaimer

This project is intended for educational and research purposes. It is not an operational law-enforcement system and must not be used to determine guilt, identify suspects conclusively, or make consequential decisions about individuals.

Author

Adesh Singh

B.Tech — Computer Science and Engineering (Data Science)

Manav Rachna International Institute of Research and Studies