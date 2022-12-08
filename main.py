import streamlit as st
import pandas as pd
from os import path
import invoice_generator as ig

st.set_page_config(layout='wide')

st.title("Invoice generator")
st.header("Generate PDF invoices from excel files")

content = f"""
In order to generate invoice, please upload an Excel.\n
Excel file name has to be in format <invoice number>-<date>.xlsx\n
Column names have to be:\n
{' | '.join([column['name'] for column in ig.INVOICE_COLUMNS.values()])}\n
Invoice data have to be in 'Sheet 1' sheet of the file.\n
For examples please check Examples tab selectable in menu on the left.
"""
st.write(content)

uploaded_file = st.file_uploader(label='Upload your Excel file', type='xlsx')

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name='Sheet 1')
    file_name = uploaded_file.name
    invoice_name = file_name.replace('.xlsx', '')
    st.table(df)
    
    ig.generate_invoice(invoice_df=df, invoice_file_name=invoice_name)

    PDF_invoice_name=f'{invoice_name}.pdf'

    with open(path.join('PDFs', PDF_invoice_name), 'rb') as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label='Download invoice', data=PDFbyte, 
        file_name=PDF_invoice_name)
    
