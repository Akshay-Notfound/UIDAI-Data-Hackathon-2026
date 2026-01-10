import pandas as pd
import glob
import os

# Define base paths
BASE_DIR = r"c:/FINAL YEAR PROJECTS/UIDAI Hackathon/UIDAI Data Hackathon 2026"
BIO_DIR = os.path.join(BASE_DIR, "Aadhaar Biometric Update dataset")
DEMO_DIR = os.path.join(BASE_DIR, "Aadhaar Demographic Update Dataset")
ENROLL_DIR = os.path.join(BASE_DIR, "Aadhaar Enrollment Dataset")

def load_and_aggregate(directory, pattern, category_name):
    print(f"Loading {category_name} data from {directory}...")
    # Recursive search for csv files
    files = glob.glob(os.path.join(directory, "**", pattern), recursive=True)
    
    if not files:
        print(f"Warning: No files found for {category_name} with pattern {pattern}")
        return pd.DataFrame()
        
    df_list = []
    for file in files:
        try:
            df = pd.read_csv(file)
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            
    if not df_list:
        return pd.DataFrame()
        
    final_df = pd.concat(df_list, ignore_index=True)
    print(f"Loaded {len(final_df)} rows for {category_name}.")
    return final_df

def load_all_data():
    # Load Biometric
    bio_df = load_and_aggregate(BIO_DIR, "*.csv", "Biometric Updates")
    
    # Load Demographic
    demo_df = load_and_aggregate(DEMO_DIR, "*.csv", "Demographic Updates")
    
    # Load Enrollment
    enroll_df = load_and_aggregate(ENROLL_DIR, "*.csv", "Enrollment")
    
    return bio_df, demo_df, enroll_df

if __name__ == "__main__":
    bio, demo, enroll = load_all_data()
    
    print("\n--- Data Summary ---")
    if not bio.empty:
        print("Biometric Columns:", bio.columns.tolist())
        print(bio.head())
    if not demo.empty:
        print("Demographic Columns:", demo.columns.tolist())
        print(demo.head())
    if not enroll.empty:
        print("Enrollment Columns:", enroll.columns.tolist())
        print(enroll.head())
