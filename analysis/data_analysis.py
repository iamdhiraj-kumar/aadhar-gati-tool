import pandas as pd
import numpy as np
final_output = pd.read_csv("final_output.csv")

top_enroll = final_output.sort_values("total_enroll", ascending=False).head(10)
print(top_enroll)

# Load files
enroll = pd.read_csv("enrollment.csv")
demo = pd.read_csv("demographic_update.csv")
bio = pd.read_csv("biometric_update.csv")

# Normalize column names
for df in [enroll, demo, bio]:
    df.columns = df.columns.str.lower().str.strip()

print("\nEnrollment columns:", list(enroll.columns))
print("\nDemographic columns:", list(demo.columns))
print("\nBiometric columns:", list(bio.columns))

# Find age columns automatically
def find_age_cols(df):
    return [c for c in df.columns if "age" in c]

enroll_age_cols = find_age_cols(enroll)
demo_age_cols = find_age_cols(demo)
bio_age_cols = find_age_cols(bio)

print("\nUsing age columns:")
print("Enroll:", enroll_age_cols)
print("Demo:", demo_age_cols)
print("Bio:", bio_age_cols)

# Convert to numeric safely
for c in enroll_age_cols:
    enroll[c] = pd.to_numeric(enroll[c], errors="coerce").fillna(0)

for c in demo_age_cols:
    demo[c] = pd.to_numeric(demo[c], errors="coerce").fillna(0)

for c in bio_age_cols:
    bio[c] = pd.to_numeric(bio[c], errors="coerce").fillna(0)

# Create totals
enroll["total_enroll"] = enroll[enroll_age_cols].sum(axis=1)
demo["total_demo"] = demo[demo_age_cols].sum(axis=1)
bio["total_bio"] = bio[bio_age_cols].sum(axis=1)

# Aggregate per district
enroll_g = enroll.groupby("district")["total_enroll"].sum().reset_index()
demo_g = demo.groupby("district")["total_demo"].sum().reset_index()
bio_g = bio.groupby("district")["total_bio"].sum().reset_index()

# Merge
df = enroll_g.merge(demo_g, on="district", how="outer").merge(bio_g, on="district", how="outer")
df = df.fillna(0)

# Total update = demo + bio
df["total_update"] = df["total_demo"] + df["total_bio"]

# Thresholds
high_enroll = df["total_enroll"].quantile(0.75)
high_update = df["total_update"].quantile(0.75)

# Zone logic
def assign_zone(r):
    if r["total_enroll"] >= high_enroll and r["total_update"] >= high_update:
        return "High Traffic Zone"
    else:
        return "Balanced Zone"

df["zone"] = df.apply(assign_zone, axis=1)

# Save output
df.to_csv("final_output.csv", index=False)

print("\nSaved final_output.csv")
print(df.head())

import matplotlib.pyplot as plt

# Bar chart: Top 10 districts by enrollment
top_enroll = final_output.sort_values("total_enroll", ascending=False).head(10)
plt.figure(figsize=(10,6))
plt.bar(top_enroll["district"], top_enroll["total_enroll"])
plt.xticks(rotation=45, ha="right")
plt.title("Top Districts by Aadhaar Enrollment")
plt.tight_layout()
plt.savefig("bar_enrollment.png")
plt.close()

# Bar chart: Top 10 districts by updates
top_update = final_output.sort_values("total_update", ascending=False).head(10)
plt.figure(figsize=(10,6))
plt.bar(top_update["district"], top_update["total_update"])
plt.xticks(rotation=45, ha="right")
plt.title("Top Districts by Aadhaar Updates")
plt.tight_layout()
plt.savefig("bar_updates.png")
plt.close()

# Scatter plot: Enrollment vs Updates
plt.figure(figsize=(8,6))
plt.scatter(final_output["total_enroll"], final_output["total_update"])
plt.xlabel("Total Enrollment")
plt.ylabel("Total Updates")
plt.title("Enrollment vs Updates")
plt.tight_layout()
plt.savefig("scatter_enroll_update.png")
plt.close()

