import streamlit as st
import pdfplumber
import pandas as pd


def pdf_to_csv(uploaded_file):
    metadata_table = []
    transaction_tables = []

    with pdfplumber.open(uploaded_file) as pdf:  
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue
                if all(len(row) == 2 for row in table):
                    metadata_table.append(pd.DataFrame(table, columns=["Field", "Value"]))
                else:
                    df = pd.DataFrame(table)
                    transaction_tables.append(df)

    df_metadata = pd.concat(metadata_table).reset_index(drop=True)
    df_transactions = pd.concat(transaction_tables)

    df_transactions.columns = df_transactions.iloc[0, :].astype(str)
    df_transactions = df_transactions.iloc[1:, :].reset_index(drop=True)
    df_transactions.columns = [col.strip() for col in df_transactions.columns]  # Optional cleanup
    df_transactions = df_transactions.astype(str)


    return df_metadata, df_transactions


uploaded_files = st.file_uploader("Upload your PDF(s)", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.subheader(f"{uploaded_file.name}")
        df_meta, df_txn = pdf_to_csv(uploaded_file)

        st.write("**Metadata**")
        st.dataframe(df_meta.astype(str))

        st.write("**Transactions**")
        st.dataframe(df_txn.astype(str))



