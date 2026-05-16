import tkinter as tk
from datetime import datetime
import os

# ----------- BACKEND -----------

def save_transaction(type, amount, balance):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("transactions.txt", "a", encoding='utf-8') as file:
        file.write(f"{timestamp} | {type} | Amount: ₹{amount} | Balance: ₹{balance}\n")

def deposit_money(balance, amount):
    balance += amount
    save_transaction("Deposit", amount, balance)
    return balance

def withdraw_money(balance, amount):
    if amount <= balance:
        balance -= amount
        save_transaction("Withdraw", amount, balance)
        return balance, "Withdraw successful"
    else:
        return balance, "Insufficient balance"

def show_history():
    try:
        if not os.path.exists("transactions.txt"):
            return "No transactions found."
        with open("transactions.txt", "r", encoding='utf-8') as file:
            return file.read()
    except:
        return "Error reading history."

def load_balance():
    if not os.path.exists("transactions.txt"):
        return 0
    try:
        with open("transactions.txt", "r", encoding='utf-8') as file:
            lines = file.readlines()
            if not lines: return 0
            last_line = lines[-1].strip()
            # Find the balance at the end of the line
            if "Balance:" in last_line:
                return int(last_line.split("Balance: ₹")[1].strip())
    except:
        pass
    return 0

# ----------- GUI -----------

balance = load_balance()

def check_balance():
    result_label.config(text=f"Current Balance: ₹{balance}", fg="black")

def deposit():
    global balance
    try:
        amount_str = entry_amount.get().strip()
        amount = int(amount_str)
        if amount <= 0: raise ValueError
        balance = deposit_money(balance, amount)
        result_label.config(text=f"Deposited ₹{amount} successfully!", fg="green")
        entry_amount.delete(0, tk.END)
    except:
        result_label.config(text="Enter valid positive amount", fg="red")

def withdraw():
    global balance
    try:
        amount_str = entry_amount.get().strip()
        amount = int(amount_str)
        if amount <= 0: raise ValueError
        balance, msg = withdraw_money(balance, amount)
        color = "green" if "successful" in msg else "red"
        result_label.config(text=msg, fg=color)
        if "successful" in msg:
            entry_amount.delete(0, tk.END)
    except:
        result_label.config(text="Enter valid positive amount", fg="red")

def history():
    data = show_history()
    # Display history in a simple popup or the label
    # Given the request for "simple", I'll use a simple Toplevel for history
    history_win = tk.Toplevel(root)
    history_win.title("History")
    tk.Label(history_win, text="Transaction History", font=("Arial", 12, "bold")).pack(pady=10)
    txt = tk.Text(history_win, height=15, width=50)
    txt.insert(tk.END, data)
    txt.config(state="disabled")
    txt.pack(padx=10, pady=10)

# ----------- WINDOW -----------

root = tk.Tk()
root.title("Simple Banking")
root.geometry("350x450")
root.configure(padx=20, pady=20)

tk.Label(root, text="BANKING SYSTEM", font=("Arial", 18, "bold")).pack(pady=10)

tk.Label(root, text="Enter Amount (₹):").pack(pady=(10, 0))
entry_amount = tk.Entry(root, font=("Arial", 12), justify="center")
entry_amount.pack(pady=5)

# Buttons
btn_params = {"width": 20, "pady": 5, "font": ("Arial", 10)}
tk.Button(root, text="Check Balance", command=check_balance, **btn_params).pack(pady=5)
tk.Button(root, text="Deposit", command=deposit, bg="#e1f5fe", **btn_params).pack(pady=5)
tk.Button(root, text="Withdraw", command=withdraw, bg="#fff3e0", **btn_params).pack(pady=5)
tk.Button(root, text="View History", command=history, **btn_params).pack(pady=5)

# Output Area
result_label = tk.Label(root, text="Welcome!", wraplength=300, font=("Arial", 10, "italic"), fg="blue")
result_label.pack(pady=20)

tk.Button(root, text="Exit", command=root.quit, fg="gray", relief="flat").pack(pady=10)

root.mainloop()