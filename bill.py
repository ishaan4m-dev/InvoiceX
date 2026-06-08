import streamlit as st
from datetime import date
from fpdf import FPDF
from num2words import num2words

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Automotive Billing App", layout="wide")

# --- INITIALIZE SELLER DATA ---
if 'seller' not in st.session_state:
    st.session_state.seller = {
        "company_name": "BIYANI MOTORS PVT LTD",
        "address": "A-7, MATHURA ROAD, NEW DELHI, DELHI",
        "phone": "+91 99999 99999",
        "email": "sales@biyanimotors.com",
        "gstin": "07ABCDE12347A1BC",
        "pan": "AAAAA1234A",
        "terms": "1. All disputes are subject to New Delhi Jurisdiction only.\n2. Vehicle to be delivered post completion of documentation."
    }

# --- PDF GENERATION ENGINE ---
def generate_pdf(invoice_no, cust, veh, price, finance, seller):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. HEADER (Seller Details & Invoice Info)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(120, 8, seller['company_name'], ln=0)
    pdf.set_font("Arial", '', 10)
    pdf.cell(70, 8, "TAX INVOICE", ln=1, align='R')
    
    pdf.set_font("Arial", '', 9)
    pdf.cell(120, 5, seller['address'], ln=0)
    pdf.cell(70, 5, f"Invoice No: {invoice_no}", ln=1, align='R')
    
    pdf.cell(120, 5, f"Phone: {seller['phone']} | Email: {seller['email']}", ln=0)
    pdf.cell(70, 5, f"Date: {date.today().strftime('%d %b %Y')}", ln=1, align='R')
    
    pdf.cell(190, 5, f"GSTIN: {seller['gstin']} | PAN: {seller['pan']}", ln=1)
    
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(2)

    # 2. BILL TO SECTION (Customer Details)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 6, "BILL TO:", ln=1)
    
    pdf.set_font("Arial", '', 9)
    pdf.cell(190, 5, f"Name:   {cust['name']}", ln=1)
    pdf.cell(190, 5, f"Address: {cust['address']}", ln=1)
    pdf.cell(100, 5, f"Mobile:  {cust['mobile']}", ln=0)
    pdf.cell(90, 5, f"Email:   {cust['email']}", ln=1)
    pdf.cell(100, 5, f"Aadhar:  {cust['aadhar']}", ln=0)
    pdf.cell(90, 5, f"PAN:     {cust['pan']}", ln=1)
    
    gst_text = cust['gstin'] if cust['gstin'] else "UNREGISTERED"
    pdf.cell(100, 5, f"GSTIN:   {gst_text}", ln=0)
    pdf.cell(90, 5, f"Place of Supply: {cust['pos']}", ln=1)

    pdf.line(10, pdf.get_y()+2, 200, pdf.get_y()+2)
