Aadhaar-Gati Tool 🚀

Smart Resource Allocation System for Aadhaar Services

📌 Overview

Aadhaar-Gati Tool is a data-driven web application designed to help analyze district-wise Aadhaar service data and optimize resource allocation such as staff and mobile units.

This tool enables decision-makers to identify high-traffic, balanced, and low-traffic districts and take informed actions accordingly.

Built as part of the UIDAI Hackathon to improve efficiency, transparency, and data-based planning in Aadhaar operations.

🎯 Objectives

Analyze Aadhaar update and enrolment data

Identify service demand across districts

Classify districts into traffic zones

Recommend appropriate resource deployment

Provide clear visual and downloadable reports

🛠 Technologies Used

Python — Data processing and logic

Streamlit — Web interface

Pandas — Data analysis

Matplotlib / Streamlit Charts — Visualization

GitHub — Version control

📂 Project Structure
aadhaar-gati-tool/
│
├── app.py                # Main Streamlit application
├── requirements.txt      # Required Python libraries
├── uidai_logo.png        # UIDAI logo for UI
├── README.md             # Project documentation
└── sample_data.csv       # Sample input dataset

📄 Input Data Format

Upload a CSV file with the following columns:

Column Name	Description
District	District name
Update_Count	Number of Aadhaar updates
New_Enrolment_Count	Number of new enrolments

Example:

District	Update_Count	New_Enrolment_Count
Lucknow	5400	2100
Kanpur	4200	1800

▶ How to Run the Project
1️⃣ Install dependencies
pip install -r requirements.txt
2️⃣ Run the application
streamlit run app.py
The tool will automatically open in your browser.

🧠 Logic Used

Aggregates data district-wise

Applies threshold-based classification

Assigns zones:

High Traffic Zone

Balanced Zone

Ghost Zone

Generates recommendations:

Deploy Permanent Staff

Deploy Mobile Aadhaar Vans

No Action Required

📤 Output

Interactive data tables

Visual charts

Downloadable CSV report

Final recommendations for each district

## 👥 Team

- **Dhiraj Kumar** — Backend development, data analysis, integration  
- **Sakshi kumari** — UI design 
- **Anushree Merothiya** — Data collection and documentation  


📜 Disclaimer
This project is developed for educational and hackathon purposes only and  use or access real Aadhaar  data for fair means.
