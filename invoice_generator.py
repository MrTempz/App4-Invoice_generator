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


def add_header(pdf: FPDF, invoice_file_name: str):
    invoice_no, invoice_date = invoice_file_name.split('-',maxsplit=1)

    pdf.add_page()
    pdf.set_font(family='Times', size=16, style='B')
    pdf.cell(w=50, h=8, txt=f'Invoice no. {invoice_no}', ln=1)
    pdf.cell(w=50, h=8, txt=f'Invoice date {invoice_date}', ln=1)


def add_contents(pdf: FPDF, invoice_df: pd.DataFrame):
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
    
def add_summary(pdf: FPDF, invoice_df: pd.DataFrame):
    pdf.set_font(family='Times', size=10, style='B')
    pdf.set_text_color(80, 80, 80)

    for column in list(INVOICE_COLUMNS.values())[:-1]:
        pdf.cell(w=column['size'], h=8, txt='', border=1)
    total_sum = invoice_df['total_price'].sum()
    pdf.cell(w=INVOICE_COLUMNS[4]['size'], h=8, txt=str(total_sum), 
        border=1, ln=1)

    pdf.set_font(family='Times', size=12, style='B')
    pdf.set_text_color(0,0,0)
    pdf.cell(w=120, h=8, txt=f'Total ammount due is ${total_sum}', ln=1)
    
    pdf.set_font(family='Times', size=20, style='B')
    pdf.cell(w=36, h=8, txt='PythonHow')
    pdf.image('pythonhow.png', w=8)


def generate_invoice(invoice_df: pd.DataFrame, invoice_file_name: str) -> FPDF:
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    add_header(pdf, invoice_file_name)
    add_contents(pdf, invoice_df=invoice_df)
    add_summary(pdf, invoice_df=invoice_df)

    pdf_output = os.path.join('PDFs', f'{invoice_file_name}.pdf')
    pdf.output(pdf_output)


if __name__ == '__main__':
    filepaths = [os.path.join('invoices', item) for item 
        in os.listdir('invoices') if '.xlsx' in item]
    
    for filepath in filepaths:

        df = pd.read_excel(filepath, sheet_name='Sheet 1')
        generate_invoice(invoice_df=df, invoice_file_name=Path(filepath).stem)


