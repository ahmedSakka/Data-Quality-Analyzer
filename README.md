# 🧪 Data Quality Analyzer

The **Data Quality Analyzer** is a command-line Python tool built with [Typer](https://typer.tiangolo.com/) that performs automated quality checks on CSV datasets. It helps analysts and data engineers identify common data issues such as missing values, duplicates, inconsistent categories, and outliers. This tool can generate detailed reports in both JSON and Markdown formats.

---

## ✨ Features

- Detects:
  - Missing values
  - Duplicate rows
  - Constant columns
  - Unique value counts
  - Data type summaries
  - Numeric range stats (min, max, mean, std)
  - Categorical inconsistencies
  - Outliers using IQR method
- Supports:
  - Custom column analysis
  - Concise summary output
  - JSON and Markdown report formats
  - CLI usage with helpful options

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Data-Quality-Analyzer.git
   cd Data-Quality-Analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the CLI:
   ```bash
   python main.py analyze <path_to_csv>
   ```

---

## 🚀 Usage

### Basic

```bash
python main.py analyze data.csv
```

### Save Report

```bash
python main.py analyze data.csv --save --format markdown
```

### Summary Only

```bash
python main.py analyze data.csv --summary
```

### Specific Columns

```bash
python main.py analyze data.csv --columns age income gender
```
---

## 🛠️ Built With

- [Python 3.9+](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Typer](https://github.com/tiangolo/typer)

---

## 👤 Author

**Ahmed Al Sakka**   
📧 [ahmedsakka101@gmail.com](mailto:ahmedsakka101@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/ahmed-alsakka-analyst/) • [GitHub](https://github.com/ahmedSakka)