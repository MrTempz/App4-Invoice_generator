import streamlit as st
import pandas as pd
import os
from pathlib import Path
import invoice_generator as ig

st.set_page_config(layout='wide')

st.title("Invoice generator example")

content = f"""
Here you can see excel files lookup and download sample invoices generated from 
said files.
"""
st.write(content)

filepaths = [os.path.join('invoices', item) for item 
    in os.listdir('invoices') if '.xlsx' in item]

for filepath in filepaths:
    invoice_file_name=Path(filepath).stem
    invoice_name = invoice_file_name.replace('.xlsx', '')
    st.write(invoice_file_name)

    col1, empty_col, col2 = st.columns([2,0.5,0.5])
    with col1:
        df = pd.read_excel(filepath, sheet_name='Sheet 1')
        st.table(df)

    with col2:
        ig.generate_invoice(invoice_df=df, invoice_file_name=invoice_file_name)
        PDF_invoice_name=f'{invoice_name}.pdf'

        with open(os.path.join('PDFs', PDF_invoice_name), 'rb') as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(label=f'Download {invoice_name} invoice', 
            data=PDFbyte, file_name=PDF_invoice_name)

        