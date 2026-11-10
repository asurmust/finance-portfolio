python
# Import the streamdown web framework for rendering UI elements
import streamlit as st
# Import pandas for parsing data tables and ledger structures
import pandas as pd
# Import io to convert string text arrays into file-like data streams
import io

# Configure the browser tab title and set the interface to wide viewport mode
st.set_page_config(page_title="Aayan Surmust - Accounting Portfolio", layout="wide")

# Render the primary header block at the top of the webpage layout
st.title("📊 Aayan Surmust - Technical Finance Portfolio")
# Provide introductory copy explaining how to use the interactive dashboard
st.write("Welcome to my interactive portfolio. Click the tabs below to run my custom engines against live data.")

# Create three navigation tabs to organize the accounts, tax, and profile tools
tab1, tab2, tab3 = st.tabs(["Trial Balance Parser", "Marginal Tax Relief Calculator", "About Me"])

# =====================================================================
# TAB 1: TRIAL BALANCE SUSPENSE PARSER (FAPS MODULE PREP)
# =====================================================================
# Open the context block to render content inside the first tab item
with tab1:
    # Render the structural section title for the accounts close tool
    st.header("Trial Balance Suspense Account Parser")
    # Explain the accounting logic and validation checks handled by this tab
    st.write("This engine scans raw client transactions, cleans data text, balances debits and credits, and isolates variances into a Suspense Account.")
    
    # Store a raw string array mimicking a messy, unverified client dataset
    default_csv = """Account,Type,Amount,Note
1000 - Sales,Credit,15400.00,Q2 Gross Sales
7100 - Rent,Debit,2400.00,Office rent
7300 - Marketing,Debit,1250.00,Online campaigns
7500 - Software,Debit,860.50,Contora subscription
1200 - Bank Current Account,Debit,10550.00,Statement closing balance"""

    # Render an editable multi-line text input prefilled with the default ledger
    user_csv = st.text_area("Edit or paste client ledger rows (CSV format):", value=default_csv, height=150)
    
    # Check if the user clicks the trigger button to evaluate the trial balance
    if st.button("Run Ledger Scan"):
        # Wrap execution in a try block to handle any malformed text errors safely
        try:
            # Convert the raw text data into a structural pandas DataFrame
            df = pd.read_csv(io.StringIO(user_csv))
            # Strip trailing spaces and normalise case on the entry type column
            df['Type'] = df['Type'].str.strip().str.capitalize()
            # Clean numerical entries, forcing invalid text into zero balances
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0.0)
            
            # Sum up every record flagged as a debit entry
            debits = df[df['Type'] == 'Debit']['Amount'].sum()
            # Sum up every record flagged as a credit entry
            credits = df[df['Type'] == 'Credit']['Amount'].sum()
            # Calculate the literal variance between the two sets of totals
            variance = debits - credits
            
            # Split the viewport into two identical horizontal columns
            col1, col2 = st.columns(2)
            # Display the debit sum as a prominent numeric data metric
            col1.metric("Total Debits", f"£{debits:,.2f}")
            # Display the credit sum as a prominent numeric data metric
            col2.metric("Total Credits", f"£{credits:,.2f}")
            
            # Check if the variance exceeds a minor rounding threshold of one penny
            if abs(variance) > 0.01:
                # Render a prominent amber warning alert showing the discrepancy value
                st.warning(f"⚠️ Discrepancy Found: Ledger out of balance by £{abs(variance):,.2f}")
                # Construct a balancing line entry to correct the structural variance
                suspense_row = {
                    'Account': '9999 - Suspense Account',
                    'Type': 'Credit' if variance > 0 else 'Debit',
                    'Amount': abs(variance),
                    'Note': 'Automated correction to balance ledger'
                }
                # Append the balancing row straight into the ledger data frame
                df = pd.concat([df, pd.DataFrame([suspense_row])], ignore_index=True)
                # Render a blue information banner confirming the balancing entry
                st.info("Success: Discrepancy automatically isolated and routed to the Suspense Account.")
            # Execute this block if debits and credits match perfectly
            else:
                # Render a solid green success banner confirming a zero-variance close
                st.success("✅ Perfection: Ledger naturally balances to zero.")
                
            # Render the final data frame onto the page as an interactive table
            st.dataframe(df, use_container_width=True)
        # Handle exceptions if the CSV string cannot be read structurally
        except Exception as e:
            # Display the exact system error text within a red error alert box
            st.error(f"Error parsing data: {e}")

# =====================================================================
# TAB 2: MARGINAL TAX RELIEF CALCULATOR (TPFB MODULE PREP)
# =====================================================================
# Open the context block to render content inside the second tab item
with tab2:
    # Render the structural section title for the tax compliance tool
    st.header("UK Corporation Tax & Marginal Relief Calculator")
    # State the exact legislative framework and year being evaluated
    st.write("Calculates company tax liabilities for the 2026/27 thresholds, including tapered relief between £50,000 and £250,000.")
    
    # Render an interactive numeric slider component to choose profit values
    profit = st.slider("Select Taxable Company Profit:", min_value=10000, max_value=350000, value=120000, step=5000)
    
    # Set the lower boundary threshold for small business profit rates
    lower_limit = 50000
    # Set the upper boundary threshold where the main tax rate is fixed
    upper_limit = 250000
    # Set the fixed fraction required by HMRC to compute marginal taper relief
    fraction = 3 / 200
    
    # Evaluate if profits fall entirely below the small profits threshold
    if profit <= lower_limit:
        # Calculate liability at the preferential small profits rate of 19%
        tax = profit * 0.19
        # Set relief value to zero since no taper calculation applies
        relief = 0.0
        # Assign a clear descriptive label for this specific tax band
        rate_label = "Small Profits Rate (19%)"
    # Evaluate if profits sit at or above the main upper limit
    elif profit >= upper_limit:
        # Calculate liability at the standard main corporate rate of 25%
        tax = profit * 0.25
        # Set relief value to zero since no taper calculation applies
        relief = 0.0
        # Assign a clear descriptive label for this specific tax band
        rate_label = "Main Rate (25%)"
    # Execute this block if profits land inside the tapered relief boundary
    else:
        # Calculate the hypothetical baseline liability at the main 25% rate
        basic_tax = profit * 0.25
        # Compute the precise tapered deduction according to the statutory formula
        relief = (upper_limit - profit) * fraction
        # Subtract the computed relief value from the baseline tax to get net due
        tax = basic_tax - relief
        # Assign a clear descriptive label for this specific tax band
        rate_label = "Marginal Taper Zone"
        
    # Split the viewport layout into three identical horizontal columns
    c1, col2, c3 = st.columns(3)
    # Display what the tax would have been at 25% inside the first metric slot
    c1.metric("Gross Liability (25%)", f"£{profit * 0.25:,.2f}" if profit > lower_limit else "N/A")
    # Display the isolated relief value inside the second horizontal metric slot
    col2.metric("HMRC Marginal Relief", f"£{relief:,.2f}")
    # Display the final net tax due inside the third horizontal metric slot
    c3.metric("Net Tax Due", f"£{tax:,.2f}")
    
    # Render a status ribbon showing the tax band and the calculated effective percentage
    st.info(f"Tax Status: **{rate_label}** | Effective Tax Rate: **{(tax / profit) * 100:.2f}%**")

# =====================================================================
# TAB 3: PROFILE
# =====================================================================
# Open the context block to render content inside the third profile tab
with tab3:
    # Render your full name as the personal header
    st.header("Aayan Surmust")
    # State the exact target apprenticeship role being pursued
    st.write("**Applying for:** Assistant Accounts Apprentice")
    # Present your verified contact details clearly for the recruiter
    st.write("Phone: 07518 064709 | Email: a.surmust@gmail.com")
    # Explain how these engineering projects prepare you for the AAT curriculum
    st.write("Proactively upskilling for AAT Level 3 FAPS and TPFB modules through data engineering applications.")
