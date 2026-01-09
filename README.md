# FedEx DCA Management System

**AI-powered Debt Collection Agency (DCA) Management System.**
Built for the FedEx Hackathon to automate customer debt recovery and optimize DCA allocation.

## 🚀 Key Features
- **AI Prediction Engine**: Predicts 'Recovery Likelihood' (High/Medium/Low) based on amount, delay, and history.
- **Smart Assignment**: Automatically routes cases to the best performing DCA for that region and difficulty level.
- **Real-Time Dashboard**: Visualizes "Amount at Risk", "Recovery Rates", and "DCA Performance" using Plotly.
- **Interactive Management**: Filter and prioritize active cases.

## 📦 Installation

1. **Clone/Download** this repository.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Requires: streamlit, pandas, scikit-learn, plotly, openpyxl)*

3. **Generate Synthetic Data** (Optional, creates fresh training data):
   ```bash
   python generate_data.py
   ```

## 🏃‍♂️ How to Run

1. **Train the Model** (First time only):
   ```bash
   python src/ml_engine.py
   ```
   *This trains the Random Forest model and saves `model.pkl`.*

2. **Launch the Web App**:
   ```bash
   streamlit run app.py
   ```

## 📂 Project Structure
- `app.py`: Main Streamlit application.
- `src/ml_engine.py`: AI Model logic (Training & Prediction).
- `src/logic.py`: Business logic (DCA Assignment, Mock Database).
- `generate_data.py`: Script to create 1000+ synthetic records.
- `requirements.txt`: Python package dependencies.

## 💡 Usage Flow
1. Go to **Upload Cases** tab.
2. Drag & Drop `training_data.csv` (or your own CSV).
3. Click **Process with AI**.
4. View results in **Dashboard** and **Active Cases**.
5. Check **AI Insights** for strategic recommendations.

---
*Built with ❤️ for FedEx Hackathon*
