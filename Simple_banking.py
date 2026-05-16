import tkinter as tk
from datetime import datetime
import os

class BankAccount:
    def __init__(self, filename="transactions.txt"):
        self.filename = filename
        self.balance = self._load_balance()

    def _save_transaction(self, trans_type, amount):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"{ts} | {trans_type} | Amount: ₹{amount} | Balance: ₹{self.balance}\n")

    def _load_balance(self):
        if not os.path.exists(self.filename):
            return 0
        try:
            lines = open(self.filename, encoding="utf-8").readlines()
            if lines and "Balance:" in lines[-1]:
                return int(lines[-1].strip().split("Balance: ₹")[1])
        except Exception:
            pass
        return 0

    def deposit(self, amount):
        self.balance += amount
        self._save_transaction("Deposit", amount)
        return True, f"Deposited ₹{amount} successfully!"

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self._save_transaction("Withdraw", amount)
            return True, "Withdraw successful"
        return False, "Insufficient balance"

    def get_balance(self): return self.balance

    def get_history(self):
        try:
            if not os.path.exists(self.filename):
                return "No transactions found."
            content = open(self.filename, encoding="utf-8").read()
            return content or "No transactions found."
        except Exception:
            return "Error reading history."


class BankingApp:
    def __init__(self, root):
        self.root = root
        self.account = BankAccount()
        root.title("Simple Banking")
        root.geometry("350x450")
        root.configure(padx=20, pady=20)
        self._create_widgets()

    def _create_widgets(self):
        tk.Label(self.root, text="BANKING SYSTEM", font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(self.root, text="Enter Amount (₹):").pack(pady=(10, 0))
        self.entry = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry.pack(pady=5)

        bp = {"width": 20, "pady": 5, "font": ("Arial", 10)}
        tk.Button(self.root, text="Check Balance",  command=self.check_balance,               **bp).pack(pady=5)
        tk.Button(self.root, text="Deposit",        command=self.deposit,  bg="#e1f5fe",      **bp).pack(pady=5)
        tk.Button(self.root, text="Withdraw",       command=self.withdraw, bg="#fff3e0",      **bp).pack(pady=5)
        tk.Button(self.root, text="View History",   command=self.show_history,                **bp).pack(pady=5)

        self.result = tk.Label(self.root, text="Welcome!", wraplength=300,
                               font=("Arial", 10, "italic"), fg="blue")
        self.result.pack(pady=20)
        tk.Button(self.root, text="Exit", command=self.root.quit, fg="gray", relief="flat").pack(pady=10)

    def _get_amount(self):
        try:
            a = int(self.entry.get().strip())
            return a if a > 0 else None
        except ValueError:
            return None

    def _show(self, msg, color): self.result.config(text=msg, fg=color)

    def check_balance(self): self._show(f"Current Balance: ₹{self.account.get_balance()}", "black")

    def deposit(self):
        a = self._get_amount()
        if a is None: self._show("Enter valid positive amount", "red"); return
        ok, msg = self.account.deposit(a)
        self._show(msg, "green" if ok else "red")
        self.entry.delete(0, tk.END)

    def withdraw(self):
        a = self._get_amount()
        if a is None: self._show("Enter valid positive amount", "red"); return
        ok, msg = self.account.withdraw(a)
        self._show(msg, "green" if ok else "red")
        if ok: self.entry.delete(0, tk.END)

    def show_history(self):
        win = tk.Toplevel(self.root)
        win.title("Transaction History")
        tk.Label(win, text="Transaction History", font=("Arial", 12, "bold")).pack(pady=10)
        txt = tk.Text(win, height=15, width=55)
        txt.insert(tk.END, self.account.get_history())
        txt.config(state="disabled")
        txt.pack(padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    BankingApp(root)
    root.mainloop()