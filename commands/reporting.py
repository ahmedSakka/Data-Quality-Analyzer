import os
import json
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
import pandas as pd

def save_json(report: dict, output_dir: str = "reports") -> str:
    os.makedirs(output_dir, exist_ok= True)
    file_path = os.path.join(output_dir, f"report_{timestamp()}.json")
    with open(file_path, "w") as f:
        json.dump(report, f, indent=4)
    return file_path

def save_markdown(report: dict, output_dir: str = "reports") -> str:
    os.makedirs(output_dir, exist_ok= True)
    file_path = os.path.join(output_dir, f"report_{timestamp()}.md")
    with open(file_path, "w") as f:
        f.write(dict_to_markdown(report))
    return file_path

def dict_to_markdown(d: dict, indent: int = 0) -> str:
    md = ""
    prefix = "#" * (indent + 2)
    for key, value in d.items():
        md += f"\n{prefix} {key.replace('_', ' ').title()}\n"
        if isinstance(value, dict):
            for sub_key, sub_val in value.items():
                md += f"- **{sub_key}**: {sub_val}\n"
        elif isinstance(value, list):
            if value:
                for item in value:
                    md += f"- {item}\n"
            else:
                md += "- No items found.\n"
        else:
            md += f"- {value}\n"
    return md

def save_pdf(report: dict, df, output_dir: str = "reports") -> str:
    os.makedirs(output_dir, exist_ok= True)
    timestamp_str = timestamp()
    file_path = os.path.join(output_dir, f"report_{timestamp_str}.pdf")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"{df} data quality report", ln= True, align='C')
    pdf.ln(10)

    # Key metrics
    for section, content in report.items():
        pdf.set_font("Arial", 'B', size=14)
        pdf.cell(0, 10, section.replace('_', ' ').title(), ln=True)
        pdf.set_font("Arial", size=12)
        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, dict):
                    pdf.multi_cell(0, 10, f"{key.replace('_', ' ').title()}:\n{json.dumps(value, indent=2)}")
                else:
                    pdf.cell(0, 10, f"{key.replace('_', ' ').title()}: {value}", ln=True)
        else:
            pdf.cell(0, 10, str(content), ln=True)
        pdf.ln(5)
    
    # Visulaizations
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    # Handling columns with numeric-looking strings
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col].str.extract(r'([-+]?[0-9]*\.?[0-9]+)')[0], errors= 'coerce')
            except Exception as e:
                continue
    
    numeric_cols = df.select_dtypes(include='number').columns

    for col in numeric_cols:
        # Skip if there is no variability in the column
        if df[col].dropna().nunique() < 2:
            continue
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(x=df[col], ax=ax, color='skyblue')
        plt.title(f"Boxplot of {col}")
        img_path = os.path.join(output_dir, f"{col}_boxplot_{timestamp_str}.png")
        plt.savefig(img_path, bbox_inches='tight')
        plt.close(fig)

        pdf.add_page()
        pdf.set_font("Arial", "B", size=14)
        pdf.cell(0, 10, f"Boxplot of {col}", ln=True)
        pdf.image(img_path, x=10, y=None, w=180)
        os.remove(img_path)
    
    pdf.output(file_path)
    return file_path


def timestamp():
    return dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")