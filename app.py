import streamlit as st
import pandas as pd
from cleaner import clean_data  # Make sure this accepts parameters as before
from io import BytesIO

st.set_page_config(page_title="CSV Data Cleaner", layout="wide")

st.title("🧼 CSV Data Cleaner")

uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("🔍 Original Data Preview")
        st.dataframe(df.head())

        
        st.sidebar.header("Cleaning Options")

        all_cols = df.columns.tolist()
        selected_cols = st.sidebar.multiselect("Select columns to clean", all_cols, default=all_cols)

        numeric_fill = st.sidebar.selectbox(
            "Fill missing numeric values with",
            ["mean", "median", "drop"],
            index=0
        )

        cat_fill = st.sidebar.selectbox(
            "Fill missing categorical values with",
            ["mode", "constant", "drop"],
            index=0
        )
        cat_constant = None
        if cat_fill == "constant":
            cat_constant = st.sidebar.text_input("Constant value for categorical missing", "unknown")

        dup_option = st.sidebar.selectbox(
            "Remove duplicates by",
            ["full row", "specific columns", "none"],
            index=0
        )
        dup_cols = []
        if dup_option == "specific columns":
            dup_cols = st.sidebar.multiselect("Columns for duplicate detection", all_cols)

        remove_outliers = st.sidebar.checkbox("Remove outliers (IQR method)", value=False)

        
        if st.sidebar.button("Clean Data"):
            cleaned_df = clean_data(
                df,
                selected_columns=selected_cols,
                numeric_fill_strategy=numeric_fill,
                categorical_fill_strategy=cat_fill,
                cat_fill_constant=cat_constant,
                remove_outliers=remove_outliers,
                duplicate_removal=dup_option,
                duplicate_columns=dup_cols,
            )

            st.subheader("✅ Cleaned Data Preview")
            st.dataframe(cleaned_df.head())

            def convert_df_to_csv(df):
                output = BytesIO()
                df.to_csv(output, index=False)
                return output.getvalue()

            st.download_button(
                label="📥 Download Cleaned CSV",
                data=convert_df_to_csv(cleaned_df),
                file_name="cleaned_data.csv",
                mime='text/csv',
            )

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")
