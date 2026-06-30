GHANA PAYROLL AND TAX CALCULATOR

This is a web app built with Python and Streamlit to help workers in Ghana calculate their exact salary deductions and take-home pay. It allows you to look at two different salary choices side by side to see which one leaves you with more cash.


WHAT THIS APP DOES

It lets you type in your basic monthly salary, your allowances, bonuses, and overtime pay. 

It calculates your automatic five point five percent SSNIT contribution.

It checks your voluntary Tier three pension savings and applies tax breaks up to the legal limit of sixteen point five percent.

It breaks down your income tax automatically using the official steps set by the Ghana Revenue Authority.

It shows your final cash take-home pay after subtracting your savings, taxes, and short term Treasury Bill investment targets.

It lets you click a button to download the entire summary as a clean CSV file or a PDF document directly to your computer.


HOW IT CALCULATES YOUR TAX

The app uses the official progressive tax blocks. Your income is split into separate sections and taxed at different rates:

First 490.00 GHS is tax free
Next 110.00 GHS is taxed at 5 percent
Next 130.00 GHS is taxed at 10 percent
Next 3166.67 GHS is taxed at 17.5 percent
Next 11000.00 GHS is taxed at 25 percent
Any remaining amount above that is taxed at 30 percent


HOW TO RUN THIS APP LOCALLY

Follow these simple steps on your computer terminal to run the app:

1. Download or clone this project folder to your computer.

2. Open your terminal inside the folder and create a virtual environment by typing:
python -m venv venv

3. Activate the virtual environment:
On Windows PowerShell type: .\venv\Scripts\Activate.ps1
On Windows Command Prompt type: .\venv\Scripts\activate.bat

4. Install the two needed packages by typing:
pip install streamlit fpdf

5. Start the web server app by typing:
streamlit run app.py


WHERE THE DATA COMES FROM

All tax percentages, pension caps, and progressive income blocks used in this application are copied exactly from the public operational schedules on the official Ghana Revenue Authority domestic tax portal.


IMPORTANT WARNING

This web application was made strictly as a school engineering project prototype. It is meant for educational simulation and learning purposes only. It does not count as formal legal, financial, or professional tax accounting advice.