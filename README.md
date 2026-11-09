# ATM
🏦 ATM Simulation System (Multi-User)
📌 Project Description

The ATM Simulation System is a menu-driven Python application that simulates the basic operations of an Automated Teller Machine (ATM). It supports multiple users, allowing them to create bank accounts, log in securely using a 4-digit PIN, manage their balances, and view transaction history.

The system uses CSV files to store account details and transaction records permanently. It is developed using only core Python libraries without requiring any external packages.

✨ Features
Create Account: Create a new bank account with a unique 10-digit account number.
User Login: Log in using an account number and 4-digit PIN.
Check Balance: View the current account balance.
Deposit Money: Deposit money into the account.
Withdraw Money: Withdraw money in multiples of Rs. 100.
Mini Statement: View the last five transactions.
Change PIN: Change the existing account PIN.
Account Blocking: Automatically block an account after three incorrect PIN attempts.
Delete Account: Permanently delete an account after PIN and confirmation verification.
Data Persistence: Store user details and transaction history in CSV files.
🛠️ Technologies Used
Programming Language: Python 3
Modules:
csv – Reading and writing CSV files.
os – Checking file existence.
random – Generating unique account numbers.
datetime – Recording transaction dates and times.
📂 Project Structure
text
ATM-Simulation-System/
│
├── atm.py
├── users.csv
├── transactions.csv
└── README.md

File	Description
atm.py	Main Python program containing all ATM operations.
users.csv	Stores account numbers, names, PINs, balances, and account status.
transactions.csv	Stores transaction history for all users.
README.md	Project documentation.
⚙️ Requirements
Python 3.x
Any Python-supported operating system.
A code editor such as VS Code, PyCharm, or IDLE.

No external Python packages are required.

🚀 Installation and Execution
Step 1: Clone the Repository
bash
git clone https://github.com/your-username/ATM-Simulation-System.git

Step 2: Navigate to the Project Folder
bash
cd ATM-Simulation-System

Step 3: Run the Python Program
bash
python atm.py


If your system uses Python 3 separately, run:

bash
python3 atm.py

Step 4: Prepare the CSV Files

Create a users.csv file with the following headers:

csv
account_no,name,pin,balance,blocked


The transactions.csv file can be created automatically when the first transaction is recorded.

💻 Sample Output
text
=== Welcome to Python ATM ===

1. Login
2. Create New Account
3. Exit

Choose an option: 2

--- Create New Account ---
Enter your name: Rahul
Set a 4-digit PIN: 1234
Confirm PIN: 1234
Opening deposit: 5000

Account created! Your account number is: 1234567890
Please remember it - you need it to log in.

User Dashboard
text
1. Check Balance
2. Deposit
3. Withdraw
4. Mini Statement
5. Change PIN
6. Delete Account
7. Logout

Choose an option: 1

Current balance: Rs. 5000.00

📊 Data Storage

The project uses two CSV files for data management.

1. users.csv

Stores user account information:

Account Number
Account Holder Name
PIN
Account Balance
Account Blocking Status

2. transactions.csv

Stores transaction information:

Account Number
Transaction Date and Time
Transaction Type
Transaction Amount
Remaining Balance

All account and transaction information is saved to CSV files, so data remains available after restarting the program.

🔐 Security and Validation
PIN must contain exactly four digits.
Users get a maximum of three login attempts.
Accounts are blocked after three incorrect PIN attempts.
Withdrawals must be in multiples of Rs. 100.
Withdrawals cannot exceed the available balance.
Account deletion requires PIN verification and confirmation.

Note: This is an educational simulation, not a production banking system. PINs are stored as plain text, and additional security measures would be necessary for real-world use.

🎯 Learning Outcomes

This project demonstrates practical applications of:

Python functions and modular programming.
Dictionaries and lists.
File handling using CSV files.
Conditional statements and loops.
Exception handling.
User input validation.
Random number generation.
Date and time handling.
Basic banking operations.
🔮 Future Enhancements
Add fund transfers between accounts.
Add interest calculation.
Add daily withdrawal limits.
Encrypt PINs for improved security.
Add an administrator dashboard.
Develop a graphical user interface (GUI).
Generate downloadable account statements.
