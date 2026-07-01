import streamlit as st
import pandas as pd
from fpdf import FPDF

def compute_ghana_payroll_taxes(basic_salary, allowances, bonus, overtime, additional_deductions, tier3_rate):
    mandatory_ssnit = basic_salary * 0.055
    
    raw_tier3_deduction = basic_salary * (tier3_rate / 100.0)
    max_tax_exempt_tier3 = basic_salary * 0.165
    tax_exempt_tier3 = min(raw_tier3_deduction, max_tax_exempt_tier3)
    
    total_gross = basic_salary + allowances + bonus + overtime
    chargeable_income = max(0.0, total_gross - mandatory_ssnit - tax_exempt_tier3 - additional_deductions)
    
    gra_tax_bands = [
        ("First Band", 490.0, 0.0),
        ("Next Band", 110.0, 0.05),
        ("Next Band", 130.0, 0.10),
        ("Next Band", 3166.67, 0.175),
        ("Next Band", 11000.0, 0.25)
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
        allocated_tax = remaining_taxable * 0.30
        tax_paid += allocated_tax
        band_breakdown.append({
            "Tax Band Position": "Exceeding Balance",
            "Tax Rate": "30%",
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

def generate_pdf_report(details, final_net, tbill):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, "Official Payroll Computation Report", 0, 1, "C")
    pdf.cell(200, 10, "-------------------------------------------------------------------------", 0, 1, "C")
    pdf.cell(200, 10, f"Total Gross Earnings: GHS {details['gross']:.2f}", 0, 1)
    pdf.cell(200, 10, f"Mandatory SSNIT Contribution (5.5%): GHS {details['ssnit']:.2f}", 0, 1)
    pdf.cell(200, 10, f"Pension Plan Savings (Tier 3): GHS {details['tier3']:.2f}", 0, 1)
    pdf.cell(200, 10, f"Taxable Chargeable Income: GHS {details['taxable']:.2f}", 0, 1)
    pdf.cell(200, 10, f"Income Tax Paid to GRA (PAYE): GHS {details['tax']:.2f}", 0, 1)
    pdf.cell(200, 10, f"Total Deductions Applied: GHS {details['total_deductions']:.2f}", 0, 1)
    pdf.cell(200, 10, f"Effective Income Tax Rate: {details['effective_tax_rate']:.2f}%", 0, 1)
    pdf.cell(200, 10, f"Short Term Treasury Bill Target: GHS {tbill:.2f}", 0, 1)
    pdf.cell(200, 10, f"Final Net Take Home: GHS {final_net:.2f}", 0, 1)
    
    pdf_output = pdf.output(dest="S")
    if isinstance(pdf_output, str):
        return pdf_output.encode("latin-1")
    return bytes(pdf_output)

st.set_page_config(layout="wide")
st.title("Ghana Payroll and Tax Calculator")
st.write("Calculate monthly statutory basic salary deductions and net take-home pay.")

input_col_left, input_col_right = st.columns(2)
with input_col_left:
    basic = st.number_input("Monthly Basic Salary (GHS)", min_value=0.0, value=3000.0)
    allowances = st.number_input("Total Monthly Allowances (GHS)", min_value=0.0, value=0.0)
    bonus = st.number_input("Monthly Bonuses (GHS)", min_value=0.0, value=0.0)
with input_col_right:
    overtime = st.number_input("Overtime Earnings (GHS)", min_value=0.0, value=0.0)
    additional_deductions = st.number_input("Other Optional Deductions (GHS)", min_value=0.0, value=0.0)
    tier3_rate = st.number_input("Voluntary Tier 3 Savings Rate (%)", min_value=0.0, max_value=16.5, value=0.0)

st.write("Investment Targets")
tbill_investment = st.number_input("Monthly Treasury Bill Target (GHS)", min_value=0.0, value=0.0)

results = compute_ghana_payroll_taxes(basic, allowances, bonus, overtime, additional_deductions, tier3_rate)
final_net_take_home = max(0.0, results["net_salary"] - tbill_investment)

st.write("Graphical Representation")
chart_data = {"Amount (GHS)": [results["gross"], results["ssnit"], results["tax"], final_net_take_home]}
st.bar_chart(data=chart_data, y="Amount (GHS)", height=280)

st.write("Deductions and Net Pay Details")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Gross Earnings", f"GHS {results['gross']:.2f}")
m2.metric("Mandatory SSNIT", f"GHS {results['ssnit']:.2f}")
m3.metric("Income Tax (GRA PAYE)", f"GHS {results['tax']:.2f}")
m4.metric("Final Net Take Home", f"GHS {final_net_take_home:.2f}")

st.write(f"Effective Tax Rate: {results['effective_tax_rate']:.2f}%")

export_col_1, export_col_2 = st.columns(2)
with export_col_1:
    csv_data = generate_csv_report(results)
    st.download_button(label="Download CSV Report", data=csv_data, file_name="payroll_report.csv", mime="text/csv")
with export_col_2:
    pdf_data = generate_pdf_report(results, final_net_take_home, tbill_investment)
    st.download_button(label="Download PDF Report", data=pdf_data, file_name="payroll_report.pdf", mime="application/pdf")

st.write(" Official Ghana Income Tax Rates")
official_tax_bands_data = [
    {"Tax Band Position": "First Band", "Chargeable Income Amount (GHS)": "490.00", "Tax Rate Percentage": "0% / Free"},
    {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "110.00", "Tax Rate Percentage": "5%"},
    {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "130.00", "Tax Rate Percentage": "10%"},
    {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "3,166.67", "Tax Rate Percentage": "17.5%"},
    {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "11,000.00", "Tax Rate Percentage": "25%"},
    {"Tax Band Position": "Exceeding Balance", "Chargeable Income Amount (GHS)": "Above 15,396.67", "Tax Rate Percentage": "30%"}
]
st.table(official_tax_bands_data)

st.write("Tax Information & Education")
st.write("PAYE stands for Pay As You Earn. It is the system used by the Ghana Revenue Authority to calculate income tax on what you earn from your job. This is a progressive tax system, which means your tax rate goes up as you earn more money. Your income is broken down into separate blocks or bands, and each block is taxed at its own matching rate.")

st.write("Under Ghanaian labor laws, your employer takes a mandatory 5.5 percent out of your basic salary and sends it straight to SSNIT to fund your main retirement pension. If you choose to put money into an approved voluntary Tier 3 pension plan, you get special tax breaks. You are allowed to set aside up to 16.5 percent of your basic salary completely tax-free. This money is taken out first, lowering the amount of income that the GRA can actually touch with tax percentages.")

st.write("All tax bands and tax percentages used in this calculation app are taken directly from the official website and public guidelines of the Ghana Revenue Authority.")

st.caption("Regulatory & Legal Source Attribution Statement: The progressive personal income tax bands, Pay-As-You-Earn (PAYE) calculation variables, and Tier 1/2/3 statutory pension deduction percentages utilized within this application engine are derived from the official statutory schedules published by the Ghana Revenue Authority (GRA). Data Access Reference: 2026.")
st.caption("Educational Prototype Disclaimer: This web application is developed strictly as an academic engineering project prototype. It does not constitute formal financial, legal, or professional tax accounting advice. All calculations are for educational transparency and demonstration purposes only.")