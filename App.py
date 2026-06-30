import streamlit as st
import io
from fpdf import FPDF

def calculate_primary_payroll_details(primary_basic_salary, primary_allowances, primary_bonus, primary_overtime, primary_additional_deductions, primary_tier3_percentage):
    primary_ssnit_mandatory = primary_basic_salary * 0.055
    
    primary_tier3_decimal = primary_tier3_percentage / 100.0
    primary_tier3_deduction = primary_basic_salary * primary_tier3_decimal
    
    primary_max_tax_free_tier3 = primary_basic_salary * 0.165
    if primary_tier3_deduction > primary_max_tax_free_tier3:
        primary_tax_exempt_tier3 = primary_max_tax_free_tier3
    else:
        primary_tax_exempt_tier3 = primary_tier3_deduction
        
    primary_total_gross = primary_basic_salary + primary_allowances + primary_bonus + primary_overtime
    
    primary_chargeable_income = primary_total_gross - primary_ssnit_mandatory - primary_tax_exempt_tier3 - primary_additional_deductions
    if primary_chargeable_income < 0:
        primary_chargeable_income = 0.0
        
    primary_tax_paid = 0.0
    primary_remaining_income = primary_chargeable_income
    
    primary_tax_bands = [
        ("First Band", 490.0, 0.0),
        ("Next Band", 110.0, 0.05),
        ("Next Band", 130.0, 0.10),
        ("Next Band", 3166.67, 0.175),
        ("Next Band", 11000.0, 0.25)
    ]
    
    primary_band_breakdown = []
    
    for primary_band_name, primary_band_limit, primary_tax_rate in primary_tax_bands:
        if primary_remaining_income > primary_band_limit:
            primary_allocated_amount = primary_band_limit
            primary_allocated_tax = primary_band_limit * primary_tax_rate
            primary_tax_paid += primary_allocated_tax
            primary_remaining_income -= primary_band_limit
        else:
            primary_allocated_amount = primary_remaining_income
            primary_allocated_tax = primary_remaining_income * primary_tax_rate
            primary_tax_paid += primary_allocated_tax
            primary_remaining_income = 0.0
            
        primary_band_breakdown.append({
            "Tax Band Position": primary_band_name,
            "Tax Rate": f"{primary_tax_rate * 100}%",
            "Amount Taxed (GHS)": f"{primary_allocated_amount:.2f}",
            "Tax Paid (GHS)": f"{primary_allocated_tax:.2f}"
        })
        
        if primary_remaining_income == 0.0:
            break
            
    if primary_remaining_income > 0:
        primary_allocated_tax = primary_remaining_income * 0.30
        primary_tax_paid += primary_allocated_tax
        primary_band_breakdown.append({
            "Tax Band Position": "Exceeding Balance",
            "Tax Rate": "30%",
            "Amount Taxed (GHS)": f"{primary_remaining_income:.2f}",
            "Tax Paid (GHS)": f"{primary_allocated_tax:.2f}"
        })
        
    primary_total_deductions = primary_ssnit_mandatory + primary_tax_paid + primary_tier3_deduction + primary_additional_deductions
    primary_net_salary = primary_total_gross - primary_total_deductions
    
    primary_effective_tax_rate = (primary_tax_paid / primary_total_gross * 100) if primary_total_gross > 0 else 0.0
    
    return {
        "primary_gross": primary_total_gross,
        "primary_ssnit": primary_ssnit_mandatory,
        "primary_tier3": primary_tier3_deduction,
        "primary_taxable": primary_chargeable_income,
        "primary_tax": primary_tax_paid,
        "primary_total_deductions": primary_total_deductions,
        "primary_net_salary": primary_net_salary,
        "primary_effective_tax_rate": primary_effective_tax_rate,
        "primary_breakdown_table": primary_band_breakdown
    }

def calculate_alternative_payroll_details(alternative_basic_salary, alternative_allowances, alternative_bonus, alternative_overtime, alternative_additional_deductions, alternative_tier3_percentage):
    alternative_ssnit_mandatory = alternative_basic_salary * 0.055
    
    alternative_tier3_decimal = alternative_tier3_percentage / 100.0
    alternative_tier3_deduction = alternative_basic_salary * alternative_tier3_decimal
    
    alternative_max_tax_free_tier3 = alternative_basic_salary * 0.165
    if alternative_tier3_deduction > alternative_max_tax_free_tier3:
        alternative_tax_exempt_tier3 = alternative_max_tax_free_tier3
    else:
        alternative_tax_exempt_tier3 = alternative_tier3_deduction
        
    alternative_total_gross = alternative_basic_salary + alternative_allowances + alternative_bonus + alternative_overtime
    
    alternative_chargeable_income = alternative_total_gross - alternative_ssnit_mandatory - alternative_tax_exempt_tier3 - alternative_additional_deductions
    if alternative_chargeable_income < 0:
        alternative_chargeable_income = 0.0
        
    alternative_tax_paid = 0.0
    alternative_remaining_income = alternative_chargeable_income
    
    alternative_tax_bands = [
        ("First Band", 490.0, 0.0),
        ("Next Band", 110.0, 0.05),
        ("Next Band", 130.0, 0.10),
        ("Next Band", 3166.67, 0.175),
        ("Next Band", 11000.0, 0.25)
    ]
    
    alternative_band_breakdown = []
    
    for alternative_band_name, alternative_band_limit, alternative_tax_rate in alternative_tax_bands:
        if alternative_remaining_income > alternative_band_limit:
            alternative_allocated_amount = alternative_band_limit
            alternative_allocated_tax = alternative_band_limit * alternative_tax_rate
            alternative_tax_paid += alternative_allocated_tax
            alternative_remaining_income -= alternative_band_limit
        else:
            alternative_allocated_amount = alternative_remaining_income
            alternative_allocated_tax = alternative_remaining_income * alternative_tax_rate
            alternative_tax_paid += alternative_allocated_tax
            alternative_remaining_income = 0.0
            
        alternative_band_breakdown.append({
            "Tax Band Position": alternative_band_name,
            "Tax Rate": f"{alternative_tax_rate * 100}%",
            "Amount Taxed (GHS)": f"{alternative_allocated_amount:.2f}",
            "Tax Paid (GHS)": f"{alternative_allocated_tax:.2f}"
        })
        
        if alternative_remaining_income == 0.0:
            break
            
    if alternative_remaining_income > 0:
        alternative_allocated_tax = alternative_remaining_income * 0.30
        alternative_tax_paid += alternative_allocated_tax
        alternative_band_breakdown.append({
            "Tax Band Position": "Exceeding Balance",
            "Tax Rate": "30%",
            "Amount Taxed (GHS)": f"{alternative_remaining_income:.2f}",
            "Tax Paid (GHS)": f"{alternative_allocated_tax:.2f}"
        })
        
    alternative_total_deductions = alternative_ssnit_mandatory + alternative_tax_paid + alternative_tier3_deduction + alternative_additional_deductions
    alternative_net_salary = alternative_total_gross - alternative_total_deductions
    
    alternative_effective_tax_rate = (alternative_tax_paid / alternative_total_gross * 100) if alternative_total_gross > 0 else 0.0
    
    return {
        "alternative_gross": alternative_total_gross,
        "alternative_ssnit": alternative_ssnit_mandatory,
        "alternative_tier3": alternative_tier3_deduction,
        "alternative_taxable": alternative_chargeable_income,
        "alternative_tax": alternative_tax_paid,
        "alternative_total_deductions": alternative_total_deductions,
        "alternative_net_salary": alternative_net_salary,
        "alternative_effective_tax_rate": alternative_effective_tax_rate,
        "alternative_breakdown_table": alternative_band_breakdown
    }

def generate_primary_csv_report(primary_details, primary_final_net_take_home, primary_tbill):
    primary_output = io.StringIO()
    primary_output.write("Payroll Report for Primary Salary Layout\n")
    primary_output.write(f"Total Gross Earnings (GHS),{primary_details['primary_gross']:.2f}\n")
    primary_output.write(f"Mandatory SSNIT Contribution (GHS),{primary_details['primary_ssnit']:.2f}\n")
    primary_output.write(f"Pension Plan Savings (GHS),{primary_details['primary_tier3']:.2f}\n")
    primary_output.write(f"Taxable Chargeable Income (GHS),{primary_details['primary_taxable']:.2f}\n")
    primary_output.write(f"Income Tax Paid to GRA (GHS),{primary_details['primary_tax']:.2f}\n")
    primary_output.write(f"Total Deductions (GHS),{primary_details['primary_total_deductions']:.2f}\n")
    primary_output.write(f"Effective Tax Rate (%),{primary_details['primary_effective_tax_rate']:.2f}\n")
    primary_output.write(f"Treasury Bill Investment Target (GHS),{primary_tbill:.2f}\n")
    primary_output.write(f"Final Net Take Home (GHS),{primary_final_net_take_home:.2f}\n")
    return primary_output.getvalue()

def generate_alternative_csv_report(alternative_details, alternative_final_net_take_home, alternative_tbill):
    alternative_output = io.StringIO()
    alternative_output.write("Payroll Report for Alternative Salary Layout\n")
    alternative_output.write(f"Total Gross Earnings (GHS),{alternative_details['alternative_gross']:.2f}\n")
    alternative_output.write(f"Mandatory SSNIT Contribution (GHS),{alternative_details['alternative_ssnit']:.2f}\n")
    alternative_output.write(f"Pension Plan Savings (GHS),{alternative_details['alternative_tier3']:.2f}\n")
    alternative_output.write(f"Taxable Chargeable Income (GHS),{alternative_details['alternative_taxable']:.2f}\n")
    alternative_output.write(f"Income Tax Paid to GRA (GHS),{alternative_details['alternative_tax']:.2f}\n")
    alternative_output.write(f"Total Deductions (GHS),{alternative_details['alternative_total_deductions']:.2f}\n")
    alternative_output.write(f"Effective Tax Rate (%),{alternative_details['alternative_effective_tax_rate']:.2f}\n")
    alternative_output.write(f"Treasury Bill Investment Target (GHS),{alternative_tbill:.2f}\n")
    alternative_output.write(f"Final Net Take Home (GHS),{alternative_final_net_take_home:.2f}\n")
    return alternative_output.getvalue()

def generate_primary_pdf_report(primary_details, primary_final_net_take_home, primary_tbill):
    primary_pdf = FPDF()
    primary_pdf.add_page()
    primary_pdf.set_font("Arial", size=12)
    
    primary_pdf.cell(200, 10, txt="Official Payroll Computation Report - Primary Salary Layout", ln=1, align="C")
    primary_pdf.cell(200, 10, txt=f"Total Gross Earnings: GHS {primary_details['primary_gross']:.2f}", ln=1)
    primary_pdf.cell(200, 10, txt=f"Mandatory SSNIT Contribution (5.5%): GHS {primary_details['primary_ssnit']:.2f}", ln=1)
    primary_pdf.cell(200, 10, txt=f"Pension Plan Savings: GHS {primary_details['primary_tier3']:.2f}", ln=1)
    primary_pdf.cell(200, 10, txt=f"Taxable Chargeable Income: GHS {primary_details['primary_taxable']:.2f}", ln=1)
    primary_pdf.cell(200, 10, txt=f"Income Tax Paid to GRA (PAYE): GHS {primary_details['primary_tax']:.2f}", ln=1)
    primary_pdf.cell(200, 10, txt=f"Total Deductions Applied: GHS {primary_details['primary_total_deductions']:.2f}", ln=1)
    primary_pdf.cell(200, 10, txt=f"Effective Income Tax Rate: {primary_details['primary_effective_tax_rate']:.2f}%", ln=1)
    primary_pdf.cell(200, 10, txt=f"Short Term Treasury Bill Target: GHS {primary_tbill:.2f}", ln=1)
    primary_pdf.cell(200, 10, txt=f"Final Net Take Home: GHS {primary_final_net_take_home:.2f}", ln=1)
    
    return primary_pdf.output(dest="S").encode("latin-1")

def generate_alternative_pdf_report(alternative_details, alternative_final_net_take_home, alternative_tbill):
    alternative_pdf = FPDF()
    alternative_pdf.add_page()
    alternative_pdf.set_font("Arial", size=12)
    
    alternative_pdf.cell(200, 10, txt="Official Payroll Computation Report - Alternative Salary Layout", ln=1, align="C")
    alternative_pdf.cell(200, 10, txt=f"Total Gross Earnings: GHS {alternative_details['alternative_gross']:.2f}", ln=1)
    alternative_pdf.cell(200, 10, txt=f"Mandatory SSNIT Contribution (5.5%): GHS {alternative_details['alternative_ssnit']:.2f}", ln=1)
    alternative_pdf.cell(200, 10, txt=f"Pension Plan Savings: GHS {alternative_details['alternative_tier3']:.2f}", ln=1)
    alternative_pdf.cell(200, 10, txt=f"Taxable Chargeable Income: GHS {alternative_details['alternative_taxable']:.2f}", ln=1)
    alternative_pdf.cell(200, 10, txt=f"Income Tax Paid to GRA (PAYE): GHS {alternative_details['alternative_tax']:.2f}", ln=1)
    alternative_pdf.cell(200, 10, txt=f"Total Deductions Applied: GHS {alternative_details['alternative_total_deductions']:.2f}", ln=1)
    alternative_pdf.cell(200, 10, txt=f"Effective Income Tax Rate: {alternative_details['alternative_effective_tax_rate']:.2f}%", ln=1)
    alternative_pdf.cell(200, 10, txt=f"Short Term Treasury Bill Target: GHS {alternative_tbill:.2f}", ln=1)
    alternative_pdf.cell(200, 10, txt=f"Final Net Take Home: GHS {alternative_final_net_take_home:.2f}", ln=1)
    
    return alternative_pdf.output(dest="S").encode("latin-1")

st.set_page_config(layout="wide")

st.markdown("<h2 style='text-align: center;'>Ghana Payroll and Tax Calculator</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Find out your correct basic salary deductions and your final cash out.</p>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>Primary Salary Details</h3>", unsafe_allow_html=True)

primary_left_spacer, primary_center_content, primary_right_spacer = st.columns([0.5, 5, 0.5])

with primary_center_content:
    primary_input_column_left, primary_input_column_right = st.columns(2)
    
    with primary_input_column_left:
        primary_basic_salary = st.number_input("Input your monthly basic salary here", min_value=0.0, value=3000.0, key="primary_b1")
        primary_allowances = st.number_input("Input your total monthly allowances here", min_value=0.0, value=0.0, key="primary_a1")
        primary_bonus = st.number_input("Input your monthly bonuses here", min_value=0.0, value=0.0, key="primary_bo1")
        
    with primary_input_column_right:
        primary_overtime = st.number_input("Input your overtime earnings here", min_value=0.0, value=0.0, key="primary_o1")
        primary_additional_deductions = st.number_input("Input any additional optional deductions here", min_value=0.0, value=0.0, key="primary_d1")
        
    st.markdown("<h4 style='text-align: center; margin-top: 30px;'>Investments</h4>", unsafe_allow_html=True)
    
    primary_investment_column_left, primary_investment_column_right = st.columns(2)
    
    with primary_investment_column_left:
        primary_tbill_investment = st.number_input("Enter your monthly Treasury Bill savings target", min_value=0.0, value=0.0, key="primary_t1")
        
    with primary_investment_column_right:
        primary_tier3_rate = st.number_input("Enter your voluntary Tier 3 retirement savings rate percentage", min_value=0.0, max_value=16.5, value=0.0, key="primary_tr1")

primary_payroll_results = calculate_primary_payroll_details(primary_basic_salary, primary_allowances, primary_bonus, primary_overtime, primary_additional_deductions, primary_tier3_rate)

primary_final_net_take_home = primary_payroll_results["primary_net_salary"] - primary_tbill_investment
if primary_final_net_take_home < 0:
    primary_final_net_take_home = 0.0

st.markdown("<h4 style='text-align: center; margin-top: 35px;'>Primary Salary Graphical Representation</h4>", unsafe_allow_html=True)
primary_chart_left, primary_chart_center, primary_chart_right = st.columns([1.2, 2.6, 1.2])

with primary_chart_center:
    primary_vertical_chart_data = {
        "Amount (GHS)": [
            primary_payroll_results["primary_gross"], 
            primary_payroll_results["primary_ssnit"], 
            primary_payroll_results["primary_tax"], 
            primary_final_net_take_home
        ]
    }
    st.bar_chart(data=primary_vertical_chart_data, y="Amount (GHS)", height=280)

st.markdown("<h4 style='text-align: center; margin-top: 35px;'>Primary Salary Deductions and Net Pay Details</h4>", unsafe_allow_html=True)
primary_metric_left, primary_metric_center, primary_metric_right = st.columns([0.5, 5, 0.5])

with primary_metric_center:
    primary_metric_column_one, primary_metric_column_two, primary_metric_column_three, primary_metric_column_four = st.columns(4)
    with primary_metric_column_one:
        st.metric("Total Gross Earnings", f"GHS {primary_payroll_results['primary_gross']:.2f}")
    with primary_metric_column_two:
        st.metric("Mandatory SSNIT Contribution", f"GHS {primary_payroll_results['primary_ssnit']:.2f}")
    with primary_metric_column_three:
        st.metric("Income Tax Paid to GRA", f"GHS {primary_payroll_results['primary_tax']:.2f}")
    with primary_metric_column_four:
        st.metric("Final Net Take Home", f"GHS {primary_final_net_take_home:.2f}")
        
    st.markdown(f"<p style='text-align: center; margin-top: 25px; margin-bottom: 25px; font-size: 1.25em;'>Effective Tax Rate: {primary_payroll_results['primary_effective_tax_rate']:.2f}%</p>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; margin-top: 40px; margin-bottom: 20px;'>Primary Salary Expenses and Estimates</h4>", unsafe_allow_html=True)
primary_pocket_left, primary_pocket_center, primary_pocket_right = st.columns([0.5, 5, 0.5])

with primary_pocket_center:
    primary_pocket_left_pane, primary_space_buffer, primary_pocket_right_pane = st.columns([2.5, 0.5, 2.5])
    with primary_pocket_left_pane:
        st.markdown("<h5 style='text-align: left; margin-bottom: 15px;'>Take-Home Pay Summary</h5>", unsafe_allow_html=True)
        st.markdown(f"<p style='line-height: 2.0; margin-bottom: 10px;'>Final Net Take Home: GHS {primary_final_net_take_home:.2f}</p>", unsafe_allow_html=True)
        if primary_payroll_results["primary_gross"] > 0:
            primary_retention_percentage = (primary_final_net_take_home / primary_payroll_results["primary_gross"]) * 100
            st.markdown(f"<p style='line-height: 2.0;'>You get to keep {primary_retention_percentage:.1f}% of everything you earned.</p>", unsafe_allow_html=True)
            
    with primary_pocket_right_pane:
        st.markdown("<h5 style='text-align: left; margin-bottom: 15px;'>Your Total Savings Breakdown</h5>", unsafe_allow_html=True)
        st.markdown(f"<p style='line-height: 2.0; margin-bottom: 10px;'>Pension Plan Savings: GHS {primary_payroll_results['primary_tier3']:.2f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='line-height: 2.0;'>Treasury Bill Investment Amount: GHS {primary_tbill_investment:.2f}</p>", unsafe_allow_html=True)
        
    primary_export_col_1, primary_spacer_btn_1, primary_export_col_2, primary_spacer_btn_2 = st.columns([1.5, 1.0, 1.5, 1.0])
    with primary_export_col_1:
        primary_csv_data = generate_primary_csv_report(primary_payroll_results, primary_final_net_take_home, primary_tbill_investment)
        st.download_button(label="Download CSV Report", data=primary_csv_data, file_name="primary_salary_payroll_report.csv", mime="text/csv", use_container_width=True)
    with primary_export_col_2:
        primary_pdf_data = generate_primary_pdf_report(primary_payroll_results, primary_final_net_take_home, primary_tbill_investment)
        st.download_button(label="Download PDF Report", data=primary_pdf_data, file_name="primary_salary_payroll_report.pdf", mime="application/pdf", use_container_width=True)


st.markdown("<h3 style='text-align: center;'>Alternative Salary Details</h3>", unsafe_allow_html=True)

alternative_left_spacer, alternative_center_content, alternative_right_spacer = st.columns([0.5, 5, 0.5])

with alternative_center_content:
    alternative_input_column_left, alternative_input_column_right = st.columns(2)
    
    with alternative_input_column_left:
        alternative_basic_salary = st.number_input("Input the second monthly basic salary to compare", min_value=0.0, value=4000.0, key="alternative_b2")
        alternative_allowances = st.number_input("Input the second total monthly allowances to compare", min_value=0.0, value=0.0, key="alternative_a2")
        alternative_bonus = st.number_input("Input the second monthly bonuses to compare", min_value=0.0, value=0.0, key="alternative_bo2")
        
    with alternative_input_column_right:
        alternative_overtime = st.number_input("Input the second overtime earnings to compare", min_value=0.0, value=0.0, key="alternative_o2")
        alternative_additional_deductions = st.number_input("Input the second additional optional deductions to compare", min_value=0.0, value=0.0, key="alternative_d2")
        
    st.markdown("<h4 style='text-align: center; margin-top: 30px;'>Comparison Investments</h4>", unsafe_allow_html=True)
    
    alternative_investment_column_left, alternative_investment_column_right = st.columns(2)
    
    with alternative_investment_column_left:
        alternative_tbill_investment = st.number_input("Enter the second monthly Treasury Bill savings target", min_value=0.0, value=0.0, key="alternative_t2")
        
    with alternative_investment_column_right:
        alternative_tier3_rate = st.number_input("Enter the second voluntary Tier 3 retirement savings rate percentage", min_value=0.0, max_value=16.5, value=0.0, key="alternative_tr2")

alternative_payroll_results = calculate_alternative_payroll_details(alternative_basic_salary, alternative_allowances, alternative_bonus, alternative_overtime, alternative_additional_deductions, alternative_tier3_rate)

alternative_final_net_take_home = alternative_payroll_results["alternative_net_salary"] - alternative_tbill_investment
if alternative_final_net_take_home < 0:
    alternative_final_net_take_home = 0.0

st.markdown("<h4 style='text-align: center; margin-top: 35px;'>Alternative Salary Graphical Representation</h4>", unsafe_allow_html=True)
alternative_chart_left, alternative_chart_center, alternative_chart_right = st.columns([1.2, 2.6, 1.2])

with alternative_chart_center:
    alternative_vertical_chart_data = {
        "Amount (GHS)": [
            alternative_payroll_results["alternative_gross"], 
            alternative_payroll_results["alternative_ssnit"], 
            alternative_payroll_results["alternative_tax"], 
            alternative_final_net_take_home
        ]
    }
    st.bar_chart(data=alternative_vertical_chart_data, y="Amount (GHS)", height=280)

st.markdown("<h4 style='text-align: center; margin-top: 35px;'>Alternative Salary Deductions and Net Pay Details</h4>", unsafe_allow_html=True)
alternative_metric_left, alternative_metric_center, alternative_metric_right = st.columns([0.5, 5, 0.5])

with alternative_metric_center:
    alternative_metric_column_one, alternative_metric_column_two, alternative_metric_column_three, alternative_metric_column_four = st.columns(4)
    with alternative_metric_column_one:
        st.metric("Total Gross Earnings", f"GHS {alternative_payroll_results['alternative_gross']:.2f}")
    with alternative_metric_column_two:
        st.metric("Mandatory SSNIT Contribution", f"GHS {alternative_payroll_results['alternative_ssnit']:.2f}")
    with alternative_metric_column_three:
        st.metric("Income Tax Paid to GRA", f"GHS {alternative_payroll_results['alternative_tax']:.2f}")
    with alternative_metric_column_four:
        st.metric("Final Net Take Home", f"GHS {alternative_final_net_take_home:.2f}")

    st.markdown(f"<p style='text-align: center; margin-top: 25px; margin-bottom: 25px; font-size: 1.25em;'>Effective Tax Rate: {alternative_payroll_results['alternative_effective_tax_rate']:.2f}%</p>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; margin-top: 40px; margin-bottom: 20px;'>Alternative Salary Expenses and Estimates</h4>", unsafe_allow_html=True)
alternative_pocket_left, alternative_pocket_center, alternative_pocket_right = st.columns([0.5, 5, 0.5])

with alternative_pocket_center:
    alternative_pocket_left_pane, alternative_space_buffer_2, alternative_pocket_right_pane = st.columns([2.5, 0.5, 2.5])
    with alternative_pocket_left_pane:
        st.markdown("<h5 style='text-align: left; margin-bottom: 15px;'>Take-Home Pay Summary</h5>", unsafe_allow_html=True)
        st.markdown(f"<p style='line-height: 2.0; margin-bottom: 10px;'>Final Net Take Home: GHS {alternative_final_net_take_home:.2f}</p>", unsafe_allow_html=True)
        if alternative_payroll_results["alternative_gross"] > 0:
            alternative_retention_percentage = (alternative_final_net_take_home / alternative_payroll_results["alternative_gross"]) * 100
            st.markdown(f"<p style='line-height: 2.0;'>You get to keep {alternative_retention_percentage:.1f}% of everything you earned.</p>", unsafe_allow_html=True)
            
    with alternative_pocket_right_pane:
        st.markdown("<h5 style='text-align: left; margin-bottom: 15px;'>Your Total Savings Breakdown</h5>", unsafe_allow_html=True)
        st.markdown(f"<p style='line-height: 2.0; margin-bottom: 10px;'>Pension Plan Savings: GHS {alternative_payroll_results['alternative_tier3']:.2f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='line-height: 2.0;'>Treasury Bill Investment Amount: GHS {alternative_tbill_investment:.2f}</p>", unsafe_allow_html=True)
        
    alternative_export_col_3, alternative_spacer_btn_3, alternative_export_col_4, alternative_spacer_btn_4 = st.columns([1.5, 1.0, 1.5, 1.0])
    with alternative_export_col_3:
        alternative_csv_data = generate_alternative_csv_report(alternative_payroll_results, alternative_final_net_take_home, alternative_tbill_investment)
        st.download_button(label="Download CSV Report", data=alternative_csv_data, file_name="alternative_salary_payroll_report.csv", mime="text/csv", use_container_width=True)
    with alternative_export_col_4:
        alternative_pdf_data = generate_alternative_pdf_report(alternative_payroll_results, alternative_final_net_take_home, alternative_tbill_investment)
        st.download_button(label="Download PDF Report", data=alternative_pdf_data, file_name="alternative_salary_payroll_report.pdf", mime="application/pdf", use_container_width=True)


st.markdown("<h3 style='text-align: center;'>Official Ghana Income Tax Rates</h3>", unsafe_allow_html=True)

table_left, table_center, table_right = st.columns([0.5, 5, 0.5])
with table_center:
    official_tax_bands_data = [
        {"Tax Band Position": "First Band", "Chargeable Income Amount (GHS)": "490.00", "Tax Rate Percentage": "0% / Free"},
        {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "110.00", "Tax Rate Percentage": "5%"},
        {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "130.00", "Tax Rate Percentage": "10%"},
        {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "3,166.67", "Tax Rate Percentage": "17.5%"},
        {"Tax Band Position": "Next Band", "Chargeable Income Amount (GHS)": "11,000.00", "Tax Rate Percentage": "25%"},
        {"Tax Band Position": "Exceeding Balance", "Chargeable Income Amount (GHS)": "Above 15,396.67", "Tax Rate Percentage": "30%"}
    ]
    st.table(official_tax_bands_data)

st.markdown("<h3 style='text-align: center;'>Tax Information & Education</h3>", unsafe_allow_html=True)

edu_left, edu_center, edu_right = st.columns([0.5, 5, 0.5])
with edu_center:
    st.markdown("<h5 style='text-align: center;'>Understanding Pay As You Earn (PAYE)</h5>", unsafe_allow_html=True)
    st.write("PAYE stands for Pay As You Earn. It is the system used by the Ghana Revenue Authority to calculate income tax on what you earn from your job. This is a progressive tax system, which means your tax rate goes up as you earn more money. Your income is broken down into separate blocks or bands, and each block is taxed at its own matching rate. As your earnings move up into higher bands, only the money inside those new bands faces the higher tax percentages.")
    
    st.markdown("<h5 style='text-align: center; margin-top: 15px;'>How Pension Deductions Help You Save on Tax</h5>", unsafe_allow_html=True)
    st.write("Under Ghanaian labor laws, your employer takes a mandatory 5.5 percent out of your basic salary and sends it straight to SSNIT to fund your main retirement pension. If you choose to put money into an approved voluntary Tier 3 pension plan, you get special tax breaks. You are allowed to set aside up to 16.5 percent of your basic salary completely tax-free. This money is taken out first, lowering the amount of income that the GRA can actually touch with tax percentages.")
    
    st.markdown("<h5 style='text-align: center; margin-top: 15px;'>Where This Information Comes From</h5>", unsafe_allow_html=True)
    st.write("All tax bands and tax percentages used in this calculation app are taken directly from the official website and public guidelines of the Ghana Revenue Authority. The calculation rules match the current systems used across the country.")

st.markdown(
    """
    <div style='text-align: center; color: #666666; font-size: 0.85em; margin-top: 30px; padding: 20px;'>
        <p>Regulatory & Legal Source Attribution Statement:</p>
        <p>The progressive personal income tax bands, Pay-As-You-Earn (PAYE) calculation variables, and 
        Tier 1/2/3 statutory pension deduction percentages utilized within this application engine are derived from 
        the official statutory schedules published by the Ghana Revenue Authority (GRA).</p>
        <p>Data Access & Verification Reference Date: May 2026. Official Schedule Source: <a href="https://gra.gov.gh/domestic-tax/tax-types/paye/" target="_blank">GRA PAYE Portal</a>.</p>
        <hr style='border: 0; border-top: 1px solid #e0e0e0; width: 50%; margin: 15px auto;'>
        <p>Educational Prototype Disclaimer: This web application is developed strictly as an academic 
        engineering project prototype. It does not constitute formal financial, legal, or professional tax accounting advice. 
        All calculations are for educational transparency and demonstration purposes only.</p>
    </div>
    """, 
    unsafe_allow_html=True
)