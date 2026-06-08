import streamlit as st
import pandas as pd
from datetime import date
from fpdf import FPDF
from num2words import num2words
import base64

st.set_page_config(page_title="Vehicle Billing Software", layout="wide")

# --- PDF GENERATION FUNCTION ---
def create_pdf(invoice_no, cust_name, vehicle, pricing):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="TAX INVOICE - VEHICLE SALES", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Invoice No: {invoice_no} | Date: {date.today()}", ln=True, align='R')
    pdf.line(10, 30, 200, 30)
    
    # Customer Details
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Bill To:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 8, txt=f"Name: {cust_name}", ln=True)
    
    # Vehicle Details
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Vehicle Details:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(100, 8, txt=f"Model: {vehicle['model']} | Color: {vehicle['color']}", ln=True)
    pdf.cell(100, 8, txt=f"Engine No: {vehicle['engine']} | Chassis No: {vehicle['chassis']}", ln=True)
    pdf.cell(100, 8, txt=f"VIN: {vehicle['vin']}", ln=True)
    
    # Pricing Table Header
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(60, 10, 'Description', 1, 0, 'C')
    pdf.cell(40, 10, 'Pre-Tax Amount', 1, 0, 'C')
    pdf.cell(30, 10, f"GST ({pricing['gst_rate']}%)", 1, 0, 'C')
    pdf.cell(30, 10, 'Discount', 1, 0, 'C')
    pdf.cell(30, 10, 'Total', 1, 1, 'C')
    
    # Pricing Table Data
    pdf.set_font("Arial", size=10)
    pdf.cell(60, 10, vehicle['model'], 1, 0, 'L')
    pdf.cell(40, 10, f"Rs. {pricing['pre_tax']:.2f}", 1, 0, 'R')
    pdf.cell(30, 10, f"Rs. {pricing['tax_amt']:.2f}", 1, 0, 'R')
    pdf.cell(30, 10, f"Rs. {pricing['discount']:.2f}", 1, 0, 'R')
    pdf.cell(30, 10, f"Rs. {pricing['net_payable']:.2f}", 1, 1, 'R')
    
    # Totals and Words
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Ex-Showroom Price (Incl. Tax): Rs. {pricing['ex_showroom']:.2f}", ln=True, align='R')
    pdf.cell(200, 10, txt=f"Final Net Payable: Rs. {pricing['net_payable']:.2f}", ln=True, align='R')
    
    pdf.ln(5)
    pdf.set_font("Arial", 'I', 11)
    amount_words = num2words(pricing['net_payable'], lang='en_IN').title()
    pdf.cell(200, 10, txt=f"Amount in Words: Rupees {amount_words} Only", ln=True)
    
    return pdf.output(dest="S").encode("latin-1")

# --- UI LAYOUT ---
st.title("Vehicle Billing System")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Customer Details")
    invoice_no = st.text_input("Invoice Number", "INV-1001")
    cust_name = st.text_input("Customer Name")
    
    st.subheader("Vehicle Details")
    model = st.text_input("Car Model (e.g., SUV LX 2024)")
    color = st.text_input("Color")
    engine = st.text_input("Engine Number")
    chassis = st.text_input("Chassis Number")
    vin = st.text_input("VIN Number")

with col2:
    st.subheader("Pricing & Tax")
    ex_showroom = st.number_input("Ex-Showroom Price (Inclusive of GST)", min_value=0.0, value=1000000.0, step=1000.0)
    gst_rate = st.number_input("GST Rate (%)", min_value=0.0, value=28.0, step=1.0)
    discount = st.number_input("Discount Amount", min_value=0.0, value=0.0, step=500.0)
    
    # Core Mathematical Logic
    if gst_rate >= 0:
        pre_tax_price = ex_showroom / (1 + (gst_rate / 100))
        tax_amount = ex_showroom - pre_tax_price
    else:
        pre_tax_price = ex_showroom
        tax_amount = 0
        
    net_payable = ex_showroom - discount

    st.divider()
    st.write("### Financial Breakdown")
    st.write(f"**Price Before Tax:** Rs. {pre_tax_price:,.2f}")
    st.write(f"**GST Amount:** Rs. {tax_amount:,.2f}")
    st.write(f"**Ex-Showroom Price:** Rs. {ex_showroom:,.2f}")
    st.write(f"**Discount Applied:** - Rs. {discount:,.2f}")
    st.write(f"### Final Payable: Rs. {net_payable:,.2f}")
    
    try:
        words = num2words(net_payable, lang='en_IN').title()
        st.info(f"**Amount in Words:** Rupees {words} Only")
    except:
        pass

st.divider()

# --- PDF GENERATION TRIGGER ---
if st.button("Generate & Download PDF Bill", type="primary"):
    vehicle_data = {"model": model, "color": color, "engine": engine, "chassis": chassis, "vin": vin}
    pricing_data = {
        "pre_tax": pre_tax_price, "tax_amt": tax_amount, "gst_rate": gst_rate, 
        "ex_showroom": ex_showroom, "discount": discount, "net_payable": net_payable
    }
    
    pdf_bytes = create_pdf(invoice_no, cust_name, vehicle_data, pricing_data)
    
    st.download_button(
        label="📥 Click here to Download PDF",
        data=pdf_bytes,
        file_name=f"{invoice_no}_{cust_name.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
