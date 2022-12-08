import pandas as pd
import os
from pathlib import Path
from fpdf import FPDF



def add_header(pdf: FPDF, invoice_file_path: str):
    file_name = Path(invoice_file_path).stem
    invoice_no, invoice_date = file_name.split('-',maxsplit=1)

    pdf.add_page()
    pdf.set_font(family='Times', size=16, style='B')
    pdf.cell(w=50, h=8, txt=f'Invoice no. {invoice_no}', ln=1)
    pdf.cell(w=50, h=8, txt=f'Invoice date {invoice_date}', ln=1)


def generate_invoice(invoice_df: pd.DataFrame, invoive_file_path: str) -> FPDF:
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    add_header(pdf, invoive_file_path)

    return pdf


if __name__ == '__main__':
    filepaths = [os.path.join('invoices', item) for item 
        in os.listdir('invoices') if '.xlsx' in item]
    
    for filepath in filepaths:

        df = pd.read_excel(filepath, sheet_name='Sheet 1')
        pdf = generate_invoice(invoice_df=df, invoive_file_path=filepath)

        filename = Path(filepath).stem
        pdf_output = os.path.join('PDFs', f'{filename}.pdf')
        pdf.output(pdf_output)

