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
    
    pdf.set_font("Arial", '', 9)
    pdf.cell(190, 5, f"Name:   {cust['name']}", ln=1)
    pdf.cell(190, 5, f"Address: {cust['address']}", ln=1)
    pdf.cell(100, 5, f"Mobile:  {cust['mobile']}", ln=0)
    pdf.cell(90, 5, f"Email:   {cust['email']}", ln=1)
    pdf.cell(100, 5, f"Aadhar:  {cust['aadhar']}", ln=0)
    pdf.cell(90, 5, f"PAN:     {cust['pan']}", ln=1)
    if cust['gstin']:
        pdf.cell(190, 5, f"GSTIN:   {cust['gstin']}", ln=1)

    pdf.line(10, pdf.get_y()+2, 200, pdf.get_y()+2)
    pdf.ln(5)

    # 3. VEHICLE DETAILS SECTION
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 6, "VEHICLE DETAILS:", ln=1)
    pdf.set_font("Arial", '', 9)
    pdf.cell(95, 5, f"Model: {veh['model']}", ln=0)
    pdf.cell(95, 5, f"Color: {veh['color']}", ln=1)
    pdf.cell(95, 5, f"Engine No: {veh['engine']}", ln=0)
    pdf.cell(95, 5, f"Chassis No: {veh['chassis']}", ln=1)
    pdf.cell(190, 5, f"VIN Number: {veh['vin']}", ln=1)
    
    pdf.ln(5)

    # 4. MAIN BILLING TABLE
    # Table Header
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(90, 8, "Description", border=1, align='C')
    pdf.cell(30, 8, "Base Rate (Rs)", border=1, align='C')
    pdf.cell(35, 8, f"GST ({price['gst_rate']}%)", border=1, align='C')
    pdf.cell(35, 8, "Amount (Rs)", border=1, align='C', ln=1)
    
    # Table Body
    pdf.set_font("Arial", '', 9)
    # The vehicle row
    x_start = pdf.get_x()
    y_start = pdf.get_y()
    
    pdf.cell(90, 20, f"{veh['model']} ({veh['color']})", border=1, align='C')
    pdf.cell(30, 20, f"{price['pre_tax']:,.2f}", border=1, align='R')
    pdf.cell(35, 20, f"{price['tax_amt']:,.2f}", border=1, align='R')
    pdf.cell(35, 20, f"{(price['pre_tax'] + price['tax_amt']):,.2f}", border=1, align='R', ln=1)
    
    # Discount Row
    if price['discount'] > 0:
        pdf.cell(155, 8, "Less: Discount", border=1, align='R')
        pdf.cell(35, 8, f"- {price['discount']:,.2f}", border=1, align='R', ln=1)
    
    # Grand Total Row
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(155, 10, "GRAND TOTAL (Net Payable)", border=1, align='R')
    pdf.cell(35, 10, f"Rs. {price['net_payable']:,.2f}", border=1, align='R', ln=1)

    # 5. AMOUNT IN WORDS
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 9)
    try:
        amt_words = num2words(price['net_payable'], lang='en_IN').title()
        pdf.cell(190, 6, f"Amount in Words: Rupees {amt_words} Only", ln=1)
    except:
        pass

    # 6. FOOTER (Terms & Signatures)
    pdf.ln(10)
    y_footer = pdf.get_y()
    
    # Terms Box (Left side)
    pdf.set_font("Arial", 'B', 8)
    pdf.cell(100, 5, "Terms & Conditions:", ln=1)
    pdf.set_font("Arial", '', 8)
    pdf.multi_cell(100, 4, seller['terms'])
    
    # Signature Box (Right side)
    pdf.set_xy(120, y_footer)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(70, 5, f"For {seller['company_name']}", ln=1, align='R')
    pdf.ln(15)
    pdf.set_x(120)
    pdf.cell(70, 5, "Authorized Signatory", ln=1, align='R')

    return pdf.output(dest="S").encode("latin-1")


# --- UI LAYOUT ---
st.title("Automotive Billing System")

tab_invoice, tab_seller = st.tabs(["Create Invoice", "Edit Seller Details"])

# --- TAB 1: CREATE INVOICE ---
with tab_invoice:
    st.header("Generate Tax Invoice")
    
    col_inv1, col_inv2 = st.columns(2)
    invoice_no = col_inv1.text_input("Invoice Number", "INV-1001")
    invoice_date = col_inv2.date_input("Invoice Date", date.today())
    
    st.divider()
    
    # 1. Customer Details
    st.subheader("Customer Details (Bill To)")
    cc1, cc2 = st.columns(2)
    with cc1:
        c_name = st.text_input("Customer Name")
        c_address = st.text_area("Address")
        c_mobile = st.text_input("Mobile No.")
        c_email = st.text_input("Email")
    with cc2:
        c_aadhar = st.text_input("Aadhar No.")
        c_pan = st.text_input("PAN No.")
        c_gstin = st.text_input("GST No. (If registered)")

    st.divider()

    # 2. Vehicle Details
    st.subheader("Vehicle Details")
    vc1, vc2 = st.columns(2)
    with vc1:
        v_model = st.text_input("Car Model")
        v_color = st.text_input("Color")
        v_vin = st.text_input("VIN Number")
    with vc2:
        v_engine = st.text_input("Engine No.")
        v_chassis = st.text_input("Chassis No.")

    st.divider()

    # 3. Pricing
    st.subheader("Pricing & Tax Calculations")
    pc1, pc2 = st.columns(2)
    with pc1:
        ex_showroom = st.number_input("Ex-Showroom Price (Inclusive of GST)", min_value=0.0, step=1000.0)
        gst_rate = st.number_input("GST Rate (%)", min_value=0.0, value=28.0, step=1.0)
        discount = st.number_input("Discount Amount", min_value=0.0, step=500.0)
    
    # Mathematical Logic
    if gst_rate > 0:
        pre_tax = ex_showroom / (1 + (gst_rate / 100))
        tax_amt = ex_showroom - pre_tax
    else:
        pre_tax = ex_showroom
        tax_amt = 0
        
    net_payable = ex_showroom - discount

    with pc2:
        st.write("### Live Breakdown")
        st.write(f"**Pre-Tax Base Price:** Rs. {pre_tax:,.2f}")
        st.write(f"**GST Amount:** Rs. {tax_amt:,.2f}")
        st.write(f"**Discount:** - Rs. {discount:,.2f}")
        st.write(f"### Net Payable: Rs. {net_payable:,.2f}")

    st.divider()

    # 4. Generate Button
    if st.button("Generate & Download PDF", type="primary"):
        # Package data
        customer_data = {"name": c_name, "address": c_address, "mobile": c_mobile, "email": c_email, "aadhar": c_aadhar, "pan": c_pan, "gstin": c_gstin}
        vehicle_data = {"model": v_model, "color": v_color, "engine": v_engine, "chassis": v_chassis, "vin": v_vin}
        pricing_data = {"pre_tax": pre_tax, "tax_amt": tax_amt, "gst_rate": gst_rate, "discount": discount, "net_payable": net_payable}
        
        # Generate
        pdf_bytes = generate_pdf(invoice_no, customer_data, vehicle_data, pricing_data, st.session_state.seller)
        
        st.download_button(
            label="📥 Download Invoice PDF",
            data=pdf_bytes,
            file_name=f"{invoice_no}_{c_name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

# --- TAB 2: EDIT SELLER DETAILS ---
with tab_seller:
    st.header("Update Seller Information")
    st.info("These credentials print at the top of the invoice.")
    
    with st.form("seller_form"):
        new_name = st.text_input("Company Name", value=st.session_state.seller["company_name"])
        new_address = st.text_area("Address", value=st.session_state.seller["address"])
        sc1, sc2 = st.columns(2)
        new_phone = sc1.text_input("Mobile No.", value=st.session_state.seller["phone"])
        new_email = sc2.text_input("Email", value=st.session_state.seller["email"])
        sc3, sc4 = st.columns(2)
        new_gstin = sc3.text_input("GSTIN", value=st.session_state.seller["gstin"])
        new_pan = sc4.text_input("PAN No.", value=st.session_state.seller["pan"])
        
        new_terms = st.text_area("Terms and Conditions (Appears at bottom of bill)", value=st.session_state.seller["terms"], height=150)
        
        if st.form_submit_button("Save Credentials"):
            st.session_state.seller.update({
                "company_name": new_name, "address": new_address,
                "phone": new_phone, "email": new_email,
                "gstin": new_gstin, "pan": new_pan, "terms": new_terms
            })
            st.success("Seller credentials updated! Generate a new bill to see changes.")
