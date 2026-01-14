import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Aadhaar-Gati Tool", layout="wide")

logo = Image.open("uidai_logo.png")
st.image(logo, width=180)

st.title("Aadhaar-Gati: Smart Resource Allocation Tool")
st.write("Data-driven optimization of Aadhaar services at district level")

uploaded_file = st.file_uploader("Upload Aadhaar District Data (CSV or Excel)", type=["csv","xlsx","xls")]

def aggregate_data(df):
    return df.groupby("District").agg({
        "Update_Count": "sum",
        "New_Enrolment_Count": "sum"
    }).reset_index()

def classify(row):
    if row["Update_Count"] > 4000:
        return "High Traffic Zone"
    elif row["New_Enrolment_Count"] < 500:
        return "Ghost Zone"
    else:
        return "Balanced Zone"

def recommend(zone):
    if zone == "High Traffic Zone":
        return "Deploy Permanent Staff"
    elif zone == "Ghost Zone":
        return "Deploy Mobile Aadhaar Vans"
    else:
        return "No Action Required"

if uploaded_file and st.button("Run Analysis"):
    if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
else:
    df=pd.read_excel(uploaded file)
    agg = aggregate_data(df)
    agg["Zone"] = agg.apply(classify, axis=1)
    agg["Recommended_Action"] = agg["Zone"].apply(recommend)
    st.session_state["result"] = agg
    st.success("Analysis Completed")

if "result" in st.session_state:
    result = st.session_state["result"]

    st.subheader("Filters")
    zones = result["Zone"].unique().tolist()
    selected_zones = st.multiselect("Select Zone", zones, default=zones)

    filtered = result[result["Zone"].isin(selected_zones)]

    st.subheader("Final Output")
    st.dataframe(filtered, use_container_width=True)

    st.subheader("Traffic Comparison Chart")
    st.bar_chart(filtered.set_index("District")[["Update_Count", "New_Enrolment_Count"]])

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Allocation Report",
        data=csv,
        file_name="aadhaar_gati_report.csv",
        mime="text/csv"
    )

