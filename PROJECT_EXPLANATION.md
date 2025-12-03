# Phishing Detection System - Technical Overview

This document provides a detailed explanation of the technologies, features, and architecture of the Phishing Detection System.

## 1. Technology Stack

### Frontend (User Interface)
- **HTML5**: Provides the semantic structure of the application.
- **CSS3**: Custom styling with a modern, glassmorphism aesthetic.
  - **Variables**: Used for consistent theming (colors, spacing).
  - **Animations**: CSS keyframes for typing indicators and hover effects.
- **JavaScript (ES6+)**: Handles user interactions, API calls, and state management.
- **GSAP (GreenSock Animation Platform)**: Powers the advanced animations (sidebar entrance, floating shapes, robot movements).
- **FontAwesome**: Provides the icons used throughout the interface.
- **Google Fonts**: Uses 'Poppins' for modern typography.

### Backend (API & Logic)
- **Python 3.11+**: The core programming language.
- **FastAPI**: A modern, high-performance web framework for building the API.
- **Uvicorn**: An ASGI server to run the FastAPI application.
- **Pydantic**: Data validation for API requests (e.g., ensuring email content is a string).
- **Joblib**: Used for saving and loading the trained Machine Learning models.
- **Requests**: Handles HTTP requests to the Ollama/Gemma API.

### Machine Learning & AI
- **Scikit-learn**: The primary ML library.
  - **Random Forest Classifier**: The algorithm used for both URL and Email phishing detection.
  - **TF-IDF Vectorizer**: Converts email text into numerical features for the model.
- **Pandas & NumPy**: Used for data manipulation and feature engineering during training.
- **Ollama + Gemma**:
  - **Ollama**: A local tool for running Large Language Models.
  - **Gemma (by Google)**: The specific LLM used for the "Security Assistant" chat and for providing natural language explanations of analysis results.

## 2. Features & Functionality

### A. URL Phishing Detection
- **How it works**:
  1. User enters a URL.
  2. Frontend sends it to `/analyze/url`.
  3. **Feature Extractor** (`feature_extractor.py`) breaks the URL down into numerical features:
     - Length of URL, domain, path.
     - Count of special characters (dots, dashes, @ symbols).
     - Presence of IP addresses or suspicious keywords.
     - HTTPS status.
  4. **ML Model** (`model.pkl`) predicts the probability of phishing based on these features.
  5. System returns a Risk Score (0-100) and classification (Safe, Suspicious, Phishing).

### B. Email Phishing Detection
- **How it works**:
  1. User pastes email content.
  2. Frontend sends it to `/analyze/email`.
  3. **ML Model** (`email_model.pkl`):
     - Text is converted to numbers using TF-IDF.
     - Random Forest model predicts phishing probability.
  4. **AI Explanation** (Optional):
     - The system asks Gemma to briefly explain *why* the email was classified that way.
  5. Result is displayed with a Risk Score and the AI's explanation.

### C. Security Assistant (Chatbot)
- **How it works**:
  1. User types a question in the chat widget.
  2. Frontend sends it to `/chat`.
  3. Backend forwards the message + conversation history to Gemma (via Ollama).
  4. Gemma generates a helpful, cybersecurity-focused response.
  5. Response is displayed in the chat window.

### D. History & Dashboard
- **Local Storage**: The frontend saves scan history in the browser's Local Storage, so it persists even if you refresh the page.
- **Visualizations**: History is shown as a timeline with color-coded badges for quick risk assessment.

### E. Theme System
- **Dark/Light Mode**: Toggles CSS variables to switch color schemes instantly.
- **Persisted Preference**: Saves the user's choice in Local Storage.

## 3. Project Structure

```
phishing_detection/
├── backend/
│   ├── app.py                 # Main API server (FastAPI)
│   ├── feature_extractor.py   # Logic to extract features from URLs
│   ├── gemma_client.py        # Client to talk to Ollama/Gemma
│   ├── train_model.py         # Script to train URL model
│   ├── train_email_model.py   # Script to train Email model
│   ├── generate_data.py       # Generates synthetic training data
│   ├── model.pkl              # Trained URL model
│   ├── email_model.pkl        # Trained Email model
│   └── tfidf_vectorizer.pkl   # Text processor for emails
│
├── frontend/
│   ├── index.html             # Main user interface
│   ├── styles.css             # All visual styling
│   ├── script.js              # Frontend logic (API calls, UI updates)
│   └── *.wav                  # Sound effects for the robot
│
└── data/                      # CSV files used for training models
```

## 4. How Everything Connects

1.  **Start**: You run `python app.py` (Backend) and `python -m http.server` (Frontend).
2.  **Interaction**: You click "Scan" on the frontend.
3.  **Request**: `script.js` uses `fetch()` to send data to `http://localhost:8000/...`.
4.  **Processing**: `app.py` receives the data, loads the `.pkl` models, runs predictions, and optionally calls `gemma_client.py`.
5.  **Response**: JSON data is sent back to the frontend.
6.  **Display**: `script.js` parses the JSON and updates the HTML DOM to show results, charts, and badges.
