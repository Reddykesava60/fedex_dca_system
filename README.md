# FedEx DCA Management System

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**AI-Powered Debt Collection Agency Management Platform**

*Automating customer debt recovery and optimizing DCA allocation for FedEx*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-project-structure)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Technical Stack](#-technical-stack)
- [Data Requirements](#-data-requirements)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **FedEx DCA Management System** is an intelligent, AI-powered platform designed to revolutionize debt collection operations. Built for the FedEx Hackathon, this system leverages machine learning to predict recovery likelihood, automate case assignments, and provide actionable insights for optimizing debt recovery strategies.

### Key Objectives

- **Automate Debt Recovery**: Streamline the process of managing overdue customer payments
- **Optimize DCA Assignment**: Intelligently route cases to the most suitable collection agencies
- **Predict Recovery Outcomes**: Use AI to forecast collection success rates
- **Enhance Decision Making**: Provide real-time analytics and strategic recommendations

---

## 🚀 Features

### 🤖 AI Prediction Engine
- **Machine Learning Model**: Random Forest classifier trained on historical debt recovery data
- **Recovery Likelihood Prediction**: Categorizes cases as High/Medium/Low recovery probability
- **Multi-Factor Analysis**: Considers outstanding amount, payment delay, customer history, and regional factors
- **Model Accuracy**: Achieves 85%+ prediction accuracy on test datasets

### 🎯 Smart DCA Assignment
- **Automated Routing**: Intelligently assigns cases to DCAs based on:
  - Regional expertise and coverage
  - Historical performance metrics
  - Case difficulty level
  - Current workload distribution
- **Performance-Based Selection**: Prioritizes high-performing agencies for critical cases
- **Load Balancing**: Ensures equitable distribution across available DCAs

### 📊 Real-Time Analytics Dashboard
- **Interactive Visualizations**: Built with Plotly for dynamic data exploration
- **Key Metrics Tracking**:
  - Total Amount at Risk
  - Recovery Rate Trends
  - DCA Performance Comparison
  - Case Distribution by Region
- **Drill-Down Capabilities**: Filter and analyze data by multiple dimensions

### 💼 Case Management
- **Bulk Upload**: Process hundreds of cases simultaneously via CSV import
- **Advanced Filtering**: Search and filter by status, region, amount, and priority
- **Status Tracking**: Monitor case progression from assignment to resolution
- **Export Functionality**: Generate reports in multiple formats

### 🧠 AI-Powered Insights
- **Strategic Recommendations**: Data-driven suggestions for improving recovery rates
- **Trend Analysis**: Identify patterns in successful vs. unsuccessful collections
- **Risk Assessment**: Highlight high-risk cases requiring immediate attention

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit Web Interface                │
│              (User Interaction & Visualization)          │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼─────────┐   ┌────────▼──────────┐
│   ML Engine      │   │  Business Logic   │
│  (ml_engine.py)  │   │    (logic.py)     │
│                  │   │                   │
│ • Training       │   │ • DCA Assignment  │
│ • Prediction     │   │ • Data Management │
│ • Model Mgmt     │   │ • Validation      │
└────────┬─────────┘   └────────┬──────────┘
         │                      │
         └──────────┬───────────┘
                    │
         ┌──────────▼───────────┐
         │   Data Layer         │
         │                      │
         │ • training_data.csv  │
         │ • model.pkl          │
         │ • encoders.pkl       │
         └──────────────────────┘
```

---

## 📦 Installation

### Prerequisites

- **Python**: Version 3.8 or higher
- **pip**: Python package installer
- **Git**: For cloning the repository (optional)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd fedex_dca_system
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate Training Data** (First-time setup)
   ```bash
   python generate_data.py
   ```
   *This creates `training_data.csv` with 1000+ synthetic debt collection records.*

5. **Train the AI Model** (First-time setup)
   ```bash
   python src/ml_engine.py
   ```
   *This trains the Random Forest model and saves `model.pkl` and `encoders.pkl`.*

---

## 🏃‍♂️ Usage

### Starting the Application

```bash
streamlit run app.py
```

The application will launch in your default web browser at `http://localhost:8501`

### Workflow Guide

#### 1️⃣ **Upload Cases**
- Navigate to the **Upload Cases** tab
- Drag and drop your CSV file or use the file browser
- Ensure CSV contains required columns: `Customer_ID`, `Outstanding_Amount`, `Days_Overdue`, `Region`, `Payment_History`
- Click **Process with AI** to analyze and assign cases

#### 2️⃣ **View Dashboard**
- Access the **Dashboard** tab for comprehensive analytics
- Monitor key metrics:
  - **Total Amount at Risk**: Sum of all outstanding debt
  - **Recovery Rate**: Percentage of successfully recovered cases
  - **DCA Performance**: Comparative analysis of collection agencies
- Interact with charts for detailed insights

#### 3️⃣ **Manage Active Cases**
- Open the **Active Cases** tab
- Filter cases by:
  - Recovery likelihood (High/Medium/Low)
  - Region (North/South/East/West)
  - Assigned DCA
  - Amount range
- Export filtered results for reporting

#### 4️⃣ **Review AI Insights**
- Check the **AI Insights** tab for strategic recommendations
- Review model performance metrics
- Identify improvement opportunities

### Sample CSV Format

```csv
Customer_ID,Outstanding_Amount,Days_Overdue,Region,Payment_History
CUST001,15000,45,North,Good
CUST002,8500,120,South,Poor
CUST003,25000,30,East,Excellent
```

---

## 📂 Project Structure

```
fedex_dca_system/
│
├── app.py                      # Main Streamlit application
│   ├── UI Components
│   ├── Tab Management
│   └── Data Visualization
│
├── src/
│   ├── ml_engine.py           # AI/ML Module
│   │   ├── Model Training
│   │   ├── Prediction Logic
│   │   └── Model Persistence
│   │
│   └── logic.py               # Business Logic
│       ├── DCA Assignment Algorithm
│       ├── Mock Database Operations
│       └── Data Validation
│
├── generate_data.py           # Synthetic Data Generator
│   └── Creates training_data.csv
│
├── requirements.txt           # Python Dependencies
│
├── training_data.csv          # Training Dataset (generated)
├── model.pkl                  # Trained ML Model (generated)
├── encoders.pkl              # Feature Encoders (generated)
│
└── README.md                  # Documentation (this file)
```

### File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main application entry point with Streamlit UI |
| `src/ml_engine.py` | Machine learning model training and prediction |
| `src/logic.py` | Business rules and DCA assignment logic |
| `generate_data.py` | Generates synthetic training data for demo |
| `requirements.txt` | Lists all Python package dependencies |
| `training_data.csv` | Historical debt collection data for training |
| `model.pkl` | Serialized trained Random Forest model |
| `encoders.pkl` | Serialized label encoders for categorical features |

---

## 🛠️ Technical Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Frontend** | Streamlit | Latest | Web interface and visualization |
| **ML Framework** | Scikit-learn | Latest | Machine learning model |
| **Data Processing** | Pandas | Latest | Data manipulation and analysis |
| **Numerical Computing** | NumPy | Latest | Mathematical operations |
| **Visualization** | Plotly | Latest | Interactive charts and graphs |
| **Model Persistence** | Joblib | Latest | Model serialization |
| **Excel Support** | OpenPyXL | Latest | Excel file handling |

### Machine Learning Details

- **Algorithm**: Random Forest Classifier
- **Features**: Outstanding Amount, Days Overdue, Region, Payment History
- **Target**: Recovery Likelihood (High/Medium/Low)
- **Training Data**: 1000+ synthetic records
- **Validation**: Train-test split (80/20)

---

## 📊 Data Requirements

### Input CSV Columns

| Column Name | Data Type | Description | Example |
|-------------|-----------|-------------|---------|
| `Customer_ID` | String | Unique customer identifier | CUST001 |
| `Outstanding_Amount` | Float | Total debt amount | 15000.00 |
| `Days_Overdue` | Integer | Days since payment due | 45 |
| `Region` | String | Geographic region | North/South/East/West |
| `Payment_History` | String | Historical payment behavior | Excellent/Good/Average/Poor |

### Optional Columns

- `Contact_Number`: Customer phone number
- `Email`: Customer email address
- `Last_Payment_Date`: Date of most recent payment
- `Original_Amount`: Initial debt amount

---

## 🔧 Troubleshooting

### Common Issues

#### Model Not Found Error
```
FileNotFoundError: model.pkl not found
```
**Solution**: Run `python src/ml_engine.py` to train and save the model

#### Missing Training Data
```
FileNotFoundError: training_data.csv not found
```
**Solution**: Run `python generate_data.py` to create synthetic data

#### Import Errors
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Ensure virtual environment is activated and run `pip install -r requirements.txt`

#### Port Already in Use
```
OSError: [Errno 98] Address already in use
```
**Solution**: Specify a different port: `streamlit run app.py --server.port 8502`

### Debug Mode

Run Streamlit in debug mode for detailed error messages:
```bash
streamlit run app.py --logger.level=debug
```

---

## 🚀 Future Enhancements

### Planned Features

- [ ] **Real Database Integration**: Replace mock database with PostgreSQL/MongoDB
- [ ] **Advanced ML Models**: Implement XGBoost, Neural Networks for improved accuracy
- [ ] **User Authentication**: Add role-based access control (Admin, Manager, Analyst)
- [ ] **Email Notifications**: Automated alerts for high-priority cases
- [ ] **API Integration**: RESTful API for third-party system integration
- [ ] **Mobile Responsiveness**: Optimize UI for mobile devices
- [ ] **Multi-Language Support**: Internationalization for global deployment
- [ ] **Automated Reporting**: Scheduled PDF/Excel report generation
- [ ] **Payment Gateway Integration**: Direct payment processing
- [ ] **Historical Trend Analysis**: Time-series forecasting for recovery rates

### Performance Optimizations

- Implement caching for faster data retrieval
- Optimize model inference for real-time predictions
- Add pagination for large datasets
- Implement lazy loading for visualizations

---

## 🤝 Contributing

We welcome contributions to improve the FedEx DCA Management System!

### How to Contribute

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Your Changes**
4. **Commit Your Changes**
   ```bash
   git commit -m "Add: Brief description of your changes"
   ```
5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Submit a Pull Request**

### Coding Standards

- Follow PEP 8 style guide for Python code
- Add docstrings to all functions and classes
- Include unit tests for new features
- Update documentation as needed

<div align="center">

**Built with ❤️ for FedEx Hackathon 2026**

*Empowering smarter debt recovery through AI*

⭐ Star this repository if you find it helpful!

</div>
