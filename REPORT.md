GHANA PAYROLL AND TAX CALcalculator REPORT

This report breaks down how the application works, how the calculations are made, and how the files in this project are organized. It is meant to show the exact steps used to handle payroll calculations in Ghana.


PROJECT FILE STRUCTURE

Here is what each file in this project folder does:

App.py
This is the main file that runs the web application. It contains the logic for calculating taxes and pensions, and it creates the web interface you see on your screen.

README.md
This file gives a quick summary of the application and explains how to install and run it on your computer.

REPORT.md
This is the file you are reading right now. It explains the project details, the math behind the calculations, and how the program is structured.

requirements.txt
This file lists the exact packages that need to be installed for the app to run, which are streamlit and fpdf.

tax_bands.json
This file stores the official Ghana Revenue Authority tax rates in a structured data format so the application can read them.


HOW PAYROLL CALCULATIONS WORK

The calculation engine follows a strict step by step order to make sure the final take home cash is completely accurate according to Ghanaian laws.

Step 1: Gross Earnings
The app adds up your basic salary, allowances, bonuses, and overtime pay to find your total gross earnings.

Step 2: Mandatory SSNIT Deduction
The program takes exactly five point five percent of your basic salary. This money goes directly to your national retirement pension and is completely tax free.

Step 3: Voluntary Tier Three Pension Deduction
If you choose to save extra money in a Tier three pension, the app calculates that amount. The law says you can save up to sixteen point five percent of your basic salary without paying tax on it. The app checks this limit and subtracts the tax free portion from your remaining income.

Step 4: Chargeable Income
The app subtracts your SSNIT deduction, your tax free Tier three savings, and any other optional deductions from your gross earnings. The number left over is your chargeable income, which is the exact amount of money the government can tax.

Step 5: Progressive Income Tax Calculation
The app takes your chargeable income and passes it through the official Ghana Revenue Authority tax bands. It taxes the first section at zero percent, the next section at five percent, and keeps moving up through the blocks until it reaches the final thirty percent rate for any high remaining balance.

Step 6: Final Take Home Cash
To find your final pocket money, the app starts with your total gross earnings and subtracts all taxes paid to the government, your SSNIT contribution, your Tier three savings, any extra deductions, and your chosen short term Treasury Bill investment targets.


SYSTEM FLOW AND DESIGN

The application is split into two completely separate calculation engines. One engine handles the Primary Salary numbers, and the second engine handles the Alternative Salary numbers. 

Every variable name, internal function, and data storage key uses specific tags like primary or alternative. Because these blocks are kept totally separate, you can change the numbers in the first section without messing up or changing the numbers in the second comparison section. This guarantees that your side by side comparison is always correct and free from errors.