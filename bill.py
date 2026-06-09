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
    pdf.ln(5)

    # 3. MAIN BILLING TABLE (Vehicle Details inside)
    pdf.set_font("Arial", 'B', 9)
    # Adjusted widths: 110 + 40 + 40 = 190 total width
    pdf.cell(110, 8, "Vehicle Description & Details", border=1, align='C')
    pdf.cell(40, 8, "Base Rate (Rs)", border=1, align='C')
    pdf.cell(40, 8, "Ex-Showroom (Rs)", border=1, align='C', ln=1)
    
    # Table Body
    pdf.set_font("Arial", '', 9)
    
    # Row 1: Model & Pricing
    pdf.cell(110, 6, f" {veh['model']} ({veh['color']})", border='LR', align='L')
    pdf.cell(40, 6, f"{price['pre_tax']:,.2f}", border='LR', align='R')
    pdf.cell(40, 6, f"{price['ex_showroom']:,.2f}", border='LR', align='R', ln=1)
    
    # Rows 2-5: Specific Credentials including Mfg Year
    pdf.cell(110, 6, f" Mfg Year: {veh['year']}", border='LR', align='L')
    pdf.cell(40, 6, "", border='LR')
    pdf.cell(40, 6, "", border='LR', ln=1)

    pdf.cell(110, 6, f" Engine No: {veh['engine']}", border='LR', align='L')
    pdf.cell(40, 6, "", border='LR')
    pdf.cell(40, 6, "", border='LR', ln=1)
    
    pdf.cell(110, 6, f" Chassis No: {veh['chassis']}", border='LR', align='L')
    pdf.cell(40, 6, "", border='LR')
    pdf.cell(40, 6, "", border='LR', ln=1)
    
    pdf.cell(110, 6, f" VIN Number: {veh['vin']}", border='LR', align='L')
    pdf.cell(40, 6, "", border='LR')
    pdf.cell(40, 6, "", border='LR', ln=1)

    # Close the table with a bottom line
    pdf.cell(110, 0, "", border='T')
    pdf.cell(40, 0, "", border='T')
    pdf.cell(40, 0, "", border='T', ln=1)

    # Discount Row (Only shows if discount > 0)
    if price['discount'] > 0:
        pdf.set_font("Arial", '', 9)
        pdf.cell(150, 8, "Less: Discount ", border=1, align='R')
        pdf.cell(40, 8, f"- Rs. {price['discount']:,.2f}", border=1, align='R', ln=1)

    # Net Payable Row
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(150, 8, "FINAL NET PAYABLE : ", border=1, align='R')
    pdf.cell(40, 8, f"Rs. {price['net_payable']:,.2f}", border=1, align='R', ln=1)

    # 4. TAX BREAKDOWN TABLE
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(190, 6, "Tax Breakdown:", ln=1)
    
    pdf.cell(50, 8, "Price Before Tax", border=1, align='C')
    pdf.cell(40, 8, "GST Rate", border=1, align='C')
    pdf.cell(50, 8, "GST Amount", border=1, align='C')
    pdf.cell(50, 8, "Ex-Showroom Price", border=1, align='C', ln=1)
    
    pdf.set_font("Arial", '', 9)
    pdf.cell(50, 8, f"Rs. {price['pre_tax']:,.2f}", border=1, align='C')
    pdf.cell(40, 8, f"{price['gst_rate']}%", border=1, align='C')
    pdf.cell(50, 8, f"Rs. {price['tax_amt']:,.2f}", border=1, align='C')
    pdf.cell(50, 8, f"Rs. {price['ex_showroom']:,.2f}", border=1, align='C', ln=1)

    # 5. FINANCE DETAILS TABLE (Dynamic)
    if finance['is_financed']:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(190, 6, "Finance Details:", ln=1)
        
        pdf.cell(70, 8, "Financier / Bank Name", border=1, align='C')
        pdf.cell(60, 8, "Loan Amount", border=1, align='C')
        pdf.cell(60, 8, "Reference / DO Number", border=1, align='C', ln=1)
        
        pdf.set_font("Arial", '', 9)
        pdf.cell(70, 8, finance['bank'], border=1, align='C')
        pdf.cell(60, 8, f"Rs. {finance['amount']:,.2f}", border=1, align='C')
        pdf.cell(60, 8, finance['ref_no'], border=1, align='C', ln=1)

    # 6. AMOUNT IN WORDS
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 9)
    try:
        amt_words = num2words(price['net_payable'], lang='en_IN').title()
        pdf.cell(190, 6, f"Amount in Words: Rupees {amt_words} Only", ln=1)
    except:
        pass

    # 7. FOOTER (Terms & Signatures)
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
        c_pos = st.text_input("Place of Supply (e.g., Delhi, Chandigarh)")

    st.divider()

    # 2. Vehicle Details
    st.subheader("Vehicle Details")
    vc1, vc2 = st.columns(2)
    with vc1:
        v_model = st.text_input("Car Model (e.g., CAMRY HYBRID ZX)")
        v_color = st.text_input("Color")
        v_year = st.text_input("Manufacturing Year (e.g., 2024)")
    with vc2:
        v_engine = st.text_input("Engine No.")
        v_chassis = st.text_input("Chassis No.")
        v_vin = st.text_input("VIN Number")

    st.divider()

    # 3. Finance Details
    st.subheader("Finance Options")
    is_financed = st.checkbox("Vehicle is Financed (Check to add finance details to bill)")
    
    f_bank = ""
    f_amount = 0.0
    f_ref = ""
    
    if is_financed:
        fc1, fc2, fc3 = st.columns(3)
        f_bank = fc1.text_input("Financier / Bank Name")
        f_amount = fc2.number_input("Loan Amount", min_value=0.0, step=10000.0)
        f_ref = fc3.text_input("DO / Reference Number")

    st.divider()

    # 4. Pricing
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

    # 5. Generate Button
    if st.button("Generate & Download PDF", type="primary"):
        customer_data = {"name": c_name, "address": c_address, "mobile": c_mobile, "email": c_email, "aadhar": c_aadhar, "pan": c_pan, "gstin": c_gstin, "pos": c_pos}
        vehicle_data = {"model": v_model, "color": v_color, "year": v_year, "engine": v_engine, "chassis": v_chassis, "vin": v_vin}
        pricing_data = {"pre_tax": pre_tax, "tax_amt": tax_amt, "gst_rate": gst_rate, "ex_showroom": ex_showroom, "discount": discount, "net_payable": net_payable}
        finance_data = {"is_financed": is_financed, "bank": f_bank, "amount": f_amount, "ref_no": f_ref}
        
        pdf_bytes = generate_pdf(invoice_no, customer_data, vehicle_data, pricing_data, finance_data, st.session_state.seller)
        
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
