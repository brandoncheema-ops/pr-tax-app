import streamlit as st
import pandas as pd

st.set_page_config(page_title="PR Tourism Tax Extractor", layout="wide")

st.title("🇵🇷 PR Tourism Tax Data Extractor")
st.markdown("Upload your Airbnb Earnings CSV to get totals for the 7% Room Tax declaration.")

uploaded_file = st.file_uploader("Choose an Airbnb CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # 1. Clean and Filter Data
    # We only want 'Reservation' or 'Cancellation Fee'
    taxable_df = df[df['Type'].isin(['Reservation', 'Cancellation Fee'])].copy()
    
    # Ensure columns are numeric (handling potential string formats)
    taxable_df['Gross earnings'] = pd.to_numeric(taxable_df['Gross earnings'], errors='coerce')
    taxable_df['Occupancy taxes'] = pd.to_numeric(taxable_df['Occupancy taxes'], errors='coerce')
    taxable_df['Nights'] = pd.to_numeric(taxable_df['Nights'], errors='coerce')

    # 2. Extract Month (assuming 'Start date' format MM/DD/YYYY)
    taxable_df['Date_Parsed'] = pd.to_datetime(taxable_df['Start date'])
    month_year = taxable_df['Date_Parsed'].dt.strftime('%B %Y').iloc[0] if not taxable_df.empty else "Unknown"

    # 3. Calculate Totals
    gross_revenue = taxable_df['Gross earnings'].sum()
    occ_tax = taxable_df['Occupancy taxes'].sum()
    nights_occupied = taxable_df['Nights'].sum()

    # 4. Display Result Table
    st.subheader(f"Reporting Period: {month_year}")
    
    results = {
        "Reporting Month": [month_year],
        "Gross Taxable Revenue": [f"${gross_revenue:,.2f}"],
        "7% Occupancy Tax": [f"${occ_tax:,.2f}"],
        "Nights Occupied": [int(nights_occupied)]
    }
    
    st.table(pd.DataFrame(results))

    # 5. Copy-Paste Section
    st.divider()
    st.subheader("Monthly Totals for Copying")
    st.code(f"Gross Revenue: {gross_revenue:.2f}")
    st.code(f"7% Tax: {occ_tax:.2f}")
    st.code(f"Nights: {int(nights_occupied)}")
