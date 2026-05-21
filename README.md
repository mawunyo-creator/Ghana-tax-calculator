## 🚀 Production Operation & Deployment Guide

Follow these steps to operate the calculator engine locally or push it to a live cloud server.

### 1. Running the Application Locally
After installing your dependencies from the `requirements.txt` file, boot up the local web engine:
```bash
streamlit run App.py
```
* **Note**: A local browser window should pop up automatically at `http://localhost:8501`. If it does not, copy the link outputted in your terminal.

---

### 2. How to Operate the Application Interface

#### 📊 Salary Tax Calculator Tab
1. **Input Parameters**: Use the sidebar or input fields to specify a worker's **Monthly Basic Salary**, **Allowances**, **Bonus**, and **Overtime**.
2. **Review Deductions**: Watch the **Payroll Transparency Dashboard** update live. It automatically isolates the 5.5% SSNIT worker deduction before running the multi-bracket tax algorithm.
3. **Audit the Breakdown Table**: Verify compliance using the required **Tax Band | Tax Rate | Amount Taxed | Tax Paid** matrix display.
4. **Export Audits**: Click the **📥 Download Payroll Breakdown Report (.CSV)** button at the bottom of the page to export local records instantly.

#### 📈 Multi-Salary Comparison Tool Tab
1. Input two unique base compensation figures under Profile Option A and Option B.
2. Review the structural visual bar chart comparing respective effective tax burdens side-by-side.

---

### 3. Cloud Deployment Instructions (Streamlit Community Cloud)
To fulfill the public deployment requirement, follow these continuous integration steps:

1. Visit [share.streamlit.io](https://streamlit.io) and log in using your GitHub Account.
2. Click **New App** in the upper-right corner of your workspace dashboard.
3. Configure the deployment properties field precisely as follows:
   * **Repository**: `mawunyo-creator/Ghana-tax-calculators`
   * **Branch**: `main` (Ensure you have merged your `development` branch into `main` before this step)
   * **Main file path**: `App.py`
4. Click **Deploy!** Your production build will be live globally on a public web URL within 2 minutes.
