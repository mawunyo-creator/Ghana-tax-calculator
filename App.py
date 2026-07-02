import streamlit as st
import pandas as pd
import io
from fpdf import FPDF
def compute_ghana_payroll_taxes(basic_salary, allowances, bonus, overtime, additional_deductions, tier3_rate):
    """
    Computes statutory payroll deductions using standard 2026 GRA tax bands
    and mandatory/voluntary pension deductions.
    """
    mandatory_ssnit = basic_salary * 0.055
    
    raw_tier3_deduction = basic_salary * (tier3_rate / 100.0)
    max_tax_exempt_tier3 = basic_salary * 0.165
    tax_exempt_tier3 = min(raw_tier3_deduction, max_tax_exempt_tier3)
    
    
    total_gross = basic_salary + allowances + bonus + overtime

    chargeable_income = total_gross - mandatory_ssnit - tax_exempt_tier3 - additional_deductions
    chargeable_income = max(0.0, chargeable_income)
    
    gra_tax_bands = [
        ("First Band", 490.0, 0.0),
        ("Next Band", 110.0, 0.05),
        ("Next Band", 130.0, 0.10),
        ("Next Band", 3166.67, 0.175),
        ("Next Band", 11000.0, 0.25),
        ("Next Band", 29603.33, 0.30) 
    ]
    
    tax_paid = 0.0
    remaining_taxable = chargeable_income
    band_breakdown = []
    
    for band_name, band_limit, tax_rate in gra_tax_bands:
        allocated_amount = min(remaining_taxable, band_limit)
        allocated_tax = allocated_amount * tax_rate
        tax_paid += allocated_tax
        remaining_taxable -= allocated_amount
        
        band_breakdown.append({
            "Tax Band Position": band_name,
            "Tax Rate": f"{tax_rate * 100}%",
            "Amount Taxed (GHS)": f"{allocated_amount:.2f}",
            "Tax Paid (GHS)": f"{allocated_tax:.2f}"
        })
        if remaining_taxable <= 0:
            break
            

    if remaining_taxable > 0:
        allocated_tax = remaining_taxable * 0.35
        tax_paid += allocated_tax
        band_breakdown.append({
            "Tax Band Position": "Exceeding Balance",
            "Tax Rate": "35%",
            "Amount Taxed (GHS)": f"{remaining_taxable:.2f}",
            "Tax Paid (GHS)": f"{allocated_tax:.2f}"
        })
        
    total_deductions = mandatory_ssnit + tax_paid + raw_tier3_deduction + additional_deductions
    net_salary = total_gross - total_deductions
    effective_tax_rate = (tax_paid / total_gross * 100) if total_gross > 0 else 0.0
    
    return {
        "gross": total_gross,
        "ssnit": mandatory_ssnit,
        "tier3": raw_tier3_deduction,
        "taxable": chargeable_income,
        "tax": tax_paid,
        "total_deductions": total_deductions,
        "net_salary": net_salary,
        "effective_tax_rate": effective_tax_rate,
        "breakdown": band_breakdown
    }

def generate_csv_report(details):
    df_csv = pd.DataFrame(details["breakdown"])
    return df_csv.to_csv(index=False).encode("utf-8")


def generate_pdf_report(label, details, final_net, tbill):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.cell(200, 10, txt=f"Official Payroll  Report - {label}", ln=1, align="C")
    
    
    pdf.cell(200, 10, txt=f"Total Gross Earnings: GHS {details['gross']:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Mandatory SSNIT Contribution (5.5%): GHS {details['ssnit']:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Pension Plan Savings: GHS {details['tier3']:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Taxable Chargeable Income: GHS {details['taxable']:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Income Tax Paid to GRA (PAYE): GHS {details['tax']:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Total Deductions Applied: GHS {details['total_deductions']:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Effective Income Tax Rate: {details['effective_tax_rate']:.2f}%", ln=1)
    pdf.cell(200, 10, txt=f"Treasury Bill Target: GHS {tbill:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Final Net Take Home: GHS {final_net:.2f}", ln=1)
    
    pdf_output = pdf.output(dest="S")
    if isinstance(pdf_output, str):
        return pdf_output.encode("latin-1")
    return bytes(pdf_output)


st.set_page_config(layout="wide")

st.markdown("<h2 style='text-align: center;'>Ghana Payroll and Tax Calculator</h2>", unsafe_allow_html=True)


def render_payroll_section(key_prefix, layout_title, default_basic):
    st.markdown(f"<h3 style='text-align: center; margin-top: 20px;'>{layout_title}</h3>", unsafe_allow_html=True)
    
    _, center_content, _ = st.columns([0.5, 5, 0.5])
    
    with center_content:
        input_col_left, input_col_right = st.columns(2)
        with input_col_left:
            basic = st.number_input("Input your monthly basic salary", min_value=0.0, value=default_basic, key=f"{key_prefix}_basic")
            allowances = st.number_input("Input your total monthly allowances", min_value=0.0, value=0.0, key=f"{key_prefix}_allowance")
            bonus = st.number_input("Input your monthly bonuses", min_value=0.0, value=0.0, key=f"{key_prefix}_bonus")
        with input_col_right:
            overtime = st.number_input("Input your overtime earnings", min_value=0.0, value=0.0, key=f"{key_prefix}_overtime")
            additional_deductions = st.number_input("Input any additional optional deductions", min_value=0.0, value=0.0, key=f"{key_prefix}_deduct")
            
        st.markdown("<h4 style='text-align: center; margin-top: 30px;'>Investments</h4>", unsafe_allow_html=True)
        investment_col_left, investment_col_right = st.columns(2)
        with investment_col_left:
            tbill_investment = st.number_input("Enter your monthly Treasury Bill savings target", min_value=0.0, value=0.0, key=f"{key_prefix}_tbill")
        with investment_col_right:
            tier3_rate = st.number_input("Enter your voluntary Tier 3 retirement savings rate percentage", min_value=0.0, max_value=16.5, value=0.0, key=f"{key_prefix}_t3")

    results = compute_ghana_payroll_taxes(basic, allowances, bonus, overtime, additional_deductions, tier3_rate)
    final_net_take_home = max(0.0, results["net_salary"] - tbill_investment)


    st.markdown(f"<h4 style='text-align: center; margin-top: 35px;'>{layout_title} Graphical Representation</h4>", unsafe_allow_html=True)
    _, chart_center, _ = st.columns([1.2, 2.6, 1.2])
    with chart_center:
        chart_df = pd.DataFrame(
            [results["gross"], results["ssnit"], results["tax"], final_net_take_home],
            index=["Gross Earnings", "SSNIT (5.5%)", "Income Tax (PAYE)", "Net Take-Home"],
            columns=["Amount (GHS)"]
        )
        st.bar_chart(chart_df, height=280)
    st.markdown(f"<h4 style='text-align: center; margin-top: 35px;'>{layout_title} Deductions and Net Pay Details</h4>", unsafe_allow_html=True)
    _, metric_center, _ = st.columns([0.5, 5, 0.5])
    with metric_center:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Gross Earnings", f"GHS {results['gross']:.2f}")
        m2.metric("Mandatory SSNIT Contribution", f"GHS {results['ssnit']:.2f}")
        m3.metric("Income Tax Paid to GRA", f"GHS {results['tax']:.2f}")
        m4.metric("Final Net Take Home", f"GHS {final_net_take_home:.2f}")
        st.markdown(f"<p style='text-align: center; margin-top: 25px; margin-bottom: 25px; font-size: 1.25em;'>Effective Tax Rate: {results['effective_tax_rate']:.2f}%</p>", unsafe_allow_html=True)

    st.markdown(f"<h4 style='text-align: center; margin-top: 40px; margin-bottom: 20px;'>{layout_title} Expenses and Estimates</h4>", unsafe_allow_html=True)
    _, pocket_center, _ = st.columns([0.5, 5, 0.5])
    with pocket_center:
        pane_left, _, pane_right = st.columns([2.5, 0.5, 2.5])
        with pane_left:
            st.markdown("<h5 style='text-align: left; margin-bottom: 15px;'>Take-Home Pay Summary</h5>", unsafe_allow_html=True)
            st.markdown(f"<p style='line-height: 2.0; margin-bottom: 10px;'>Final Net Take Home: GHS {final_net_take_home:.2f}</p>", unsafe_allow_html=True)
            if results["gross"] > 0:
                retention_percentage = (final_net_take_home / results["gross"]) * 100
                st.markdown(f"<p style='line-height: 2.0;'>You get to keep {retention_percentage:.1f}% of everything you earned.</p>", unsafe_allow_html=True)
        with pane_right:
            st.markdown("<h5 style='text-align: left; margin-bottom: 15px;'>Your Total Savings Breakdown</h5>", unsafe_allow_html=True)
            st.markdown(f"<p style='line-height: 2.0; margin-bottom: 10px;'>Pension Plan Savings: GHS {results['tier3']:.2f}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='line-height: 2.0;'>Treasury Bill Investment Amount: GHS {tbill_investment:.2f}</p>", unsafe_allow_html=True)
            
        export_col_1, _, export_col_2, _ = st.columns([1.5, 1.0, 1.5, 1.0])
        with export_col_1:
            csv_data = generate_csv_report(results)
            st.download_button(label="Download CSV Report", data=csv_data, file_name=f"{key_prefix}_salary_payroll_report.csv", mime="text/csv", use_container_width=True)
        with export_col_2:
            pdf_data = generate_pdf_report(layout_title, results, final_net_take_home, tbill_investment)
            st.download_button(label="Download PDF Report", data=pdf_data, file_name=f"{key_prefix}_salary_payroll_report.pdf", mime="application/pdf", use_container_width=True)

render_payroll_section("primary", "Primary Salary Details", 3000.0)
render_payroll_section("alternative", "Alternative Salary Details", 4000.0)


st.markdown("<h3 style='text-align: center;'>Official Ghana Income Tax Rates</h3>", unsafe_allow_html=True)

_, table_center, _ = st.columns([0.5, 5, 0.5])
with table_center:
    official_tax_bands_data = [
        {"Tax Band Position": "First Band", "Chargeable Income Amount (GHS)": "490.00", "Tax Rate Percentage": "0% / Free"},
        {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "110.00", "Tax Rate Percentage": "5%"},
        {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "130.00", "Tax Rate Percentage": "10%"},
        {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "3,166.67", "Tax Rate Percentage": "17.5%"},
        {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "11,000.00", "Tax Rate Percentage": "25%"},
        {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "29,603.33", "Tax Rate Percentage": "30%"},
        {"Tax Band Position": "Exceeding Balance", "Chargeable Income Amount (GHS)": "Above 45,000.00", "Tax Rate Percentage": "35%"}
    ]
    st.table(official_tax_bands_data)

st.divider()

st.caption("Regulatory & Legal Source Attribution Statement:")

st.caption(
    "This progressive personal income tax bands, Pay-As-You-Earn (PAYE) rules, "
    "and statutory pension deduction percentages utilize the official statutory "
    "schedules published by the Ghana Revenue Authority (GRA)."
)

st.caption("Access & Verification Reference Date: May 2026.")

st.caption(
    "Operational Prototype Disclaimer: This web application is intended for "
    "informational purposes only and does not constitute formal tax advice."
)