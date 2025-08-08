# CSV Data Cleaner

🧼 A simple Streamlit app to clean CSV datasets by removing duplicates, filling missing values, normalizing text, and removing outliers.

---

## Features

- Upload your CSV file via the web interface  
- Removes duplicate rows (exact or based on key columns)  
- Fills missing numeric values with column means  
- Fills missing categorical values with mode (most frequent value)  
- Normalizes text columns by trimming whitespace and converting to lowercase  
- Removes outliers based on IQR method  
- Download cleaned CSV file  

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/csv-data-cleaner.git
cd csv-data-cleaner
