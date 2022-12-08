import pandas as pd
import os
from pathlib import Path
from fpdf import FPDF

INVOICE_COLUMNS={0: {'name': 'product_id', 'size': 30, 'ln': 0},
                 1: {'name': 'product_name', 'size': 70, 'ln': 0}, 
                 2: {'name': 'amount_purchased', 'size': 30, 'ln': 0},
                 3: {'name': 'price_per_unit', 'size': 30, 'ln': 0},
                 4: {'name': 'total_price', 'size': 30, 'ln': 1}
}


def add_header(pdf: FPDF, invoice_file_path: str):
    file_name = Path(invoice_file_path).stem
    invoice_no, invoice_date = file_name.split('-',maxsplit=1)

    pdf.add_page()
    pdf.set_font(family='Times', size=16, style='B')
    pdf.cell(w=50, h=8, txt=f'Invoice no. {invoice_no}', ln=1)
    pdf.cell(w=50, h=8, txt=f'Invoice date {invoice_date}', ln=1)


def add_table(pdf: FPDF, invoice_df: pd.DataFrame):
    pdf.set_font(family='Times', size=10, style='B')
    pdf.set_text_color(80, 80, 80)

    for column in INVOICE_COLUMNS.values():
        pdf.cell(w=column['size'], h=8, 
            txt=column['name'].replace('_', ' ').title(), 
            border=1, ln=column['ln'])

    pdf.set_font(family='Times', size=10)
    for index, row in invoice_df.iterrows():
        for column in INVOICE_COLUMNS.values():
            pdf.cell(w=column['size'], h=8, txt=str(row[column['name']]),
                border=1, ln=column['ln'])


def generate_invoice(invoice_df: pd.DataFrame, invoive_file_path: str) -> FPDF:
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    add_header(pdf, invoive_file_path)
    add_table(pdf, invoice_df=invoice_df)

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

