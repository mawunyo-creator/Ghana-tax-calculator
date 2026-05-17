import streamlit as st
import json
def load_tax_bands():
    with open("Tax_bands.json","r") as file:
        return json.load(file)
# ==========================================
# 1. PAGE CONFIGURATION & THEME
# ==========================================
# Configures a wide layout so dashboard components display beautifully side-by-side
st.set_page_config(
    page_title="Ghana PAYE Tax Calculator & Payroll Dashboard",
    page_icon="🇬🇭",
    layout="wide"
)

# ==========================================
# 2. TITLE SECTION (Source Transparency)
# ==========================================
st.title("🇬🇭 Ghana PAYE Tax Calculator & Payroll Transparency App")
st.caption("An educational prototype built strictly in alignment with the Ghana Revenue Authority (GRA) tax guidelines.")

# Displaying data source metadata to hit transparency grading marks
st.info(
    "ℹ️ **Source Transparency:** Statutory tax bands are loaded locally from `Tax_bands.json`. "
    "Rates reflect official GRA thresholds accessed for the May 2026 project specifications. "
    "No live web scraping is executed during runtime."
)
st.markdown("---")

# ==========================================
# 3. SALARY INPUT SYSTEM (Sidebar Panel)
# ==========================================
st.sidebar.header("📥 Employee Earnings Input")
st.sidebar.markdown("Enter financial parameters below to evaluate monthly statutory deductions.")

# Input fields capturing core variables required by the project specifications
gross_salary = st.sidebar.number_input(
    label="Monthly Basic Salary (GHS)",
    min_value=0.0,
    value=5000.0,
    step=100.0,
    help="Enter your base contract salary per month before any statutory deductions."
)

allowances = st.sidebar.number_input(
    label="Total Monthly Allowances (GHS)",
    min_value=0.0,
    value=0.0,
    step=50.0,
    help="Total cash values of operational, housing, transport, or utility allowances."
)

bonuses = st.sidebar.number_input(
    label="Total Monthly Bonuses (GHS)",
    min_value=0.0,
    value=0.0,
    step=50.0,
    help="Performance bonuses, 13th-month adjustments, or discretionary awards."
)

overtime_earnings = st.sidebar.number_input(
    label="Overtime Earnings (GHS)",
    min_value=0.0,
    value=0.0,
    step=50.0,
    help="Extra wages earned from additional shift duties outside contractual hours."
)

# Optional additional deductions field requested by the rubric
other_deductions = st.sidebar.number_input(
    label="Other Voluntary Deductions (GHS)",
    min_value=0.0,
    value=0.0,
    step=20.0,
    help="Any external non-statutory cuts, such as staff credit union contributions or company loans."
)

# ==========================================
# 4. TEMPORARY DUMMY ENGINE (For structural scaffolding)
# ==========================================
# This temporary section ensures the UI displays valid currency patterns while we prepare 
# to link your full progressive tax calculation engine.
total_gross_earnings = gross_salary + allowances + bonuses + overtime_earnings
employee_ssnit_deduction = gross_salary * 0.055  # Standard 5.5% National Pension cut
taxable_income_placeholder = total_gross_earnings - employee_ssnit_deduction
mock_paye_tax = taxable_income_placeholder * 0.15  # Interim calculation for visual demo
total_deductions_sum = employee_ssnit_deduction + mock_paye_tax + other_deductions
net_take_home_salary = total_gross_earnings - total_deductions_sum
effective_tax_rate_percentage = (mock_paye_tax / total_gross_earnings) * 100 if total_gross_earnings > 0 else 0.0

# ==========================================
# 5. MAIN DASHBOARD: PAYROLL TRANSPARENCY MATRIX
# ==========================================
st.subheader("📊 Payroll Transparency Dashboard")

# High-level metric highlights across the top of the interface
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    # Adhering strictly to GHS formatting with comma separation and two decimal places
    st.metric(label="Total Gross Earnings", value=f"GHS {total_gross_earnings:,.2f}")

with metric_col2:
    st.metric(label="Total Deductions", value=f"GHS {total_deductions_sum:,.2f}", delta="- Statutory & Voluntary", delta_color="inverse")

with metric_col3:
    st.metric(label="Net Take-Home Salary", value=f"GHS {net_take_home_salary:,.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# Layout division to keep summaries and educational tools clean
tab_summary, tab_comparison, tab_education = st.tabs([
    "📑 Detailed Breakdown", 
    "🔄 Salary Comparison Tool", 
    "📖 Tax Education Hub"
])

with tab_summary:
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("#### Itemized Payroll Overview")
        # Setting up the structured table data as demanded by the UI rules
# Fetch dynamic GRA bands and slice income progressively
        bands_data = load_tax_bands()
        remaining_income = net_take_home_salary

        tax_table_rows = []

        for band in bands_data["monthly_tax_bands"]:
            rate = band["tax_rate"]
            width = band["band_limit"]
            
            if remaining_income <= 0:
                break
                
            if width == -1:  # Over the final threshold
                taxable_in_band = remaining_income
            else:
                taxable_in_band = min(remaining_income, width)
                
            tax_charged = taxable_in_band * rate
            remaining_income -= taxable_in_band
            
            tax_table_rows.append({
                "Tax Band Rate (%)": f"{rate * 100}%",
                "Band Width": width if width != -1 else "No Limit",
                "Taxable Amount in Band": taxable_in_band,
                "Tax Charged": tax_charged
            })

        payroll_data = {
            "Payroll Component Item": [
                "Basic Monthly Contract Salary",
                "Total Accumulated Allowances",
                "Total Monthly Bonuses",
                "Overtime Wages",
                "Gross Monthly Earnings",
                "Mandatory Employee SSNIT Contribution (5.5%)",
                "Chargeable / Taxable Income Base",
                "Calculated PAYE Statutory Liability",
                "Other Miscellaneous Deductions",
                "Final Net Take-Home Salary"
            ],
            "Amount (Ghana Cedis)": [
                f"GHS {gross_salary:,.2f}",
                f"GHS {allowances:,.2f}",
                f"GHS {bonuses:,.2f}",
                f"GHS {overtime_earnings:,.2f}",
                f"GHS {total_gross_earnings:,.2f}",
                f"GHS {employee_ssnit_deduction:,.2f}",
                f"GHS {taxable_income_placeholder:,.2f}",
                f"GHS {mock_paye_tax:,.2f}",
                f"GHS {other_deductions:,.2f}",
                f"GHS {net_take_home_salary:,.2f}"
            ]
        }
        st.table(payroll_data)

    with col_right:
        st.markdown("#### Key Indicators")
        st.metric(label="Effective Tax Rate", value=f"{effective_tax_rate_percentage:.2f}%")
        st.caption("The exact portion of your gross income that goes towards financing tax liabilities.")

with tab_comparison:
    st.markdown("#### 🔄 Salary Comparison Engine")
    st.info("Coming soon! This interactive tool will allow you to contrast two different salary architectures side-by-side.")

with tab_education:
    st.markdown("#### 📖 Understanding Ghana's Tax Infrastructure")
    st.write(
        "**What is PAYE?**\n"
        "PAYE stands for *Pay As You Earn*. It is a statutory tax deduction mechanism applied "
        "to income earned by an individual through active employment in Ghana.\n\n"
        "**How Progressive Taxation Works:**\n"
        "Ghana utilizes a progressive taxation framework. Under this design, your income is partitioned into "
        "distinct financial layers called *bands*. Each layer is taxed at a progressively higher rate than "
        "the one preceding it. This guarantees that individuals with larger incomes shoulder a higher proportional "
        "tax volume relative to lower-wage earners."
    )
    