# Ghana Revenue Authority (GRA) Compliant Payroll Transparency System

An advanced, data-driven statutory accounting and comparative payroll projection engine built using Python and Streamlit. This application serves as an educational prototype designed to model progressive national income tax withholding algorithms under the **Income Tax Act, 2015 (Act 896)** and pension rules under the **National Pensions Act, 2008 (Act 766)**.

## 📊 Technical Project Features
- **Dynamic Configuration Layer**: Fully decoupled data structure parsing progressive tax boundaries from local JSON schemas instead of hardcoding variables.
- **Sequential Deduction Math Engine**: Accurate calculation of non-taxable pension reliefs (Tier 1/2/3) prior to computing graduated tax steps.
- **Dual-Scenario Modeling Portal**: Parallel sandbox modeling enabling real-time structural adjustments and side-by-side delta tracking against current metrics.
- **Audit-Ready Visual Formatting**: Full-width vertical metrics presentation and high-contrast styled data matrices preventing string truncations.
- **Enterprise Report Generation**: On-demand file streaming for raw data logs (CSV) and officially mapped statutory compliance payslips (PDF).

## ⚖️ Ethical & Legal Compliance Boundaries
- **Zero-Scraping Architecture**: To comply strictly with project constraints and protect public resource bandwidth, this application completely avoids live scraping frameworks on the GRA domain. All data arrays are validated manually and stored locally in `Tax_bands.json`.
- **Data Privacy Protocols**: The runtime system treats user entries purely as transient state data. No identity metrics or personal financial parameters are written to permanent external databases.

## 🛠️ Local Environment Initialization Instructions

1. **Clone the Repository Branch**:
   ```bash
   git clone [https://github.com/your-username/Ghana-tax-calculator.git](https://github.com/your-username/Ghana-tax-calculator.git)
   cd Ghana-tax-calculator