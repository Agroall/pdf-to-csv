import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO


# ---------- App Title ----------
st.set_page_config(page_title="PDF to CSV Extractor", layout="centered")
st.title("📄 PDF Table Extractor to CSV")
st.markdown("Upload bank statement PDFs to extract **metadata** and **transactions** as tables.")


# ---------- Function ----------
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

    # Handle metadata
    if metadata_table:
        df_metadata = pd.concat(metadata_table).reset_index(drop=True)
    else:
        df_metadata = pd.DataFrame(columns=["Field", "Value"])

    # Handle transactions
    if transaction_tables:
        df_transactions = pd.concat(transaction_tables)
        df_transactions.columns = df_transactions.iloc[0, :].astype(str)
        df_transactions = df_transactions.iloc[1:, :].reset_index(drop=True)
        # df_transactions.columns = [col.strip() for col in df_transactions.columns]
        # df_transactions = df_transactions.astype(str)
    else:
        df_transactions = pd.DataFrame()

    index_list = []

    for index, _ in df_transactions.iterrows():
        if df_transactions.iloc[index, :].isna().sum() >= 2:
            index_list.append(index)
            df_transactions.iloc[index-1, -1] = str(df_transactions.iloc[index-1, -1]) + str(df_transactions.iloc[index, -1])

    df_transactions.drop(index=index_list, inplace=True)
    df_transactions = df_transactions.reset_index(drop=True)


    return df_metadata, df_transactions, index_list



# ---------- Uploader ----------
uploaded_files = st.file_uploader("📎 Upload your PDF(s)", type="pdf", accept_multiple_files=True)


# ---------- Process Each File ----------
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.divider()
        st.subheader(f"📘 File: `{uploaded_file.name}`")
        with st.spinner("Processing file..."):
            df_meta, df_txn, idx = pdf_to_csv(uploaded_file)

        # Layout
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🧾 Metadata")
            if not df_meta.empty:
                st.dataframe(df_meta, use_container_width=True)
                st.download_button(
                    label="⬇️ Download Metadata CSV",
                    data=df_meta.to_csv(index=False).encode("utf-8"),
                    file_name=f"{uploaded_file.name}_metadata.csv",
                    mime="text/csv"
                )
            else:
                st.info("No metadata table found.")

        with col2:
            st.markdown("### 📑 Transactions")
            if not df_txn.empty:
                st.dataframe(df_txn, use_container_width=True)
                st.download_button(
                    label="⬇️ Download Transactions CSV",
                    data=df_txn.to_csv(index=False).encode("utf-8"),
                    file_name=f"{uploaded_file.name}_transactions.csv",
                    mime="text/csv"
                )
            else:
                st.info("No transaction table found.")


        st.success("✅ File processed successfully!")
        st.write(idx)

