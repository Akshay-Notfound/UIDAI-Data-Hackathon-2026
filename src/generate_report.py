
from fpdf import FPDF
import os
import glob

# Setup paths
BASE_DIR = r"c:/FINAL YEAR PROJECTS/UIDAI Hackathon"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
REPORT_PATH = os.path.join(OUTPUT_DIR, "UIDAI_Hackathon_Submission.pdf")

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

    def add_image(self, image_path, title=""):
        if os.path.exists(image_path):
            self.ln(5)
            if title:
                self.set_font('Arial', 'I', 10)
                self.cell(0, 5, title, 0, 1, 'C')
            # Adjust image width to fit page
            self.image(image_path, x=10, w=190) 
            self.ln(5)
        else:
            self.set_text_color(255, 0, 0)
            self.cell(0, 10, f"Image not found: {os.path.basename(image_path)}", 0, 1)
            self.set_text_color(0, 0, 0)

def create_pdf():
    pdf = PDF()
    pdf.add_page()

    # 1. Problem Statement and Approach
    pdf.chapter_title("1. Problem Statement and Approach")
    pdf.chapter_body(
        "Problem Statement: Unlocking Societal Trends in Aadhaar Enrolment and Updates.\n\n"
        "Approach: This analysis leverages aggregated daily Aadhaar transaction data to identify "
        "enrollment saturation, demographic update patterns, and regional disparities. "
        "We utilize Python (Pandas, Matplotlib) to process large-scale CSV datasets, aggregate them "
        "by geography and age groups, and visualize trends to extract actionable insights."
    )

    # 2. Datasets Used
    pdf.chapter_title("2. Datasets Used")
    pdf.chapter_body(
        "The analysis uses three primary datasets provided by UIDAI:\n"
        "- Aadhaar Enrolment Dataset: Daily new enrollments (0-5, 5-17, 18+).\n"
        "- Aadhaar Biometric Update Dataset: Daily biometric updates (5-17, 17+).\n"
        "- Aadhaar Demographic Update Dataset: Daily demographic updates (5-17, 17+).\n\n"
        "Columns used include: Date, State, District, Pincode, and aggregated counts for each age bucket."
    )

    # 3. Methodology
    pdf.chapter_title("3. Methodology")
    pdf.chapter_body(
        "1. Data Aggregation: Multiple CSV files distributed by batch/region were programmatically "
        "loaded and concatenated into unified DataFrames for Enrollment, Biometric, and Demographic activities.\n"
        "2. Data Cleaning: Date fields were standardized to datetime objects. Missing values were handled "
        "by exclusion to ensure data integrity.\n"
        "3. Exploratory Analysis: We calculated total volumes per state and tracked daily trends "
        "to identify peak activity periods.\n"
        "4. Comparative Analysis: We compared the ratio of new enrollments vs. updates to assess "
        "saturation levels across different age groups."
    )

    # 4. Data Analysis and Visualisation
    pdf.chapter_title("4. Data Analysis and Visualisation")
    pdf.chapter_body(
        "Key Findings:\n"
        "- Enrollment Trends: Visual analysis of daily enrollments highlights specific campaigns or seasonal peaks.\n"
        "- Geographic Distribution: Certain states show significantly higher activity, correlating with population density.\n"
        "- Update Preferences: The split between biometric and demographic updates reveals user needs."
    )
    
    # Add Plots
    pdf.add_image(os.path.join(OUTPUT_DIR, 'enrollment_time_series.png'), "Fig 1: Daily Enrollment Trends")
    pdf.add_image(os.path.join(OUTPUT_DIR, 'top_states_enrollment.png'), "Fig 2: Top States by Enrollment Volume")
    pdf.add_image(os.path.join(OUTPUT_DIR, 'update_type_distribution.png'), "Fig 3: Distribution of Update Types")
    pdf.add_image(os.path.join(OUTPUT_DIR, 'biometric_age_split.png'), "Fig 4: Biometric Updates by Age Group")

    # 5. Code Reference
    pdf.add_page()
    pdf.chapter_title("5. Source Code")
    pdf.chapter_body("The analysis was performed using the following Python scripts.")
    
    # Embed Analysis Code
    pdf.set_font("Courier", size=8)
    try:
        with open(os.path.join(BASE_DIR, "src", "analysis.py"), "r") as f:
            code_content = f.read()
            # Basic sanitization for PDF text
            code_content = code_content.replace("\t", "    ")
            pdf.multi_cell(0, 4, code_content)
    except Exception as e:
        pdf.chapter_body(f"Error reading code file: {str(e)}")

    pdf.output(REPORT_PATH)
    print(f"PDF Report generated successfully: {REPORT_PATH}")

if __name__ == "__main__":
    create_pdf()
