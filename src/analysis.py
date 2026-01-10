
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from loader import load_all_data

# Setup Output Directory
OUTPUT_DIR = r"c:/FINAL YEAR PROJECTS/UIDAI Hackathon/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def preprocess_data(df, date_col='date'):
    if df.empty:
        return df
    # Convert date to datetime, handle errors
    df[date_col] = pd.to_datetime(df[date_col], format='%d-%m-%Y', errors='coerce')
    # Drop rows with invalid dates if any
    df = df.dropna(subset=[date_col])
    return df

def analyze_enrollment(df):
    if df.empty:
        return
    
    print("Analyzing Enrollment...")
    # 1. Total Enrollment over time
    daily_enrollment = df.groupby('date')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=daily_enrollment)
    plt.title('Daily Aadhaar Enrollments by Age Group')
    plt.ylabel('Count')
    plt.xlabel('Date')
    plt.savefig(os.path.join(OUTPUT_DIR, 'enrollment_time_series.png'))
    plt.close()
    
    # 2. State-wise Enrollment
    state_enrollment = df.groupby('state')[['age_0_5', 'age_5_17', 'age_18_greater']].sum().sum(axis=1).sort_values(ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=state_enrollment.values, y=state_enrollment.index, palette='viridis')
    plt.title('Top 10 States by Total Enrollment')
    plt.xlabel('Total Enrollments')
    plt.savefig(os.path.join(OUTPUT_DIR, 'top_states_enrollment.png'))
    plt.close()

def analyze_updates(bio_df, demo_df):
    print("Analyzing Updates...")
    
    # Biometric vs Demographic Total Volume
    bio_total = 0
    if not bio_df.empty:
        bio_total = bio_df[['bio_age_5_17', 'bio_age_17_']].sum().sum()
    
    demo_total = 0
    if not demo_df.empty:
        demo_total = demo_df[['demo_age_5_17', 'demo_age_17_']].sum().sum()
        
    plt.figure(figsize=(6, 6))
    plt.pie([bio_total, demo_total], labels=['Biometric Updates', 'Demographic Updates'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
    plt.title('Distribution of Update Types')
    plt.savefig(os.path.join(OUTPUT_DIR, 'update_type_distribution.png'))
    plt.close()
    
    # Biometric Age Split
    if not bio_df.empty:
        bio_age_split = bio_df[['bio_age_5_17', 'bio_age_17_']].sum()
        plt.figure(figsize=(6, 6))
        
        # Check if bio_age_17_ exists, handle potential column name mismatch from inspection
        # Previous inspection showed 'bio_age_17_', let's handle if it has a suffix
        
        plt.pie(bio_age_split, labels=bio_age_split.index, autopct='%1.1f%%', startangle=90)
        plt.title('Biometric Updates by Age Group')
        plt.savefig(os.path.join(OUTPUT_DIR, 'biometric_age_split.png'))
        plt.close()

def main():
    bio, demo, enroll = load_all_data()
    
    # Preprocess
    bio = preprocess_data(bio)
    demo = preprocess_data(demo)
    enroll = preprocess_data(enroll)
    
    # Analyze
    analyze_enrollment(enroll)
    analyze_updates(bio, demo)
    
    print(f"Analysis completed. Plots saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
