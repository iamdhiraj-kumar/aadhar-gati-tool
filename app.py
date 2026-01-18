import streamlit as st
import pandas as pd
import plotly.express as px  # We use Plotly for interactive, pro-level graphs
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Aadhaar-Gati Tool", layout="wide")

# Try to load the logo
try:
    logo = Image.open("uidai_logo.png")
    st.image(logo, width=180)
except FileNotFoundError:
    st.warning("⚠️ 'uidai_logo.png' not found. Ensure it is in the same folder.")

st.title("Aadhaar-Gati: Smart Resource Allocation Tool")
st.markdown("**Data-driven optimization of Aadhaar services using 75th Percentile Thresholding**")

# 2. File Upload
uploaded_file = st.file_uploader("Upload Aadhaar District Data (CSV or Excel)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    # Load data based on file type
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("1. Raw Data Preview")
    st.dataframe(df.head())

    # 3. Main Analysis Button
    if st.button("Run Analysis & Generate Report"):
        
        # --- STEP A: Aggregation ---
        district_data = df.groupby("District").agg({
            "Update_Count": "sum",
            "New_Enrolment_Count": "sum"
        }).reset_index()

        # --- STEP B: The "75th Percentile" Logic ---
        enrollment_threshold = district_data["New_Enrolment_Count"].quantile(0.75)
        update_threshold = district_data["Update_Count"].quantile(0.75)
        low_threshold = district_data["Update_Count"].quantile(0.25)

        st.info(f"📊 **Smart Thresholds Calculated:**\n- High Traffic (Updates): > {int(update_threshold)}\n- High Traffic (Enrollment): > {int(enrollment_threshold)}")

        # --- STEP C: Classification Function ---
        def classify(row):
            if row["Update_Count"] > update_threshold or row["New_Enrolment_Count"] > enrollment_threshold:
                return "High Traffic Zone"
            elif row["Update_Count"] < low_threshold:
                return "Ghost Zone"
            else:
                return "Balanced Zone"

        district_data["Zone"] = district_data.apply(classify, axis=1)

        # --- STEP D: Recommendations ---
        def recommend(zone):
            if zone == "High Traffic Zone":
                return "Deploy Permanent Staff & Server Upgrade"
            elif zone == "Ghost Zone":
                return "Deploy Mobile Aadhaar Vans"
            else:
                return "Standard Operations"

        district_data["Recommended_Action"] = district_data["Zone"].apply(recommend)
        
        # Save to session state so data persists
        st.session_state['result'] = district_data
        st.success("✅ Analysis Completed Successfully")

# --- CHECK IF RESULT EXISTS IN SESSION STATE ---
if 'result' in st.session_state:
    district_data = st.session_state['result']

    # --- STEP E: Advanced Visualizations (For Page 7) ---
    st.markdown("---")
    st.header("Visual Insights")

    # Layout: Top row with 2 charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Enrollment vs. Update Trends")
        # Scatter Plot: Shows the relationship
        fig_scatter = px.scatter(
            district_data, 
            x="New_Enrolment_Count", 
            y="Update_Count", 
            color="Zone",
            size="Update_Count",
            hover_name="District",
            title="District Cluster Analysis"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("2. Zone Distribution")
        # Pie Chart: Shows what % of districts are High Traffic vs Ghost
        zone_counts = district_data["Zone"].value_counts().reset_index()
        zone_counts.columns = ["Zone", "Count"]
        fig_pie = px.pie(zone_counts, values="Count", names="Zone", title="Percentage of Zones in UP")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Layout: Bottom row with Bar Chart
    st.subheader("3. Top 30 High-Load Districts (Updates)")
    # Filter for Top 30 only
    top_30_data = district_data.sort_values(by="Update_Count", ascending=False).head(30)
    
    fig_bar = px.bar(
        top_30_data,
        x="District",
        y="Update_Count",
        color="Zone",
        title="Top 30 Districts requiring immediate attention",
        text_auto=True
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # --- STEP F: Final Data Table & Download ---
    st.markdown("---")
    st.subheader("Final Allocation Report")
    
    # Filter mechanism
    zone_filter = st.multiselect("Filter by Zone", district_data["Zone"].unique(), default=district_data["Zone"].unique())
    filtered_final = district_data[district_data["Zone"].isin(zone_filter)]
    
    st.dataframe(filtered_final, use_container_width=True)

    # Download Button
    csv = filtered_final.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Final Report (CSV)",
        data=csv,
        file_name="aadhaar_gati_allocation.csv",
        mime="text/csv"
    )
