# 🎓 EdTech Customer Intelligence Platform

A production-style AI analytics dashboard built with **Streamlit**, **Plotly**, and **Python**. This project combines learner engagement intelligence, review analytics, churn risk insights, and reusable dashboard engineering patterns.

## What this project showcases
- Modern dashboard UI with responsive layout and reusable components
- Data engineering for EdTech engagement and churn analytics
- Modular service architecture with cache management
- Automated insights and export capabilities
- Clean portfolio-ready documentation and packaging

---

## 🚀 Features

### Platform Analytics
- Learner engagement KPIs
- Activity and churn distribution
- Segment-level comparisons
- Retention and inactivity trends

### Learner Analytics
- Filter-driven cohort analysis
- Engagement and inactivity buckets
- Retention curve visualization
- Churn risk monitoring
- Downloadable cohort exports

### Review Intelligence
- Rating and sentiment distribution
- Review theme extraction
- Keyword-driven review analysis
- Search and filter reviews with export support

### AI Insights
- Deterministic business signals
- Churn anomaly detection
- Engagement drop candidate identification
- LLM-ready insight scaffold

### Settings & System Management
- Runtime cache invalidation
- Cache TTL controls
- Data source metadata panel
- Lightweight app health checks

---

## 🏗️ Architecture

```bash
edtech-customer-intelligence/
├── app/
│   ├── main.py              # Streamlit app entry and routing
│   ├── pages/               # Dashboard page layouts
│   ├── services/            # Data and analytics service layer
│   ├── components/          # Reusable UI components
│   └── config.py            # Central constants and paths
├── data/                    # Raw CSV data sources
├── models/                  # Model artifacts and outputs
├── notebooks/               # EDA and feature engineering workbooks
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🛠️ Tech Stack

- Python 3.11+
- Streamlit
- Plotly
- pandas
- NumPy
- scikit-learn
- NLTK

---

## 📦 Installation

```bash
git clone https://github.com/your-username/edtech-customer-intelligence.git
cd edtech-customer-intelligence
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py
```

---

## 📁 Data Structure

- `data/junyi/raw/Info_UserData.csv` — learner demographics
- `data/junyi/raw/Log_Problem.csv` — activity logs
- `data/reviews/raw/reviews.csv` — student review text

---

## 📸 Screenshots

> Add screenshots here for the Home, Learner Analytics, Review Intelligence, and AI Insights pages.

---

## ✅ Portfolio Highlights

- Professional dashboard layout with reusable UI components
- Centralized cache management and runtime TTL support
- Lightweight verification utilities for imports and data health
- Clean documentation and dependency packaging
- Minimal, polished `.gitignore` for clean repos

# ▶️ Run Application

```bash
streamlit run app/main.py
```

App will run on:

```bash
http://localhost:8501
```

---

# 📂 Datasets Used

## User Dataset
- User activity information
- learner engagement behavior
- inactivity tracking

## Activity Dataset
- learning interactions
- platform events
- engagement logs

## Review Dataset
- student reviews
- ratings
- review text feedback

---

# 📸 Screenshots

## Home Dashboard
- KPI cards
- engagement charts
- churn distribution
- segment analysis

## Review Intelligence
- sentiment analytics
- keyword extraction
- review filtering
- rating distributions

## Settings Page
- cache controls
- diagnostics
- configuration management

---

# 🧪 Future Improvements

- Real-time analytics pipeline
- LLM-powered insight generation
- Recommendation systems
- Predictive retention modeling
- Time-series forecasting
- Advanced NLP clustering
- Authentication system
- Cloud deployment

---

# 🎯 Project Goals

This project was built to demonstrate:
- applied machine learning engineering
- analytics dashboard development
- production-oriented architecture
- NLP integration
- ML system modularization
- data product thinking

---

# 📚 Key Learning Outcomes

- Designing scalable ML dashboards
- Building modular analytics systems
- Applying NLP to real datasets
- Engineering production-style Streamlit apps
- Managing caching and performance
- Structuring reusable service layers

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Built as an applied ML engineering and analytics portfolio project.
