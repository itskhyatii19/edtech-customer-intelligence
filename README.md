# 🎓 EdTech Customer Intelligence Platform

AI-powered learner intelligence platform for engagement analytics, review intelligence, churn-risk assessment, predictive analytics, and executive decision support.

Built with:

**Python • Streamlit • Plotly • scikit-learn • NLP • Analytics Engineering**

---

#  Core Features

##  Executive Analytics Dashboard

* Executive KPI overview
* Learner engagement intelligence
* Churn risk monitoring
* Platform health summaries
* Review intelligence metrics
* Business-oriented insight cards
* Executive retention indicators
* Actionable intervention recommendations

---

# 🧠 AI Insights Engine

Production-style business intelligence system featuring:

* Executive findings generation
* Retention health analysis
* Engagement quality monitoring
* Sentiment health analysis
* Churn anomaly identification
* Recommendation engine
* Action-oriented interventions
* Explainable business rules

### Recommendation Logic

Examples:

* High churn risk + inactivity → Re-engagement campaign
* Negative sentiment spikes → Course quality review
* Moderate-risk learner growth → Targeted learner nudges

---

#  Learner Analytics

Advanced learner intelligence dashboard featuring:

* Cohort-level analytics
* Learner segmentation
* Engagement scoring
* Retention analysis
* Inactivity monitoring
* Activity frequency distributions
* Churn risk monitoring
* Engagement vs inactivity visualization
* Downloadable cohort exports

---

#  Review Intelligence (NLP)

AI-powered review analytics pipeline featuring:

* Sentiment distribution analysis
* Keyword extraction
* Theme discovery
* Positive vs negative review themes
* TF-IDF based topic intelligence
* N-gram extraction
* Search & filter functionality
* Exportable review datasets
* Actionable learner feedback insights

---

#  Predictive Analytics

Production-style predictive intelligence dashboard featuring:

* Churn risk scoring
* Risk segmentation (High / Medium / Low)
* Anomaly detection
* Intervention recommendations
* Model status monitoring
* Training metadata tracking
* Risk distribution visualization
* Executive retention insights

### Predictive Intelligence Services

#### PredictiveService

* Model training workflows
* Model persistence
* Prediction APIs
* Metadata management
* Feature importance support
* Explainability extension points

#### AnomalyService

* Learner anomaly detection
* Outlier identification
* Statistical fallback analysis

#### RecommendationService

* Rule-based intervention generation
* Risk mitigation recommendations
* Retention improvement actions

---

# 🤖 Churn Intelligence Pipeline

Current capabilities:

* Deterministic churn scoring engine
* Risk band classification
* Feature-engineered learner analytics
* Modular ML-ready architecture
* Model persistence and metadata tracking
* Graceful fallback behavior when ML dependencies are unavailable

Supported architecture:

* Random Forest training pipeline
* Model registry management
* Prediction APIs
* Feature importance tracking
* Future explainability integration

---

#  Engineering Features

## Modular Architecture

* Reusable service-layer design
* Centralized configuration management
* Modular UI components
* Clean analytics separation
* Scalable project organization

## Performance Optimization

* Runtime cache management
* Configurable cache TTL
* Optimized dataset loading
* Reduced recomputation overhead
* Lightweight validation utilities

## Reliability & Validation

* Data validation helpers
* Import verification checks
* Runtime diagnostics
* Graceful error handling
* Page render validation

## Logging & Debugging

* Centralized logger utility
* Service-level diagnostics
* Structured debugging outputs
* Easier runtime troubleshooting

---

# 🖥️ Dashboard Pages

##  Overview Dashboard

* Executive KPI cards
* Engagement summaries
* Churn overview
* Platform-wide intelligence

##  Learner Analytics

* Cohort analysis
* Retention trends
* Engagement buckets
* Inactivity analysis
* Risk monitoring

##  AI Insights

* Executive findings
* Business recommendations
* Platform health summaries
* Action-oriented insights

##  Predictive Analytics

* Model status monitoring
* Churn risk assessment
* Risk segmentation
* Intervention recommendations
* Retention intelligence

##  Review Intelligence

* Sentiment analysis
* NLP theme extraction
* Keyword intelligence
* Feedback analytics

## ⚙️ Settings & Diagnostics

* Cache controls
* Runtime diagnostics
* Data source metadata
* Health verification

---

# 🏛️ Project Architecture

```bash
edtech-customer-intelligence/
├── app/
│   ├── main.py
│   ├── pages/
│   │   ├── home.py
│   │   ├── learner_analytics.py
│   │   ├── ai_insights.py
│   │   ├── predictive_analytics.py
│   │   ├── review_intelligence.py
│   │   └── settings.py
│   │
│   ├── services/
│   │   ├── analytics_service.py
│   │   ├── churn_service.py
│   │   ├── insight_service.py
│   │   ├── review_service.py
│   │   ├── predictive_service.py
│   │   ├── anomaly_service.py
│   │   ├── recommendation_service.py
│   │   ├── validation.py
│   │   └── logger.py
│   │
│   ├── components/
│   ├── config.py
│   └── assets/
│
├── data/
│   ├── junyi/
│   └── reviews/
│
├── models/
├── notebooks/
├── reports/
├── requirements.txt
└── README.md
```

---

# 🛠️ Tech Stack

## Core

* Python 3.11+
* Streamlit
* Plotly
* Pandas
* NumPy

## Machine Learning

* scikit-learn
* Random Forest
* Feature Engineering
* Predictive Analytics Pipelines

## NLP & Analytics

* NLTK
* TF-IDF Vectorization
* Sentiment Analysis
* Keyword Extraction
* Topic Intelligence

---

# 📦 Installation

```bash
git clone https://github.com/your-username/edtech-customer-intelligence.git

cd edtech-customer-intelligence

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

streamlit run app/main.py
```

---

# ▶️ Run Application

```bash
streamlit run app/main.py
```

Application runs on:

```bash
http://localhost:8501
```

---

# 📂 Datasets Used

## User Dataset

Info_UserData.csv

* Learner demographics
* Engagement behavior
* Inactivity tracking

## Activity Dataset

Log_Problem.csv

* Learning interactions
* Platform activity logs
* Engagement events

## Review Dataset

reviews.csv

* Learner reviews
* Ratings
* Text feedback
* Sentiment analysis source

---

# 📈 Analytics Capabilities

## Engagement Intelligence

* Engagement scoring
* Learner segmentation
* Activity trend analysis
* Retention health monitoring

## Churn Intelligence

* Churn risk estimation
* Inactivity risk analysis
* Risk band classification
* High-risk learner detection

## Review Intelligence

* Sentiment health monitoring
* Topic extraction
* Keyword intelligence
* Actionable feedback insights

## Predictive Intelligence

* Risk scoring
* Anomaly detection
* Recommendation generation
* Retention intervention support

---

# 📸 Screenshots

Add screenshots for:

* Overview Dashboard
* Learner Analytics
* AI Insights
* Predictive Analytics
* Review Intelligence
* Settings & Diagnostics

---

# ✅ Engineering Highlights

* Modular analytics service architecture
* Predictive analytics framework
* NLP-powered review intelligence
* Production-style dashboard engineering
* Reusable Streamlit component system
* Runtime cache management
* Validation and diagnostics utilities
* Centralized logging framework
* Business-oriented AI insights

---

#  Future Improvements

## Machine Learning

* Behavior-based churn labels
* Advanced predictive modeling
* SHAP explainability
* Model comparison dashboard
* Automated retraining pipelines
* Drift monitoring

## AI Features

* LLM-powered executive summaries
* RAG-based analytics assistant
* Conversational analytics querying
* Semantic review search

## Product Enhancements

* Authentication system
* Role-based dashboards
* Cloud deployment
* Real-time analytics pipeline
* Automated reporting exports

---

# 🎯 Project Goals

This project demonstrates:

* Applied machine learning engineering
* Analytics product development
* NLP integration in business workflows
* Predictive analytics architecture
* Business intelligence systems
* Production-oriented dashboard engineering
* Data product thinking

---

#  Key Learning Outcomes

* Designing modular ML systems
* Building scalable analytics dashboards
* Applying NLP pipelines to real-world review data
* Engineering production-style Streamlit applications
* Managing caching and performance optimization
* Structuring reusable service architectures
* Translating ML outputs into business decisions

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Built as an applied AI/ML engineering portfolio project focused on:

* Learner Analytics
* Churn Intelligence
* Predictive Analytics
* NLP Systems
* Executive Dashboards
* Business Intelligence
