# 🛡️ Aadhaar Drishti | Gov-Tech Intelligence Hub

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google)
![Status](https://img.shields.io/badge/Status-Hackathon%20Ready-success?style=for-the-badge)

> **"From Data to Action: Empowering District Officials with AI-Driven Governance."**

---

## 📖 Overview

**Aadhaar Drishti** is a next-generation analytics and governance platform designed for the **UIDAI Aadhaar Hackathon**. It empowers district-level administrators to monitor Aadhaar ecosystem health in real-time, predict resource requirements, and automate administrative legal actions.

Unlike traditional dashboards that only *display* data, Aadhaar Drishti *acts* on it—using **Unsupervised Machine Learning** to detect anomalies and **Generative AI** to draft legal notices and answer policy queries in local Indian languages.

---

## 🚀 Key Features (The 4 Pillars)

### 1. 🔴 Satark Monitor (Live Anomaly Detection)
* **What it does:** Uses **Isolation Forest** algorithms to scan thousands of transaction logs instantly.
* **Impact:** Automatically flags districts with suspicious spikes in biometric failures or demographic updates (potential fraud or operational issues).

### 2. 🔮 Bhavishya (Predictive Planning)
* **What it does:** Uses **Facebook Prophet** time-series forecasting to predict enrolment demand for the next 30 days.
* **Impact:** Helps officials allocate machines and operators *before* a shortage occurs.

### 3. 📜 Karyawahi (Auto-Bureaucrat)
* **What it does:** The "Killer Feature." One-click generation of official **Show Cause Notices (PDF)**.
* **Tech:** Uses **Google Gemini GenAI** to draft legally sound text and **FPDF** to generate the document.
* **Impact:** Reduces administrative paperwork time from hours to seconds.

### 4. 🗣️ Samvad AI (Vernacular Chatbot)
* **What it does:** A RAG-based AI assistant that understands Hindi, Marathi, Tamil, and English.
* **Impact:** Allows ground-level operators to ask complex questions like *"Pune mein migration trend kya hai?"* and get data-backed answers.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit (Python) |
| **Data Processing** | Pandas, NumPy (ETL Engine) |
| **ML Models** | Scikit-Learn (Isolation Forest), Facebook Prophet |
| **Generative AI** | Google Gemini Flash API |
| **Visualization** | Plotly Express |
| **Deployment** | Streamlit Community Cloud |

---

## ⚙️ Installation & Setup (Run Locally)

Follow these steps to run the project on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/aadhaar-drishti.git](https://github.com/YOUR_USERNAME/aadhaar-drishti.git)
cd aadhaar-drishti
```

### 2. Install Dependencies
Make sure you have Python installed. Then run:

Bash
```
pip install -r requirements.txt
```

### 3. Configure API Key (Crucial Step!)
This project uses Google Gemini AI. You need to set up your own API key.

Create a folder named .streamlit in the root directory.

Inside it, create a file named secrets.toml.

Add your API key inside that file:
```bash
Ini, TOML

# .streamlit/secrets.toml
GEMINI_API_KEY = "Your_Actual_Google_Gemini_Key_Here"
(Note: This file is ignored by Git for security purposes.)
```
### 4. Run the App
To start the dashboard, run:

```Bash

streamlit run app.py
```
### 📂 Project Structure
Here is how the project is organized:
```bash
Plaintext

aadhaar-drishti/
├── data/                   # Contains CSV datasets (Enrolment, Update, etc.)
├── .streamlit/             # (Create this locally) Stores secrets.toml
├── app.py                  # Main Frontend Application
├── ai_engine.py            # ML Logic (Anomaly Detection & Prophet)
├── etl_engine.py           # Data Cleaning & Preprocessing Logic
├── genai_tools.py          # Gemini AI Integration (Chat & PDF)
├── requirements.txt        # Python Dependencies
└── README.md               # Project Documentation
```