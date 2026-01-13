import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Aadhaar-Gati Tool", layout="wide")

logo = Image.open("uidai_logo.png")
st.image(logo, width=180)

st.title("Aadhaar-Gati: Smart Resource Allocation Tool")
st.write("Data-driven optimization of Aadhaar services at district level")

uploaded_file = st.file_uploader("Upload Aadhaar District Data (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview of Uploaded Data")
    st.dataframe(df)

    if st.button("Run Analysis"):
        # Aggregate
        district_data = df.groupby("District").agg({
            "Update_Count": "sum",
            "New_Enrolment_Count": "sum"
        }).reset_index()

        # Classify zones
        def classify(row):
            if row["Update_Count"] > 4000:
                return "High Traffic Zone"
            elif row["New_Enrolment_Count"] < 500:
                return "Ghost Zone"
            else:
                return "Balanced Zone"

        district_data["Zone"] = district_data.apply(classify, axis=1)

        # Recommend actions
        def recommend(zone):
            if zone == "High Traffic Zone":
                return "Deploy Permanent Staff"
            elif zone == "Ghost Zone":
                return "Deploy Mobile Aadhaar Vans"
            else:
                return "No Action Required"

        district_data["Recommended_Action"] = district_data["Zone"].apply(recommend)

        st.success("Analysis Completed")

        # Filters
        st.subheader("Filters")
        zone_filter = st.multiselect("Select Zone", district_data["Zone"].unique(), default=district_data["Zone"].unique())
        filtered = district_data[district_data["Zone"].isin(zone_filter)]

        st.subheader("Final Output")
        st.dataframe(filtered)

        # Chart
        st.subheader("Traffic Comparison Chart")
        st.bar_chart(filtered.set_index("District")[["Update_Count", "New_Enrolment_Count"]])

        # Download
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Allocation Report",
            data=csv,
            file_name="aadhaar_gati_report.csv",
            mime="text/csv"
        )
