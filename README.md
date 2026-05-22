# 🎓 EdTech Customer Intelligence Platform

A production-style AI/ML analytics platform built with **Streamlit**, **Plotly**, **scikit-learn**, and **Python** for learner engagement intelligence, churn prediction, review analytics, and executive business insights.

This project combines:
- analytics engineering
- machine learning workflows
- NLP pipelines
- business intelligence dashboards
- modular service architecture
- production-oriented Streamlit engineering

---

#  Core Features

## 📊 Executive Analytics Dashboard
- Executive KPI overview
- Learner engagement intelligence
- Churn risk monitoring
- Platform health summaries
- Review intelligence metrics
- Business-oriented insight cards

---

# 🧠 AI Insights Engine

Production-style business intelligence system with:
- Executive findings generation
- Retention health analysis
- Engagement quality analysis
- Sentiment health monitoring
- Churn anomaly detection
- Deterministic recommendation engine
- Actionable intervention suggestions
- Explainable business rules

### Recommendation Logic
Examples:
- High churn risk + inactivity → re-engagement campaign
- Negative sentiment spikes → course quality review
- Moderate-risk learner growth → targeted nudges

---

# 👥 Learner Analytics

Advanced learner intelligence dashboard featuring:
- Cohort-level analytics
- Engagement segmentation
- Retention analysis
- Inactivity monitoring
- Activity frequency distribution
- Churn risk distribution
- Engagement vs inactivity visualization
- Downloadable cohort exports

---

# 💬 Review Intelligence (NLP)

AI-powered review analytics pipeline with:
- Sentiment distribution
- Keyword extraction
- Theme analysis
- Positive vs negative review themes
- TF-IDF based topic intelligence
- n-gram extraction
- Search & filter reviews
- Export filtered datasets
- Actionable learner feedback patterns

---

# 🤖 Machine Learning Systems

## Churn Prediction Pipeline
- ML-driven churn scoring
- Probability-based risk prediction
- Feature-engineered learner analytics
- Modular sklearn pipeline architecture
- Explainable risk classification

## Feature Engineering
Features include:
- engagement score
- inactivity days
- activity frequency
- review sentiment
- learner segment classification
- churn indicators
- retention behavior

---

# 🏗️ Engineering Features

## Modular Architecture
- Reusable service-layer design
- Clean analytics separation
- Centralized configuration
- Modular UI components
- Scalable project organization

## Performance Optimization
- Runtime cache management
- Configurable cache TTL
- Lightweight validation utilities
- Optimized dataset loading
- Reduced recomputation overhead

## Reliability & Validation
- Data validation helpers
- Import verification checks
- Lightweight diagnostics
- Graceful error handling
- Page render validation

## Logging & Debugging
- Centralized logger utility
- Service-level diagnostics
- Structured debug outputs
- Easier runtime troubleshooting

---

# 🖥️ Dashboard Pages

## 🏠 Overview Dashboard
- Executive KPI cards
- Engagement summaries
- Churn overview
- Platform-wide intelligence

## 👥 Learner Analytics
- Cohort analysis
- Retention trends
- Engagement buckets
- Inactivity analysis
- Risk monitoring

## 🧠 AI Insights
- Executive findings
- Business recommendations
- Platform health summaries
- Action-oriented insights

## 💬 Review Intelligence
- Sentiment analysis
- NLP theme extraction
- Keyword intelligence
- Feedback analytics

## ⚙️ Settings & Diagnostics
- Cache management
- Runtime controls
- Data source metadata
- App health diagnostics

---

# 🏛️ Project Architecture

```bash
edtech-customer-intelligence/
├── app/
│   ├── main.py                  # Streamlit entrypoint and routing
│   ├── pages/                   # Dashboard page layouts
│   ├── services/                # Analytics + ML service layer
│   │   ├── analytics_service.py
│   │   ├── churn_service.py
│   │   ├── insight_service.py
│   │   ├── review_service.py
│   │   ├── validation.py
│   │   └── logger.py
│   ├── components/              # Reusable UI components
│   ├── config.py                # Central configs/constants
│   └── assets/                  # Optional static assets
│
├── data/
│   ├── junyi/
│   └── reviews/
│
├── models/                      # ML artifacts and outputs
├── notebooks/                   # EDA + feature engineering
├── reports/                     # Generated outputs/reports
├── requirements.txt
└── README.md
```

---

# 🛠️ Tech Stack

## Core
- Python 3.11+
- Streamlit
- Plotly
- pandas
- NumPy

## Machine Learning
- scikit-learn
- TF-IDF Vectorization
- NLP preprocessing
- Feature engineering

## NLP & Analytics
- NLTK
- sentiment analysis
- keyword extraction
- review intelligence pipelines

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

App runs on:

```bash
http://localhost:8501
```

---

# 📂 Datasets Used

## User Dataset
`Info_UserData.csv`
- learner demographics
- engagement behavior
- inactivity tracking

## Activity Dataset
`Log_Problem.csv`
- learning interactions
- platform activity logs
- engagement events

## Review Dataset
`reviews.csv`
- learner reviews
- ratings
- text feedback
- sentiment analysis source

---

# 📈 Analytics Capabilities

## Engagement Intelligence
- engagement scoring
- learner segmentation
- activity trend analysis
- retention health

## Churn Intelligence
- churn probability estimation
- inactivity risk analysis
- anomaly detection signals
- high-risk cohort detection

## Review Intelligence
- sentiment health
- NLP topic extraction
- keyword analytics
- actionable feedback signals

---

# 📸 Screenshots

## Overview Dashboard
- KPI cards
- executive metrics
- engagement intelligence
- churn analytics

## Learner Analytics
- cohort segmentation
- retention curves
- inactivity trends
- engagement distributions

## AI Insights
- executive findings
- platform health summaries
- recommendation engine
- business alerts

## Review Intelligence
- sentiment analysis
- keyword themes
- review filtering
- NLP intelligence

## Settings & Diagnostics
- cache controls
- runtime diagnostics
- health verification

> Add actual screenshots/GIFs here before publishing.

---

# ✅ Engineering Highlights

- Modular ML service architecture
- Production-style analytics layering
- Reusable Streamlit component system
- Runtime cache invalidation utilities
- Lightweight validation framework
- Centralized logging utilities
- Portfolio-grade project organization
- Business-oriented AI insight generation

---

# 🧪 Future Improvements

## Advanced AI Features
- LLM-powered executive summaries
- RAG-based analytics assistant
- conversational data querying
- semantic review search

## ML Improvements
- SHAP explainability
- anomaly detection models
- recommendation ranking engine
- predictive retention forecasting

## Product Features
- authentication system
- role-based dashboards
- cloud deployment
- real-time analytics pipeline
- automated reporting exports

---

# 🎯 Project Goals

This project demonstrates:
- applied machine learning engineering
- analytics product development
- NLP integration in real workflows
- business intelligence systems
- production-oriented dashboard engineering
- scalable analytics architecture
- data product thinking

---

# 📚 Key Learning Outcomes

- Designing modular ML systems
- Building scalable analytics dashboards
- Applying NLP pipelines to review data
- Engineering production-style Streamlit apps
- Managing caching and runtime performance
- Structuring reusable analytics services
- Translating ML outputs into business insights

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

If contributing:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Built as an applied AI/ML engineering and analytics portfolio project focused on:
- business intelligence
- learner analytics
- churn prediction
- NLP systems
- executive dashboard engineering
