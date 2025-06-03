import streamlit as st
import pdfplumber
import pandas as pd

def pdf_to_csv(pdf_file_path):
    metadata_table = []
    transaction_tables = []

    with pdfplumber.open(pdf_file_path) as pdf:
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

        
    df_metadata = pd.concat(metadata_table).drop_duplicates().reset_index(drop=True)
    df_transactions = pd.concat(transaction_tables)

    df_transactions.columns = df_transactions.iloc[0, :]
    df_transactions = df_transactions.iloc[1:, :]
    df_transactions = df_transactions.reset_index()

    return df_metadata, df_transactions