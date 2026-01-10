import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.ml_engine import MLEngine
from src.logic import DCAAssigner, AnalyticsService
import os

from generate_data import generate_synthetic_data

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
        color: #4D148C; /* FedEx Purple */
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'cases_df' not in st.session_state:
    st.session_state.cases_df = pd.DataFrame()
if 'ml_engine' not in st.session_state:
    st.session_state.ml_engine = MLEngine()
    # Try loading existing model
    if os.path.exists('model.pkl'):
        st.session_state.ml_engine.load_model()

def main():
    # Sidebar
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/FedEx_Corporation_logo.svg/2560px-FedEx_Corporation_logo.svg.png", width=200)
    st.sidebar.title("DCA Management")
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

    # DCA Performance (Projected)
    st.markdown("---")
    st.subheader("DCA Assignment & Load")
    if 'dca_assigned' in df.columns:
        dca_stats = AnalyticsService.calculate_dca_performance(df)
        fig = px.bar(dca_stats, x='dca_assigned', y='total_amount', title="Assigned Volume per DCA ($)", color='dca_assigned')
        st.plotly_chart(fig, use_container_width=True)

def render_upload():
    st.title("📂 Upload & Process Cases")

    st.info("You can either upload your own CSV file or auto-generate a sample dataset.")

    # ---------- UPLOAD CSV ----------
    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=["csv"],
        help="Upload a CSV file with debt case data"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Uploaded {len(df)} rows.")
            st.dataframe(df.head())

            if st.button("⚙️ Process with AI"):
                with st.spinner("Analyzing cases..."):
                    processed_df = st.session_state.ml_engine.predict_cases(df)
                    processed_df['dca_assigned'] = processed_df.apply(
                        DCAAssigner.assign_case, axis=1
                    )

                    st.session_state.cases_df = processed_df
                    st.success("🎯 Analysis complete!")
                    st.dataframe(processed_df.head())

        except Exception as e:
            st.error(f"❌ Error processing CSV: {e}")

    st.divider()

    # ---------- AUTO GENERATE ----------
    st.subheader("🔄 Auto Generate Sample Dataset")

    if st.button("Generate Synthetic Dataset"):
        try:
            df = generate_synthetic_data(1000)

            st.session_state.cases_df = df
            st.success("✅ Synthetic dataset generated!")
            st.dataframe(df.head())

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇️ Download Dataset (CSV)",
                data=csv,
                file_name="training_data.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"❌ Error generating dataset: {e}")

def render_insights():
    st.title("🤖 AI Insights & Recommendations")
    df = st.session_state.cases_df
    
    if df.empty:
        st.warning("Upload data to see insights.")
        return
        
    st.markdown("""
    > **Model Architecture**: Random Forest Classifier  
    > **Accuracy on Training**: ~78%
    """)
    
    high_priority = df[df['recovery_likelihood'] == 'High']
    total_rec = high_priority['amount_owed'].sum()
    
    st.success(f"💡 **Recommendation**: Focus immediately on {len(high_priority)} High-Priority cases. Potential Recovery: ${total_rec:,.2f}")
    
    st.info(f"⚠️ **Risk Alert**: {len(df[df['days_overdue'] > 120])} cases are overdue by > 120 days. These have been assigned to specialized agencies.")

if __name__ == "__main__":
    main()
