# === UIDAI Hackathon 2026 - Colab All-in-One Script ===
# Instructions:
# 1. Upload your "UIDAI Data Hackathon 2026" folder to your Google Drive (e.g., in the root directory).
# 2. Create a New Notebook in Google Colab.
# 3. Copy and Paste ALL this code into the first cell.
# 4. Run the cell. Follow the prompts to authorize Google Drive access.

# Part 0: Setup Environment
import sys
import os
import subprocess

# Install fpdf if not present
try:
    import fpdf
except ImportError:
    print("Installing fpdf...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf"])

# Mount Google Drive
from google.colab import drive
if not os.path.exists('/content/drive'):
    print("Mounting Google Drive...")
    drive.mount('/content/drive')

# === CONFIGURATION ===
# UPDATE THIS PATH if you uploaded the data to a different folder in Drive
# Default assumes the folder "UIDAI Data Hackathon 2026" is in "My Drive"
BASE_DRIVE_PATH = "/content/drive/MyDrive/UIDAI Data Hackathon 2026" 

# Output directory for plots and PDF
OUTPUT_DIR = "/content/drive/MyDrive/UIDAI_Hackathon_Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define Data Paths based on your structure
BIO_DIR = os.path.join(BASE_DRIVE_PATH, "Aadhaar Biometric Update dataset")
DEMO_DIR = os.path.join(BASE_DRIVE_PATH, "Aadhaar Demographic Update Dataset")
ENROLL_DIR = os.path.join(BASE_DRIVE_PATH, "Aadhaar Enrollment Dataset")

# ==========================================
# Part 1: Data Loader
# ==========================================
import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

def load_and_aggregate(directory, pattern, category_name):
    print(f"Loading {category_name} data from {directory}...")
    files = glob.glob(os.path.join(directory, "**", pattern), recursive=True)
    
    if not files:
        print(f"WARNING: No files found for {category_name} in {directory}")
        print("Please check your BASE_DRIVE_PATH.")
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
    print(f"--> Loaded {len(final_df)} rows for {category_name}.")
    return final_df

def load_all_data():
    bio_df = load_and_aggregate(BIO_DIR, "*.csv", "Biometric Updates")
    demo_df = load_and_aggregate(DEMO_DIR, "*.csv", "Demographic Updates")
    enroll_df = load_and_aggregate(ENROLL_DIR, "*.csv", "Enrollment")
    return bio_df, demo_df, enroll_df

# ==========================================
# Part 2: Analysis & Visualization
# ==========================================
def preprocess_data(df, date_col='date'):
    if df.empty: return df
    df[date_col] = pd.to_datetime(df[date_col], format='%d-%m-%Y', errors='coerce')
    return df.dropna(subset=[date_col])

def analyze_enrollment(df):
    if df.empty: return
    print("Generating Enrollment Plots...")
    
    # Time Series
    daily_enrollment = df.groupby('date')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=daily_enrollment)
    plt.title('Daily Aadhaar Enrollments by Age Group')
    plt.ylabel('Count'); plt.xlabel('Date')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'enrollment_time_series.png'))
    plt.close()
    
    # Top States
    state_totals = df.groupby('state')[['age_0_5', 'age_5_17', 'age_18_greater']].sum().sum(axis=1)
    top_10 = state_totals.sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=top_10.values, y=top_10.index, palette='viridis')
    plt.title('Top 10 States by Total Enrollment')
    plt.xlabel('Total Enrollments')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'top_states_enrollment.png'))
    plt.close()

def analyze_updates(bio_df, demo_df):
    print("Generating Update Plots...")
    bio_total = bio_df[['bio_age_5_17', 'bio_age_17_']].sum().sum() if not bio_df.empty else 0
    demo_total = demo_df[['demo_age_5_17', 'demo_age_17_']].sum().sum() if not demo_df.empty else 0
    
    if bio_total + demo_total > 0:
        plt.figure(figsize=(6, 6))
        plt.pie([bio_total, demo_total], labels=['Biometric', 'Demographic'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
        plt.title('Distribution of Update Types')
        plt.savefig(os.path.join(OUTPUT_DIR, 'update_type_distribution.png'))
        plt.close()
    
    if not bio_df.empty:
        # Check col names
        cols = [c for c in ['bio_age_5_17', 'bio_age_17_', 'bio_age_17+'] if c in bio_df.columns]
        if cols:
            bio_age = bio_df[cols].sum()
            plt.figure(figsize=(6, 6))
            plt.pie(bio_age, labels=bio_age.index, autopct='%1.1f%%', startangle=90)
            plt.title('Biometric Updates: Age Split')
            plt.savefig(os.path.join(OUTPUT_DIR, 'biometric_age_split.png'))
            plt.close()

# ==========================================
# Part 3: PDF Report Generation
# ==========================================
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'UIDAI Data Hackathon 2026 - Submission', 0, 1, 'C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()
    def add_image_safe(self, img_path, title=""):
        if os.path.exists(img_path):
            self.ln(5)
            if title:
                self.set_font('Arial', 'I', 10)
                self.cell(0, 5, title, 0, 1, 'C')
            self.image(img_path, x=10, w=190)
            self.ln(5)
        else:
            self.set_text_color(255,0,0)
            self.cell(0,10, f"Image missing: {os.path.basename(img_path)}", 0, 1)
            self.set_text_color(0,0,0)

def generate_pdf():
    print("Generating PDF Report...")
    pdf = PDF()
    pdf.add_page()
    
    pdf.chapter_title("1. Problem Statement and Approach")
    pdf.chapter_body(
        "Problem Statement: Unlocking Societal Trends in Aadhaar Enrolment and Updates.\n\n"
        "Approach: This analysis processes aggregated daily transaction data to identify "
        "enrollment saturation, update patterns, and regional trends using Python."
    )
    
    pdf.chapter_title("2. Key Findings & Visualizations")
    pdf.chapter_body("Below are the key trends identified from the dataset:")
    
    pdf.add_image_safe(os.path.join(OUTPUT_DIR, 'enrollment_time_series.png'), "Fig 1: Enrollment Trends")
    pdf.add_image_safe(os.path.join(OUTPUT_DIR, 'top_states_enrollment.png'), "Fig 2: Top States")
    pdf.add_image_safe(os.path.join(OUTPUT_DIR, 'update_type_distribution.png'), "Fig 3: Update Types")
    
    report_path = os.path.join(OUTPUT_DIR, "UIDAI_Hackathon_Submission_Colab.pdf")
    pdf.output(report_path)
    print(f"PDF Saved to: {report_path}")

# ==========================================
# Main Execution Flow
# ==========================================
if __name__ == "__main__":
    print("Starting Analysis Pipeline...")
    
    # Load
    bio, demo, enroll = load_all_data()
    
    # Process
    if not (bio.empty and demo.empty and enroll.empty):
        bio = preprocess_data(bio)
        demo = preprocess_data(demo)
        enroll = preprocess_data(enroll)
        
        # Analyze
        analyze_enrollment(enroll)
        analyze_updates(bio, demo)
        
        # Report
        generate_pdf()
        print("\nSUCCESS! Check the 'UIDAI_Hackathon_Output' folder in your Google Drive.")
    else:
        print("ERROR: No data loaded. Please verify your folder path in Drive.")
