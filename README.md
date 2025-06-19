# 📄 PDF to CSV Bank Statement Extractor

A Streamlit web application that extracts **account metadata** and **transaction history** tables from PDF bank statements and exports them as CSV files — all in one click.

---

## 🔍 Overview

Have you ever been stuck manually combing through a 50+ page bank statement with a calculator in hand?  
This tool was built to solve that.

It allows you to upload one or multiple PDF bank statements, automatically detects structured tables (like account info and transaction logs), and converts them into structured CSV files — ready for Excel or further analysis.

---

## 🚀 Features

- ✅ Upload **single or multiple** PDF files  
- ✅ Extract **account metadata** (e.g., account number, currency, balance)  
- ✅ Extract **transaction tables** with debits, credits, and balances  
- ✅ One-click **CSV export** for both tables  
- ✅ Clean, responsive UI with **Streamlit**  

---

## 📸 Demo

Try it live 👉 [https://pdftocsv.streamlit.app/](https://pdftocsv.streamlit.app/)

---

## ⚙️ Tech Stack

- [Streamlit](https://streamlit.io/) — for the web UI  
- [pdfplumber](https://github.com/jsvine/pdfplumber) — for PDF parsing  
- [Pandas](https://pandas.pydata.org/) — for data wrangling

---

## 🧠 How It Works

1. Upload a PDF containing bank statements.
2. The app scans each page for tables:
   - If a table has two columns, it’s treated as **metadata**.
   - If it has more than two, it’s treated as a **transaction log**.
3. Both tables are displayed on-screen.
4. Download them as CSV files using the buttons provided.
