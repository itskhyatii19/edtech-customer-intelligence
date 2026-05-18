# 🎓 EdTech Customer Intelligence Platform

An ML-powered analytics dashboard built with **Streamlit**, **Plotly**, and **Python** to analyze student engagement, review sentiment, churn risk, and learning behavior in EdTech platforms.

Designed as a production-style applied machine learning and analytics project focused on:
- learner engagement intelligence
- review analytics
- churn analysis
- operational dashboard engineering
- modular ML system design

---

#  Features

## 📊 Platform Analytics
- Total learner tracking
- Engagement score analysis
- Activity distribution
- User segmentation
- Churn risk analysis
- Retention insights

---

## 💬 Review Intelligence
- Review sentiment analysis
- Rating distribution
- Positive/negative review tracking
- Keyword & theme extraction
- Search and filter reviews
- NLP-powered review analytics

---

##  Learner Analytics
- Engagement trends
- Activity behavior analysis
- Segment comparison
- Active vs inactive learner analysis
- Retention-oriented insights

---

##  AI Insights Engine
- Automated analytics insights
- Engagement anomaly detection
- Risk pattern identification
- Recommendation generation
- Business intelligence summaries

---

## ⚙️ Settings & Data Management
- Dynamic cache management
- Configurable cache TTL
- Runtime cache invalidation
- Feature engineering controls
- Dataset information panel
- Application diagnostics

---

## 📁 Export Functionality
- CSV exports
- Filtered review exports
- Analytics summary downloads

---

#  Machine Learning & Analytics

## Implemented ML / Analytics Logic
- Engagement scoring
- User segmentation
- Churn risk scoring
- Sentiment classification
- Keyword extraction
- TF-IDF based NLP processing
- Activity trend analysis

---

## Churn Prediction Logic
Churn risk is calculated using:
- engagement score
- inactivity duration
- activity frequency
- weighted scoring thresholds

Risk bands:
- Low Risk
- Medium Risk
- High Risk

---

## NLP Pipeline
Review intelligence uses:
- TF-IDF vectorization
- stopword removal
- n-gram extraction
- phrase extraction
- sentiment grouping

---

# 🏗️ Architecture

## Project Structure

```bash
edtech-customer-intelligence/
│
├── app/
│   ├── main.py
│   ├── pages/
│   ├── services/
│   ├── components/
│   └── config.py
│
├── src/
│   ├── features/
│   ├── llm/
│   ├── pipelines/
│   └── utils/
│
├── data/
│   ├── junyi/
│   └── reviews/
│
├── models/
├── tests/
├── notebooks/
└── requirements.txt
```

---

# 🧩 Tech Stack

## Frontend / Dashboard
- Streamlit
- Plotly

## Backend / Processing
- Python
- Pandas
- NumPy

## Machine Learning / NLP
- Scikit-learn
- NLTK

## Engineering
- Modular service architecture
- Dynamic caching
- Reusable components
- Config-driven settings

---

# ⚡ Performance Optimizations

- Streamlit caching
- Runtime cache TTL management
- Cached analytics computations
- Reusable service layer
- Optimized dataframe operations

---

# 📈 Dashboard Pages

| Page | Description |
|------|-------------|
| Home | KPI overview and platform analytics |
| Learner Analytics | Engagement and retention insights |
| Review Intelligence | NLP and sentiment analytics |
| AI Insights | Automated business insights |
| Settings | Cache and system management |

---

# 🖥️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/your-username/edtech-customer-intelligence.git
cd edtech-customer-intelligence
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

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
