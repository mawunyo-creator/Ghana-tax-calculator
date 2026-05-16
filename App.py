def calculate_ghana_paye(chargeable_income):
    """
    Computes precise progressive PAYE tax based on the latest 
    GRA monthly tax schedules for resident individuals.
    """
    # Exact statutory monthly incremental bands (Not cumulative caps)
    bands = [
        {"limit": 490.00, "rate": 0.00},     # First 490
        {"limit": 110.00, "rate": 0.05},     # Next 110
        {"limit": 130.00, "rate": 0.10},     # Next 130
        {"limit": 3166.67, "rate": 0.175},   # Next 3,166.67
        {"limit": 16000.00, "rate": 0.25},   # Next 16,000
        {"limit": 30520.00, "rate": 0.30},   # Next 30,520
        {"limit": float('inf'), "rate": 0.35} # Exceeding cumulative 50,416.67
    ]
    
    remaining_income = chargeable_income
    total_tax = 0.0
    band_breakdown = []
    
    for i, band in enumerate(bands, 1):
        if remaining_income <= 0:
            band_breakdown.append((f"Band {i} ({band['rate']*100}%)", 0.00))
            continue
            
        taxable_amount_in_band = min(remaining_income, band["limit"])
        tax_in_band = taxable_amount_in_band * band["rate"]
        
        total_tax += tax_in_band
        band_breakdown.append((f"Band {i} ({band['rate']*100}%)", tax_in_band))
        
        remaining_income -= taxable_amount_in_band
        
    return total_tax, band_breakdown


def main():
    print("=" * 65)
    print("      GHANA REVENUE AUTHORITY COMPLIANT PAYROLL ENGINE   ")
    print("=" * 65)
    
    # -------------------------------------------------------------
    # PHASE 1: INPUT ACQUISITION & STRICT TYPE DATA VALIDATION
    # -------------------------------------------------------------
    try:
        basic_salary = float(input("Enter Monthly Basic Salary (GHS): "))
        bonuses = float(input("Enter Total Bonuses (GHS): "))
        overtime_earnings = float(input("Enter Overtime Earnings (GHS): "))
        allowances = float(input("Enter Allowances (e.g., Rent/Transport) (GHS): "))
        
        # Statutory Reliefs and non-taxable individual allowances
        tax_reliefs = float(input("Enter Total Approved Tax Reliefs (GHS): "))
        provident_fund = float(input("Enter Employee Provident Fund Contribution (GHS): "))
        
        # Capture extraneous non-tax post deductions (e.g. company loans)
        other_deductions_raw = input("Enter Voluntary Post-Tax Deductions (GHS) [Press Enter to skip]: ")
        other_deductions = float(other_deductions_raw) if other_deductions_raw.strip() else 0.0
        
        # Logic Gate: Block negative numbers
        if any(val < 0 for val in [basic_salary, bonuses, overtime_earnings, allowances, tax_reliefs, provident_fund, other_deductions]):
            print("\n[CRITICAL ERROR] Execution Halted. Negative financial parameters are invalid.")
            return
            
    except ValueError:
        print("\n[CRITICAL ERROR] Processing Failed. Input data contains non-numeric strings.")
        return

    # -------------------------------------------------------------
    # PHASE 2: SEQUENTIAL MATHEMATICAL PROCESSING (GRA Standard)
    # -------------------------------------------------------------
    
    # 1. Compute 5.5% Employee SSNIT directly on Basic Salary
    ssnit_deduction = basic_salary * 0.055
    
    # 2. Compute Total Gross Earnings (Aggregate of basic and all cash benefits)
    total_gross = basic_salary + bonuses + overtime_earnings + allowances
    
    # 3. Deduct SSNIT, Provident Fund, and Approved Reliefs to establish exact Chargeable Income
    total_allowable_deductions = ssnit_deduction + provident_fund + tax_reliefs
    chargeable_income = total_gross - total_allowable_deductions
    
    # Avoid mathematical negative errors if allowances/reliefs outpace total gross
    if chargeable_income < 0:
        chargeable_income = 0.0
        
    # 4. Route calculated Chargeable Income directly to progressive bands
    paye_tax_liability, tax_bands_breakdown = calculate_ghana_paye(chargeable_income)
    
    # 5. Compile Final Take-home metrics
    aggregate_deductions = paye_tax_liability + ssnit_deduction + provident_fund + other_deductions
    net_salary_take_home = total_gross - aggregate_deductions
    effective_tax_rate = (paye_tax_liability / total_gross * 100) if total_gross > 0 else 0.0

    # -------------------------------------------------------------
    # PHASE 3: AUDITED RESULTS DASHBOARD (Rigid Table Structure)
    # -------------------------------------------------------------
    print("\n" + "=" * 65)
    print(f"{'OFFICIAL PAYROLL EVALUATION AUDIT':^65}")
    print("=" * 65)
    print(f"| {'Itemized Component Description':<35} | {'Value (GHS)':>22} |")
    print("-" * 65)
    print(f"| {'Monthly Base/Basic Salary':<35} | {basic_salary:>22,.2f} |")
    print(f"| {'Total Added Cash Elements':<35} | {(bonuses + overtime_earnings + allowances):>22,.2f} |")
    print(f"| {'TOTAL MONTHLY GROSS EARNINGS':<35} | {total_gross:>22,.2f} |")
    print("-" * 65)
    print(f"| {'[-] Mandatory Employee SSNIT (5.5%)':<35} | {ssnit_deduction:>22,.2f} |")
    print(f"| {'[-] Employee Provident Fund':<35} | {provident_fund:>22,.2f} |")
    print(f"| {'[-] Declared Statutory Reliefs':<35} | {tax_reliefs:>22,.2f} |")
    print("-" * 65)
    print(f"| {'NET CHARGEABLE INCOME (TAX BASE)':<35} | {chargeable_income:>22,.2f} |")
    print(f"| {'TOTAL CALCULATED PAYE LIABILITY':<35} | {paye_tax_liability:>22,.2f} |")
    print(f"| {'[-] Miscellaneous Post-Tax Deductions':<35} | {other_deductions:>22,.2f} |")
    print("-" * 65)
    print(f"| {'NET TAKE-HOME SALARY':<35} | {net_salary_take_home:>22,.2f} |")
    print(f"| {'Effective Employee Tax Burthen':<35} | {effective_tax_rate:>21.2f}% |")
    print("=" * 65)
    
    # Granular Band Isolation
    print(f"\n{'PROGRESSIVE SLICE DECONSTRUCTION (PAYE)':^65}")
    print("-" * 65)
    print(f"| {'GRA Statutory Band Matrix':<35} | {'Tax Apportioned':>22} |")
    print("-" * 65)
    for slice_identity, dynamic_charge in tax_bands_breakdown:
        print(f"| {slice_identity:<35} | {dynamic_charge:>22,.2f} |")
    print("=" * 65)


if __name__ == "__main__":
    main()