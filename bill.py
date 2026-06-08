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
    pdf.cell(70, 8,
