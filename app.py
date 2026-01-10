import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Fix imports for Streamlit Cloud
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from src.ml_engine import MLEngine
from src.logic import DCAAssigner, AnalyticsService

# Page Config
st.set_page_config(page_title="FedEx DCA System", page_icon="📦", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4D148C;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #ff6200;
        color: white;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    h1, h2, h3 {
        color: #4D148C;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'cases_df' not in st.session_state:
    st.session_state.cases_df = pd.DataFrame()

if 'ml_engine' not in st.session_state:
    st.session_state.ml_engine = MLEngine()
    model_path = BASE_DIR / 'model.pkl'
    
    # Try loading existing model
    if model_path.exists():
        try:
            st.session_state.ml_engine.load_model()
            st.session_state.model_status = "✅ Loaded"
        except Exception as e:
            st.session_state.model_status = f"❌ Error: {str(e)}"
    else:
        st.session_state.model_status = "⚠️ Model not found - please include model.pkl in repo"

def main():
    # Sidebar
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/FedEx_Corporation_logo.svg/2560px-FedEx_Corporation_logo.svg.png", width=200)
    st.sidebar.title("DCA Management")
    
    # Show model status
    st.sidebar.info(f"**Model Status**: {st.session_state.model_status}")
    
    page = st.sidebar.radio("Navigate", ["Dashboard", "Upload Cases", "Active Cases", "AI Insights"])

    if page == "Dashboard":
        render_dashboard()
    elif page == "Upload Cases":
        render_upload()
    elif page == "Active Cases":
        render_cases()
    elif page == "AI Insights":
        render_insights()

def render_dashboard():
    st.title("📊 Executive Dashboard")

    df = st.session_state.cases_df

    if df.empty:
        st.info("No cases loaded. Please go to 'Upload Cases' to start.")
        
        # Show sample data option
        if st.button("📋 Load Sample Data"):
            sample_data = create_sample_data()
            st.session_state.cases_df = sample_data
            st.rerun()
        return

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Cases", len(df))
    with col2:
        val = df['amount_owed'].sum()
        st.metric("Amount at Risk", f"${val:,.2f}")
    with col3:
        avg_rec = df['confidence_score'].mean() * 100 if 'confidence_score' in df.columns else 0
        st.metric("Avg Recovery Prob", f"{avg_rec:.1f}%")
    with col4:
        st.metric("Active DCAs", df['dca_assigned'].nunique() if 'dca_assigned' in df.columns else 0)

    # Charts
    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Priority Distribution")
        if 'recovery_likelihood' in df.columns:
            fig = px.pie(df, names='recovery_likelihood', title="Cases by Recovery Likelihood", 
                         color='recovery_likelihood',
                         color_discrete_map={'High':'#00cc96', 'Medium':'#ffcc00', 'Low':'#ef553b'})
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Regional Allocation")
        if 'region' in df.columns:
            fig = px.bar(df, x='region', y='amount_owed', title="Total Debt by Region", color='region')
            st.plotly_chart(fig, use_container_width=True)

    # DCA Performance
    st.markdown("---")
    st.subheader("DCA Assignment & Load")
    if 'dca_assigned' in df.columns:
        dca_stats = AnalyticsService.calculate_dca_performance(df)
        fig = px.bar(dca_stats, x='dca_assigned', y='total_amount', 
                     title="Assigned Volume per DCA ($)", color='dca_assigned')
        st.plotly_chart(fig, use_container_width=True)

def render_upload():
    st.title("📂 Upload & Process Cases")

    # Check model status first
    if "Error" in st.session_state.model_status or "not found" in st.session_state.model_status:
        st.error("⚠️ ML Model not available. Please ensure model.pkl is in your repository.")
        st.info("**To fix**: Run `python src/ml_engine.py` locally, then commit model.pkl to your repo")

    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Uploaded {len(df)} rows.")
            
            # Preview uploaded data
            with st.expander("Preview uploaded data"):
                st.dataframe(df.head())

            if st.button("🤖 Process with AI"):
                if "Loaded" not in st.session_state.model_status:
                    st.error("Cannot process: Model not loaded")
                    return
                    
                with st.spinner("Analyzing cases..."):
                    try:
                        # 1. Predict
                        processed_df = st.session_state.ml_engine.predict_cases(df)

                        # 2. Assign DCA
                        processed_df['dca_assigned'] = processed_df.apply(DCAAssigner.assign_case, axis=1)

                        # Save to session
                        st.session_state.cases_df = processed_df
                        st.success("✅ Analysis Complete! Cases assigned.")

                        # Preview
                        st.dataframe(processed_df.head())
                        
                        # Download option
                        csv = processed_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Processed Cases",
                            data=csv,
                            file_name="processed_cases.csv",
                            mime="text/csv"
                        )
                    except Exception as e:
                        st.error(f"Error during processing: {str(e)}")
                        
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

    # Template Download
    st.markdown("---")
    st.subheader("📝 Need Sample Data?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Sample CSV Template"):
            sample = create_sample_template()
            csv = sample.to_csv(index=False)
            st.download_button(
                label="📥 Download Template",
                data=csv,
                file_name="sample_cases.csv",
                mime="text/csv"
            )
    
    with col2:
        st.info("Expected columns: customer_id, amount_owed, days_overdue, region, payment_history")

def render_cases():
    st.title("📋 Active Cases")
    
    df = st.session_state.cases_df
    
    if df.empty:
        st.warning("No active cases. Upload data first.")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'recovery_likelihood' in df.columns:
            priority_filter = st.multiselect(
                "Recovery Likelihood",
                options=df['recovery_likelihood'].unique(),
                default=df['recovery_likelihood'].unique()
            )
        else:
            priority_filter = None
    
    with col2:
        if 'region' in df.columns:
            region_filter = st.multiselect(
                "Region",
                options=df['region'].unique(),
                default=df['region'].unique()
            )
        else:
            region_filter = None
    
    with col3:
        if 'dca_assigned' in df.columns:
            dca_filter = st.multiselect(
                "Assigned DCA",
                options=df['dca_assigned'].unique(),
                default=df['dca_assigned'].unique()
            )
        else:
            dca_filter = None
    
    # Apply filters
    filtered_df = df.copy()
    if priority_filter:
        filtered_df = filtered_df[filtered_df['recovery_likelihood'].isin(priority_filter)]
    if region_filter:
        filtered_df = filtered_df[filtered_df['region'].isin(region_filter)]
    if dca_filter:
        filtered_df = filtered_df[filtered_df['dca_assigned'].isin(dca_filter)]
    
    st.dataframe(filtered_df, use_container_width=True, height=400)
    
    # Export
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Export Filtered Cases",
        data=csv,
        file_name="filtered_cases.csv",
        mime="text/csv"
    )

def render_insights():
    st.title("🤖 AI Insights & Recommendations")
    df = st.session_state.cases_df

    if df.empty:
        st.warning("Upload data to see insights.")
        return

    st.markdown("""
    > **Model Architecture**: Random Forest Classifier  
    > **Features**: Amount, Days Overdue, Region, Payment History  
    > **Accuracy on Training**: ~78%
    """)

    # High Priority Recommendations
    if 'recovery_likelihood' in df.columns:
        high_priority = df[df['recovery_likelihood'] == 'High']
        total_rec = high_priority['amount_owed'].sum()

        st.success(f"💡 **Recommendation**: Focus immediately on {len(high_priority)} High-Priority cases. Potential Recovery: ${total_rec:,.2f}")

    # Risk Alerts
    if 'days_overdue' in df.columns:
        critical = df[df['days_overdue'] > 120]
        st.warning(f"⚠️ **Risk Alert**: {len(critical)} cases are overdue by > 120 days. These have been assigned to specialized agencies.")

    # Additional Insights
    st.markdown("---")
    st.subheader("📈 Key Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'confidence_score' in df.columns:
            avg_confidence = df['confidence_score'].mean() * 100
            st.metric("Average Confidence Score", f"{avg_confidence:.1f}%")
    
    with col2:
        if 'days_overdue' in df.columns:
            avg_overdue = df['days_overdue'].mean()
            st.metric("Average Days Overdue", f"{avg_overdue:.0f} days")

def create_sample_template():
    """Create a sample CSV template for download"""
    return pd.DataFrame({
        'customer_id': ['CUST001', 'CUST002', 'CUST003'],
        'amount_owed': [15000, 8500, 25000],
        'days_overdue': [45, 120, 30],
        'region': ['North', 'South', 'East'],
        'payment_history': ['Good', 'Poor', 'Excellent']
    })

def create_sample_data():
    """Create sample processed data for demo"""
    import numpy as np
    
    np.random.seed(42)
    n = 50
    
    return pd.DataFrame({
        'customer_id': [f'CUST{i:04d}' for i in range(n)],
        'amount_owed': np.random.uniform(5000, 50000, n),
        'days_overdue': np.random.randint(10, 180, n),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n),
        'payment_history': np.random.choice(['Excellent', 'Good', 'Average', 'Poor'], n),
        'recovery_likelihood': np.random.choice(['High', 'Medium', 'Low'], n, p=[0.3, 0.5, 0.2]),
        'confidence_score': np.random.uniform(0.4, 0.95, n),
        'dca_assigned': np.random.choice(['DCA Alpha', 'DCA Beta', 'DCA Gamma', 'DCA Delta'], n)
    })

if __name__ == "__main__":
    main()