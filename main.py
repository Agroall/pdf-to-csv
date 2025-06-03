# import streamlit as st
# import pdfplumber
# import pandas as pd


# def pdf_to_csv(uploaded_file):
#     metadata_table = []
#     transaction_tables = []

#     with pdfplumber.open(uploaded_file) as pdf:  
#         for page in pdf.pages:
#             tables = page.extract_tables()
#             for table in tables:
#                 if not table:
#                     continue
#                 if all(len(row) == 2 for row in table):
#                     metadata_table.append(pd.DataFrame(table, columns=["Field", "Value"]))
#                 else:
#                     df = pd.DataFrame(table)
#                     transaction_tables.append(df)

#     df_metadata = pd.concat(metadata_table).reset_index(drop=True)
#     df_transactions = pd.concat(transaction_tables)

#     df_transactions.columns = df_transactions.iloc[0, :].astype(str)
#     df_transactions = df_transactions.iloc[1:, :].reset_index(drop=True)
#     df_transactions.columns = [col.strip() for col in df_transactions.columns]  # Optional cleanup
#     df_transactions = df_transactions.astype(str)


#     return df_metadata, df_transactions


# uploaded_files = st.file_uploader("Upload your PDF(s)", type="pdf", accept_multiple_files=True)

# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         st.subheader(f"{uploaded_file.name}")
#         df_meta, df_txn = pdf_to_csv(uploaded_file)

#         st.write("**Metadata**")
#         st.dataframe(df_meta.astype(str))

#         st.write("**Transactions**")
#         st.dataframe(df_txn.astype(str))


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

    df_metadata = pd.concat(metadata_table).reset_index(drop=True)
    df_transactions = pd.concat(transaction_tables)

    df_transactions.columns = df_transactions.iloc[0, :].astype(str)
    df_transactions = df_transactions.iloc[1:, :].reset_index(drop=True)
    df_transactions.columns = [col.strip() for col in df_transactions.columns]
    df_transactions = df_transactions.astype(str)

    return df_metadata, df_transactions


# ---------- Uploader ----------
uploaded_files = st.file_uploader("📎 Upload your PDF(s)", type="pdf", accept_multiple_files=True)


# ---------- Process Each File ----------
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.divider()
        st.subheader(f"📘 File: `{uploaded_file.name}`")
        with st.spinner("Processing file..."):
            df_meta, df_txn = pdf_to_csv(uploaded_file)

        # Layout
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🧾 Metadata")
            st.dataframe(df_meta, use_container_width=True)

            # Download Metadata
            meta_csv = df_meta.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Metadata CSV",
                data=meta_csv,
                file_name=f"{uploaded_file.name}_metadata.csv",
                mime="text/csv"
            )

        with col2:
            st.markdown("### 📑 Transactions")
            st.dataframe(df_txn, use_container_width=True)

            # Download Transactions
            txn_csv = df_txn.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Transactions CSV",
                data=txn_csv,
                file_name=f"{uploaded_file.name}_transactions.csv",
                mime="text/csv"
            )

        st.success("✅ File processed successfully!")

