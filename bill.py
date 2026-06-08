import streamlit as st
import pandas as pd
from datetime import date

# 1. Page Configuration
st.set_page_config(page_title="Web Billing App", layout="wide")

# 2. Initialize Session State (This saves seller details while the app is running)
if 'seller' not in st.session_state:
    st.session_state.seller = {
        "company_name": "Akash Enterprises",
        "address": "11, Main Market, Chandni Chowk, New Delhi",
        "phone": "+91 9981278197",
        "email": "akashenterprises@gmail.com",
        "gstin": "08AALCR2857A1ZD",
        "pan": "AVHPC6971A"
    }

# 3. Create Navigation Tabs
tab_create, tab_seller = st.tabs(["Create Invoice", "Edit Seller Details"])

# --- TAB: EDIT SELLER DETAILS ---
with tab_seller:
    st.header("Update Seller Information")
    st.info("These details will appear at the top of every generated invoice.")
    
    with st.form("seller_form"):
        new_name = st.text_input("Company Name", value=st.session_state.seller["company_name"])
        new_address = st.text_input("Address", value=st.session_state.seller["address"])
        col1, col2 = st.columns(2)
        new_phone = col1.text_input("Phone", value=st.session_state.seller["phone"])
        new_email = col2.text_input("Email", value=st.session_state.seller["email"])
        col3, col4 = st.columns(2)
        new_gstin = col3.text_input("GSTIN", value=st.session_state.seller["gstin"])
        new_pan = col4.text_input("PAN Number", value=st.session_state.seller["pan"])
        
        if st.form_submit_button("Save Details"):
            st.session_state.seller.update({
                "company_name": new_name, "address": new_address,
                "phone": new_phone, "email": new_email,
                "gstin": new_gstin, "pan": new_pan
            })
            st.success("Seller details updated successfully!")

# --- TAB: CREATE INVOICE ---
with tab_create:
    st.header("Generate New Tax Invoice")
    
    # Invoice Metadata
    col_meta1, col_meta2 = st.columns(2)
    invoice_no = col_meta1.text_input("Invoice No.", "INV-001")
    invoice_date = col_meta2.date_input("Invoice Date", date.today())
    
    st.divider()
    
    # Customer Details (BILL TO) - SHIP TO is removed
    st.subheader("Bill To (Customer Details)")
    col_c1, col_c2 = st.columns(2)
    cust_name = col_c1.text_input("Customer Name")
    cust_address = col_c1.text_area("Customer Address")
    cust_phone = col_c2.text_input("Customer Phone")
    cust_gstin = col_c2.text_input("Customer GSTIN (Optional)")
    cust_pan = col_c2.text_input("Customer PAN (Optional)")
    
    st.divider()
    
    # Item Entry using an interactive data editor
    st.subheader("Invoice Items")
    st.write("Add your items below. The total amount will be calculated automatically.")
    
    # Create an empty dataframe for the user to edit
    empty_df = pd.DataFrame(
        [{"Item": "", "HSN": "", "Qty": 0, "Rate (Rs)": 0.0, "Tax %": 5.0}] * 3
    )
    
    edited_df = st.data_editor(empty_df, num_rows="dynamic", use_container_width=True)
    
    st.divider()
    
    # Calculate Totals
    total_amount = 0
    for index, row in edited_df.iterrows():
        if row["Item"] != "":
            qty = float(row["Qty"])
            rate = float(row["Rate (Rs)"])
            tax_rate = float(row["Tax %"]) / 100
            
            base_price = qty * rate
            tax_amount = base_price * tax_rate
            total_amount += (base_price + tax_amount)

    st.subheader(f"Grand Total: Rs. {total_amount:.2f}")
    
    if st.button("Generate Final Bill (Preview)"):
        st.success("Invoice Generated successfully!")
        # Here you would typically integrate a PDF library like 'fpdf' or 'reportlab'
        # to take the session_state and edited_df and write it to a downloadable file.
        st.write("### Preview:")
        st.json({
            "Seller": st.session_state.seller,
            "Customer": {"Name": cust_name, "Phone": cust_phone},
            "Total": total_amount
        })