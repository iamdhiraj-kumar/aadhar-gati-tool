# Aadhaar-Gati Tool 🚀  
### Smart Resource Allocation System for Aadhaar Services

🔗 **Live Web App:**  
https://aadhar-gati-tool-wiyavzfmkof7ekgkws4idh.streamlit.app/

---

## 📌 Overview

**Aadhaar-Gati** is a data-driven decision support system designed to optimize Aadhaar service resource allocation at the district level.  
The project analyzes Aadhaar **enrollment and update trends** to identify operational stress and recommend appropriate deployment of staff and infrastructure.

The tool is developed as part of the **UIDAI Hackathon** with the objective of improving efficiency, transparency, and data-driven planning in Aadhaar operations.

---

## 🎯 Objectives

- Analyze district-wise Aadhaar enrollment and update data  
- Identify service demand patterns across districts  
- Classify districts into operational traffic zones  
- Recommend appropriate resource deployment strategies  
- Provide clear visual insights and downloadable reports  

---

## 🧠 Conceptual Insight

Aadhaar is a **mature digital identity system**.  
While new enrollments are largely finite, **update services (demographic and biometric)** are recurring throughout a citizen’s lifecycle.

Therefore, **update demand is a key indicator of real operational workload**, and planning based only on enrollment data can lead to inefficient resource allocation.

Aadhaar-Gati explicitly models this reality using data-driven analysis.

---

## 🧮 Methodology (Core Innovation)

### Dual-Scale Percentile-Based Classification

Instead of using raw totals, Aadhaar-Gati applies **independent percentile thresholding** to ensure fairness between enrollment and update volumes.

### Steps:
1. Aggregate total enrollment and total updates at district level  
2. Compute **75th percentile** for:
   - Enrollment demand  
   - Update demand  
3. Classify districts as:

- 🔴 **High Traffic Zone**  
  Districts exceeding the 75th percentile in either enrollment or updates  

- 🟢 **Balanced Zone**  
  Districts operating within normal capacity  

- ⚪ **Ghost Zone**  
  Districts below the 25th percentile in both categories  

This approach prevents high update volumes from masking enrollment needs and ensures balanced planning.

---

## 🔄 Data Analysis Pipeline

Raw UIDAI Data
↓
Python Data Analysis (analysis/data_analysis.py)
↓
Final District-wise Output CSV
↓
Aadhaar-Gati Streamlit Application

---

## 📂 Repository Structure

aadhaar-gati-tool/
├── analysis/
│ └── data_analysis.py # Data cleaning, aggregation, percentile logic
├── app.py # Streamlit web application
├── data/
│ └── sample_data.csv # Sample input dataset
├── output/
│ └── aadhaar_gati_final_output.csv
├── visuals/
│ ├── bar_enrollment.png
│ ├── bar_updates.png
│ └── scatter_enroll_update.png
├── requirements.txt
├── uidai_logo.png
└── README.md


---

## 📄 Input Data Format

The application accepts a CSV file with the following columns:

| Column Name | Description |
|------------|------------|
| District | District name |
| Update_Count | Number of Aadhaar updates |
| New_Enrolment_Count | Number of new enrollments |

**Example:**

District,Update_Count,New_Enrolment_Count
Lucknow,5400,2100
Kanpur,4200,1800


---

## 📤 Output

- Interactive district-level data tables  
- Visual insights (bar charts, scatter plots, zone distribution)  
- Downloadable CSV report  
- Final operational recommendations for each district  

---

## ▶ How to Run the Project Locally

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt

2️⃣ Run the application
streamlit run app.py

The application will open automatically in your browser.

🛠 Technologies Used

Python – Data processing and logic

Pandas – Data analysis

Matplotlib / Streamlit Charts – Visualization

Streamlit – Web interface

GitHub – Version control

## 👥 Team

- **Dhiraj Kumar** — Backend development, data analysis, integration  
- **Sakshi kumari** — UI design 
- **Anushree Merothiya** — Data collection and documentation  


**📜 Disclaimer**
This project is developed for educational and hackathon purposes only and  use or access real Aadhaar  data for fair means.
