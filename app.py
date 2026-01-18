import streamlit as st
import pandas as pd
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Aadhaar-Gati Tool", layout="wide")

# Try to load the logo
try:
    logo = Image.open("uidai_logo.png")
    st.image(logo, width=180)
except FileNotFoundError:
    st.warning("⚠️ 'uidai_logo.png' not found.")

st.title("Aadhaar-Gati: Smart Resource Allocation Tool")
st.markdown("**Data-driven optimization of Aadhaar services using 75th Percentile Thresholding**")

# 2. File Upload
uploaded_file = st.file_uploader("Upload Aadhaar District Data", type=["csv", "xlsx", "xls"])

if uploaded_file:
    # Load data
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
        
        # Save to session state
        st.session_state['result'] = district_data
        st.success("✅ Analysis Completed Successfully")

# --- CHECK IF RESULT EXISTS IN SESSION STATE ---
if 'result' in st.session_state:
    district_data = st.session_state['result']

    # --- STEP E: Visualizations (Standard Charts - No Plotly Error) ---
    st.markdown("---")
    st.header("Visual Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Enrollment vs. Update Trends")
        st.caption("Scatter Plot: Note how updates (Y-axis) dominate")
        # Native Scatter Chart
        st.scatter_chart(
            district_data,
            x="New_Enrolment_Count",
            y="Update_Count",
            color="Zone",
            size="Update_Count"
        )

    with col2:
        st.subheader("2. Zone Distribution")
        st.caption("Count of districts in each category")
        # Native Bar Chart for Counts
        zone_counts = district_data["Zone"].value_counts()
        st.bar_chart(zone_counts)

    st.markdown("---")
    st.subheader("3. Top 30 High-Load Districts (Updates)")
    st.caption("Districts requiring immediate attention (Sorted by Load)")
    
    # Filter for Top 30 only and Sort
    top_30_data = district_data.sort_values(by="Update_Count", ascending=False).head(30)
    
    # Native Bar Chart
    st.bar_chart(
        top_30_data.set_index("District")["Update_Count"]
    )

    # --- STEP F: Final Data Table & Download ---
    st.markdown("---")
    st.subheader("Final Allocation Report")
    
    zone_filter = st.multiselect("Filter by Zone", district_data["Zone"].unique(), default=district_data["Zone"].unique())
    filtered_final = district_data[district_data["Zone"].isin(zone_filter)]
    
    st.dataframe(filtered_final, use_container_width=True)

    csv = filtered_final.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Final Report (CSV)",
        data=csv,
        file_name="aadhaar_gati_allocation.csv",
        mime="text/csv"
    )
