import streamlit as st
from datetime import date
from fpdf import FPDF
from num2words import num2words

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Automotive Billing App", layout="wide")

# --- INITIALIZE SELLER DATA ---
if 'seller' not in st.session_state:
    st.session_state.seller = {
        "company_name": "Akash Enterprises",
        "address": "11, Main Market, Chandni Chowk, New Delhi, Delhi 110006",
        "phone": "+91 9981278197",
        "email": "akashenterprises@gmail.com",
        "gstin": "08AALCR2857A1ZD",
        "pan": "AVHPC6971A",
        "terms": "1. Customer will pay the GST.\n2. Customer will pay Delivery charges.\n3. Pay due amount within 15 days."
    }

# --- PDF GENERATION ENGINE ---
def generate_pdf(invoice_no, cust, veh, price, seller):
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
