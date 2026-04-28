# 📞 Cell2Cell: Telecom Churn Decision Intelligence System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Machine Learning](https://img.shields.io/badge/Machine_Learning-Scikit_Learn-orange)
![Deployment](https://img.shields.io/badge/Deployment-Streamlit-red)
![Docker](https://img.shields.io/badge/Containerization-Docker-2496ED)

An end-to-end Machine Learning pipeline and deployment architecture designed to predict customer churn, calculate risk severity, and trigger actionable retention strategies for high-value telecom subscribers.

---

## 📑 Table of Contents
1. [Business Context](#-business-context)
2. [Strategic Value & ROI](#-strategic-value--roi)
3. [Project Structure](#️-project-structure)
4. [Technical Features](#️-technical-features)
5. [The Machine Learning Lifecycle](#-the-machine-learning-lifecycle)
6. [Docker Containerization](#-docker-containerization)

---

## 💼 Business Context

**The Scenario:** This project utilizes historical data from the "Cell2Cell" era (tied to the SBC Communications/AT&T telecom evolution)—a period when the US wireless market shifted from high-growth acquisition to cutthroat market saturation.

With an annualized churn rate hovering near 28%, the executive mandate shifted to **Data-Driven Retention**. Because acquiring a new customer costs 5x to 20x more than retaining an existing one, identifying "at-risk" subscribers before they port their numbers to a competitor became the primary lever for profitability.

**The Objective:**
Build a predictive engine that moves beyond binary classification (Yes/No) to actionable **Decision Intelligence**. The system flags high-risk subscribers based on usage patterns, service quality (e.g., dropped calls), and billing history, and pairs them with specific retention actions.

---

## 📈 Strategic Value & ROI

This system introduces a **VIP Threshold Logic** to prioritize retention budgets. 

* **Financial Proof:** If 1,000 customers leave paying $60/month, the business leaks $60,000 in Monthly Recurring Revenue (MRR).
* **The VIP Engine:** Instead of treating all customers equally, the system identifies the 80th percentile of monthly revenue drivers (the top 20% "Whales").
* **Actionable Output:** If a VIP hits a >60% churn probability, the system escalates the risk to **Critical** and triggers a high-touch "Strategic Call" rather than a low-conversion automated email. Assuming a conservative 35% save rate on flagged VIPs, the system directly protects top-line revenue.

---

## 🏗️ Project Structure

```text
📦 CELL2CELL-PROJECT
 ┣ 📂 notebooks
 ┃ ┣ 📜 EDA.sql
 ┃ ┣ 📜 EDA.ipynb
 ┃ ┗ 📜 model_prototyping.ipynb
 ┣ 📂 saved_models
 ┃ ┣ 📜 model_trainer.pkl
 ┃ ┗ 📜 preprocessor.pkl
 ┣ 📂 src
 ┃ ┣ 📂 components
 ┃ ┃ ┣ 📜 __init__.py
 ┃ ┃ ┣ 📜 data_ingestion.py
 ┃ ┃ ┣ 📜 data_transformation.py
 ┃ ┃ ┣ 📜 model_evaluation.py
 ┃ ┃ ┣ 📜 model_pusher.py
 ┃ ┃ ┗ 📜 model_trainer.py
 ┃ ┣ 📂 pipeline
 ┃ ┃ ┣ 📜 __init__.py
 ┃ ┃ ┣ 📜 predict_pipeline.py
 ┃ ┃ ┗ 📜 training_pipeline.py
 ┃ ┣ 📜 exception.py
 ┃ ┣ 📜 logger.py
 ┃ ┗ 📜 utils.py
 ┣ 📜 .gitignore
 ┣ 📜 app.py
 ┣ 📜 Dockerfile
 ┣ 📜 Project_Approach.md
 ┣ 📜 main.py
 ┣ 📜 requirements.txt
 ┗ 📜 setup.py

 ---

## ⚙️ Technical Features

✅ **End-to-End ML Architecture:** Fully automated from raw data ingestion to inference.
✅ **Modular Component Design:** Strict separation of data lifecycle components and execution pipelines.
✅ **Custom Telemetry:** Centralized custom logging and exception handling tracking system health.
✅ **Decision Intelligence UI:** Interactive Streamlit dashboard for real-time risk profiling.
✅ **Containerization:** Dockerized environment ensuring seamless cross-platform deployment.
✅ **Artifact Management:** Automated serialization and version control of preprocessors and models.

---

## 🔄 The Machine Learning Lifecycle

The system is built on a modular pipeline architecture, executing the following stages sequentially:

1. **SQL Profiling & EDA:** Initial Exploratory Data Analysis executed natively in MySQL to understand schema constraints, identify aggregate trends, and perform business-logic queries prior to extraction.
2. **Data Ingestion:** Extracts raw historical telecom data from local storage into the Python pipeline.
3. **Data Transformation:** Applies automated feature engineering, outlier handling, and categorical encoding.
4. **Model Training:** Trains and tunes classification algorithms optimized for imbalanced datasets.
5. **Model Evaluation:** Validates performance using F1-Scores and tests against the $78.92 VIP baseline logic.
6. **Model Pushing:** Serializes approved `model.pkl` and `preprocessor.pkl` files to the production `saved_models/` directory.
7. **Prediction Pipeline:** Consumes the serialized artifacts to serve real-time predictions via the web interface.

---

## 🐳 Docker Containerization

To ensure absolute reproducibility across any operating system without dependency conflicts, this project is containerized. 

**1. Build the Image:**
```bash
docker build -t cell2cell-churn-app .

2. Run the Container:

Bash

docker run -p 8501:8501 cell2cell-churn-app