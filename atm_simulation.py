"""ATM Simulation System (Multi-User) - core Python only (csv, os, random, datetime)."""

import csv
import os
import random
from datetime import datetime

USERS_FILE = "users.csv"
TRANSACTIONS_FILE = "transactions.csv"
MAX_ATTEMPTS = 3


# ---------- File handling ----------
def load_users():
    """Load users and their transactions from the two CSV files."""
    if not os.path.exists(USERS_FILE):
        print(f"'{USERS_FILE}' not found. Put it in the same folder as this program.")
        return None

    users = {}
    with open(USERS_FILE, "r", newline="") as f:
        for row in csv.DictReader(f):
            users[row["account_no"]] = {
                "name": row["name"],
                "pin": row["pin"],
                "balance": float(row["balance"]),
                "blocked": row["blocked"].strip().lower() == "true",
                "transactions": [],
            }

    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "r", newline="") as f:
            for row in csv.DictReader(f):
                if row["account_no"] in users:
                    users[row["account_no"]]["transactions"].append({
                        "time": row["time"],
                        "type": row["type"],
                        "amount": float(row["amount"]),
                        "balance": float(row["balance"]),
                    })
    return users


def save_users(users):
    """Write all users and transactions back to the CSV files."""
    with open(USERS_FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["account_no", "name", "pin", "balance", "blocked"])
        for acc, u in users.items():
            w.writerow([acc, u["name"], u["pin"], u["balance"], u["blocked"]])

    with open(TRANSACTIONS_FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["account_no", "time", "type", "amount", "balance"])
        for acc, u in users.items():
            for t in u["transactions"]:
                w.writerow([acc, t["time"], t["type"], t["amount"], t["balance"]])


# ---------- Helpers ----------
def add_transaction(users, user, kind, amount):
    user["transactions"].append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": kind,
        "amount": amount,
        "balance": user["balance"],
    })
    save_users(users)


def get_amount(prompt):
    try:
        amount = float(input(prompt))
    except ValueError:
        print("Invalid amount. Enter a number.")
        return None
    if amount <= 0:
        print("Amount must be greater than zero.")
        return None
    return amount


def generate_account_number(users):
    while True:
        acc_no = str(random.randint(1000000000, 9999999999))
        if acc_no not in users:
            return acc_no


# ---------- Account creation and login ----------
def create_account(users):
    print("\n--- Create New Account ---")
    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    pin = input("Set a 4-digit PIN: ").strip()
    if not (pin.isdigit() and len(pin) == 4):
        print("PIN must be exactly 4 digits.")
        return
    if pin != input("Confirm PIN: ").strip():
        print("PINs do not match.")
        return
    opening = get_amount("Opening deposit: ")
    if opening is None:
        return

    acc_no = generate_account_number(users)
    users[acc_no] = {"name": name, "pin": pin, "balance": opening,
                     "blocked": False, "transactions": []}
    add_transaction(users, users[acc_no], "Deposit", opening)
    print(f"\nAccount created! Your account number is: {acc_no}")
    print("Please remember it - you need it to log in.")


def login(users):
    acc_no = input("Enter account number: ").strip()
    if acc_no not in users:
        print("Account not found.")
        return None
    user = users[acc_no]
    if user["blocked"]:
        print("This account is blocked. Contact the bank.")
        return None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if input("Enter 4-digit PIN: ").strip() == user["pin"]:
            print(f"\nWelcome, {user['name']}!")
            return acc_no, user
        print(f"Wrong PIN. Attempts left: {MAX_ATTEMPTS - attempt}")

    user["blocked"] = True
    save_users(users)
    print("Too many wrong attempts. Account blocked.")
    return None


# ---------- ATM operations ----------
def check_balance(user):
    print(f"Current balance: Rs. {user['balance']:.2f}")


def deposit(users, user):
    amount = get_amount("Enter amount to deposit: ")
    if amount is None:
        return
    user["balance"] += amount
    add_transaction(users, user, "Deposit", amount)
    print(f"Rs. {amount:.2f} deposited. New balance: Rs. {user['balance']:.2f}")


def withdraw(users, user):
    amount = get_amount("Enter amount to withdraw: ")
    if amount is None:
        return
    if amount % 100 != 0:
        print("Please enter an amount in multiples of 100.")
    elif amount > user["balance"]:
        print("Insufficient balance.")
    else:
        user["balance"] -= amount
        add_transaction(users, user, "Withdraw", amount)
        print(f"Please collect Rs. {amount:.2f}. New balance: Rs. {user['balance']:.2f}")


def mini_statement(user):
    last = user["transactions"][-5:]
    if not last:
        print("No transactions yet.")
        return
    print("\n--- Mini Statement (last 5) ---")
    print(f"{'Date/Time':<20}{'Type':<10}{'Amount':>10}{'Balance':>12}")
    for t in reversed(last):
        print(f"{t['time']:<20}{t['type']:<10}{t['amount']:>10.2f}{t['balance']:>12.2f}")


def change_pin(users, user):
    if input("Enter current PIN: ").strip() != user["pin"]:
        print("Wrong PIN.")
        return
    new_pin = input("Enter new 4-digit PIN: ").strip()
    if not (new_pin.isdigit() and len(new_pin) == 4):
        print("PIN must be exactly 4 digits.")
        return
    user["pin"] = new_pin
    save_users(users)
    print("PIN changed successfully.")


def delete_account(users, acc_no, user):
    """Delete the logged-in account after PIN and yes/no confirmation."""
    if input("Enter PIN to confirm: ").strip() != user["pin"]:
        print("Wrong PIN. Account not deleted.")
        return False
    if user["balance"] > 0:
        print(f"Your balance is Rs. {user['balance']:.2f}. "
              "It will be paid out as cash when the account is closed.")
    if input("Delete this account permanently? (yes/no): ").strip().lower() != "yes":
        print("Cancelled. Account not deleted.")
        return False
    del users[acc_no]
    save_users(users)
    print(f"Account {acc_no} deleted. Collect your cash. Goodbye!")
    return True


def user_session(users, acc_no, user):
    while True:
        print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Mini Statement"
              "\n5. Change PIN\n6. Delete Account\n7. Logout")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            check_balance(user)
        elif choice == "2":
            deposit(users, user)
        elif choice == "3":
            withdraw(users, user)
        elif choice == "4":
            mini_statement(user)
        elif choice == "5":
            change_pin(users, user)
        elif choice == "6":
            if delete_account(users, acc_no, user):
                break
        elif choice == "7":
            print("Logged out.")
            break
        else:
            print("Invalid choice. Try again.")


# ---------- Main ----------
def main():
    users = load_users()
    if users is None:
        return
    print("=== Welcome to Python ATM ===")
    while True:
        print("\n1. Login\n2. Create New Account\n3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            result = login(users)
            if result:
                user_session(users, result[0], result[1])
        elif choice == "2":
            create_account(users)
        elif choice == "3":
            print("Thank you for using the ATM. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
