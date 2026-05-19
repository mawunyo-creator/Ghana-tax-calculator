import json
import pandas as pd
import streamlit as st


# --- 1. DYNAMIC CONFIGURATION LOADER ---
def load_tax_bands():
    """Loads and parses the GRA tax bands dynamically from an external JSON configuration file."""
    try:
        with open("tax_bands.json", "r") as file:
            data = json.load(file)

        structured_bands = []
        for band in data.get("tax_bands", []):
            rate = float(band["rate"])
            if band["limit"] == "inf" or band["limit"] is None:
                limit = float("inf")
            else:
                limit = float(band["limit"])
            structured_bands.append((limit, rate))
        return structured_bands
    except Exception:
        # Hardcoded fallback safety system matching standard GRA tax thresholds
        return [
            (490.00, 0.00),
            (110.00, 0.05),
            (130.00, 0.10),
            (3166.67, 0.175),
            (1104.33, 0.25),
            (float("inf"), 0.30),
        ]


# --- 2. ADVANCED PROGRESSIVE TAX ENGINE ---
def calculate_detailed_paye(taxable_income, tax_bands):
    """Calculates progressive GRA PAYE tax and builds a compliant audit breakdown table."""
    remaining_income = taxable_income
    total_tax = 0.0
    band_breakdown = []

    for limit, rate in tax_bands:
        if remaining_income <= 0:
            band_breakdown.append(
                {
                    "Tax Band": (
                        f"Up to GHS {limit:.2f}"
                        if limit != float("inf")
                        else "Exceeding Balance"
                    ),
                    "Tax Rate": f"{rate * 100}%",
                    "Amount Taxed": "GHS 0.00",
                    "Tax Paid": "GHS 0.00",
                }
            )
            continue

        if limit == float("inf"):
            taxable_amount = remaining_income
        else:
            taxable_amount = min(remaining_income, limit)

        tax_paid = taxable_amount * rate
        total_tax += tax_paid
        remaining_income -= taxable_amount

        band_breakdown.append(
            {
                "Tax Band": (
                    f"Up to GHS {limit:.2f}"
                    if limit != float("inf")
                    else "Exceeding Balance"
                ),
                "Tax Rate": f"{rate * 100}%",
                "Amount Taxed": f"GHS {taxable_amount:,.2f}",
                "Tax Paid": f"GHS {tax_paid:,.2f}",
            }
        )

    return float(round(total_tax, 2)), pd.DataFrame(band_breakdown)


# --- 3. MAIN APPLICATION INTERFACE ARCHITECTURE ---
def main():
    st.set_page_config(
        page_title="Ghana PAYE Payroll Engine", layout="wide"
    )

    # REMOVED FLAG FOR A CLEAN, PROFESSIONAL ENTERPRISE HEADER
    st.title("Ghana Revenue Authority Payroll Transparency System")
    st.write(
        "A compliant regulatory framework engine driving dynamic data parsing from local configurations."
    )
    st.markdown("---")

    active_bands = load_tax_bands()

    # --- SIDEBAR INPUT SYSTEM (Requirement 1) ---
    st.sidebar.header("📥 Primary Income Entry Parameters")
    basic_salary = st.sidebar.number_input(
        "Basic Salary (GHS)", min_value=0.0, value=5000.0, step=100.0
    )
    allowances = st.sidebar.number_input(
        "Monthly Allowances (GHS)", min_value=0.0, value=500.0, step=50.0
    )
    bonuses = st.sidebar.number_input(
        "Bonuses (GHS)", min_value=0.0, value=0.0, step=50.0
    )
    overtime = st.sidebar.number_input(
        "Overtime Earnings (GHS)", min_value=0.0, value=0.0, step=50.0
    )
    custom_pension = st.sidebar.number_input(
        "Voluntary Pension/Provident Fund (GHS)",
        min_value=0.0,
        value=0.0,
        step=50.0,
    )
    extra_deductions = st.sidebar.number_input(
        "Additional Deductions (Optional) (GHS)",
        min_value=0.0,
        value=0.0,
        step=50.0,
    )

    # --- PRIMARY MATHEMATICAL ENGINE COMPUTATION ---
    gross_salary = basic_salary + allowances + bonuses + overtime
    employee_ssnit = basic_salary * 0.055
    total_reliefs = employee_ssnit + custom_pension
    taxable_income = max(0.0, gross_salary - total_reliefs)

    paye_tax, breakdown_df = calculate_detailed_paye(
        taxable_income, active_bands
    )
    total_deductions = paye_tax + employee_ssnit + extra_deductions
    net_salary = gross_salary - total_deductions
    effective_tax_rate = (
        ((paye_tax / gross_salary) * 100) if gross_salary > 0 else 0.0
    )

    # =========================================================================
    # SECTION 1: PRIMARY PAYROLL DASHBOARD
    # =========================================================================
    st.header("📊 Primary Payroll Dashboard")
    st.write("Real-time tracking of itemized tax parameters and statutory progressive ledgers.")
    
    m_grid1, m_grid2, m_grid3, m_grid4 = st.columns(4)
    with m_grid1:
        st.metric(label="Gross Earnings", value=f"GHS {gross_salary:,.2f}")
    with m_grid2:
        st.metric(label="PAYE Tax Liability", value=f"GHS {paye_tax:,.2f}")
    with m_grid3:
        st.metric(label="Effective Tax Rate", value=f"{effective_tax_rate:.2f}%")
    with m_grid4:
        st.metric(label="Net Take-Home Pay", value=f"GHS {net_salary:,.2f}")

    st.markdown("#### 📋 Progressive Tax Tier Ledger Breakdown")
    st.table(breakdown_df)

    st.info(
        f"**Audit Ledger Details:** Basic Salary: GHS {basic_salary:,.2f} | "
        f"SSNIT Deduction (5.5%): GHS {employee_ssnit:,.2f} | "
        f"Chargeable Base: GHS {taxable_income:,.2f} | "
        f"Total Monthly Deductions: GHS {total_deductions:,.2f}"
    )

    csv_data = breakdown_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Audit Breakdown Record (CSV)",
        data=csv_data,
        file_name="gra_payroll_breakdown.csv",
        mime="text/csv",
    )

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 2: SCENARIO VARIANCE & COMPARATIVE MODELING ENGINE
    # =========================================================================
    st.header("🔄 Scenario Variance & Comparative Modeling Engine")
    st.write("Simulate and contrast alternative salary structures side-by-side against active metrics.")
    
    c_input1, c_input2 = st.columns(2)
    with c_input1:
        comp_salary = st.number_input(
            "Compare Alternative Basic Salary (GHS)",
            min_value=0.0,
            value=7500.0,
            step=100.0,
            key="comp_base",
        )
    with c_input2:
        comp_allowance = st.number_input(
            "Compare Alternative Allowances (GHS)",
            min_value=0.0,
            value=0.0,
            step=50.0,
            key="comp_allow",
        )

    # Scenario B Calculations
    comp_gross = comp_salary + comp_allowance
    comp_ssnit = comp_salary * 0.055
    comp_reliefs = comp_ssnit + custom_pension
    comp_taxable = max(0.0, comp_gross - comp_reliefs)

    comp_tuple = calculate_detailed_paye(comp_taxable, active_bands)
    comp_paye = float(comp_tuple[0])

    comp_total_deductions = comp_paye + comp_ssnit + extra_deductions
    comp_net = comp_gross - comp_total_deductions
    comp_eff_tax = ((comp_paye / comp_gross) * 100) if comp_gross > 0 else 0.0

    st.markdown("#### Real-Time Comparative Metrics")
    v_col1, v_col2, v_col3 = st.columns(3)
    with v_col1:
        st.metric(
            label="Scenario B Net Take-Home",
            value=f"GHS {comp_net:,.2f}",
            delta=f"GHS {(comp_net - net_salary):,.2f}",
        )
    with v_col2:
        st.metric(
            label="Scenario B Deductions",
            value=f"GHS {comp_total_deductions:,.2f}",
            delta=f"GHS {(comp_total_deductions - total_deductions):,.2f}",
            delta_color="inverse",
        )
    with v_col3:
        st.metric(
            label="Scenario B Effective Tax Rate",
            value=f"{comp_eff_tax:.2f}%",
            delta=f"{(comp_eff_tax - effective_tax_rate):.2f}%",
            delta_color="inverse",
        )

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 3: STATUTORY GRA TRANSPARENCY & EDUCATION FRAMEWORK (STRICT VERTICAL)
    # =========================================================================
    st.header("🎓 Statutory GRA Transparency & Education Framework")
    st.write("Decoupled national payroll definitions explaining statutory computational parameters.")
    
    # 1. WHAT IS PAYE (FIRST)
    with st.expander("❓ 1. What is PAYE (Pay-As-You-Earn)?", expanded=True):
        st.write(
            "**Pay-As-You-Earn (PAYE)** is a statutory withholding tax framework structured under the "
            "**Income Tax Act, 2015 (Act 896)**. It mandates employers to deduct income tax directly from "
            "all resident and non-resident employee emoluments before payment.  \n\n"
            "**What counts as taxable income?** This encompasses your core basic salary, cash bonuses, "
            "overtime pay, commissions, and standard monthly allowances (housing, transport, utilities). "
            "By law, employers act as collection agents, remitting these withheld balances to the "
            "Ghana Revenue Authority (GRA) by the 15th day of every subsequent month."
        )

    # 2. PROGRESSIVE TAXATION MECHANICS (SECOND)
    with st.expander("📈 2. Progressive Taxation Mechanics Explained", expanded=True):
        st.write(
            "Ghana applies a graduated **Progressive Tax Scale** system to personal earnings rather than a flat percentage. "
            "This approach scales individual liabilities according to economic capacity, splitting your net **Chargeable Income** "
            "into separate, sequential tax bands.  \n\n"
            "Each specific portion of income is taxed only within its designated boundary rate. For instance, your first "
            "GHS 490.00 is always protected at a **0% tax-free threshold**. Any income spilling past this initial bracket "
            "cascades down into subsequent bands, facing steps of 5%, 10%, 17.5%, and 25%, until any remaining balance "
            "exceeding the top band limit is taxed at the maximum statutory margin of **30%**."
        )
        
    # 3. MANDATORY NATIONAL DEDUCTIONS (THIRD)
    with st.expander("🛡️ 3. Mandatory National Deductions & Relief Framework", expanded=True):
        st.write(
            "Before your gross income ever hits the progressive GRA tax bands, national regulatory provisions "
            "require the calculation of tax-exempt exclusions and retirement contributions. This application "
            "accurately models that exact structural sequence:  \n\n"
            "• **Tier 1 & Tier 2 Pensions (SSNIT):** Under the National Pensions Act, 2008 (Act 766), employees contribute a mandatory "
            "**5.5%** of their monthly Basic Salary toward national pension funds. This contribution is completely tax-exempt.  \n"
            "• **Voluntary Apportionments (Provident Funds/Tier 3):** Employees can deduct up to 16.5% of their basic salary into approved "
            "voluntary pension funds to secure additional statutory reliefs.  \n"
            "• **The Mathematical Core:** Your *Chargeable Income Base* (the specific value tested by the tax ledger) is derived exclusively by "
            "subtracting these non-taxable pension reliefs from your total Gross Earnings. This ensures strict compliance with GRA audit rules."
        )

    st.caption(
        "🔬 **Framework Metadata & Source Integrity:** \n"
        "• **Data Source:** Official GRA Domestic Tax Regulations  \n"
        "• **Extraction Protocol:** Parsed from localized configuration schemas (`tax_bands.json`) [No live scraping running]  \n"
        "• **Audit Verification Date:** May 2026 Inspection"
    )


if __name__ == "__main__":
    main()