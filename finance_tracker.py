import tkinter as tk
from tkinter import messagebox

# Transaction list storage
transactions = []
budget_limit = 0  

def update_summary():
    total_income = sum(t["amount"] for t in transactions if t["type"] == "Income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    balance = total_income - total_expense

    income_label.config(text=f"Total Income: ₦{total_income:,.2f}")
    expense_label.config(text=f"Total Expenses: ₦{total_expense:,.2f}")
    balance_label.config(text=f"Balance: ₦{balance:,.2f}")

    if budget_limit and total_expense > budget_limit:
        messagebox.showwarning("Budget Alert!", f"Warning! Expenses exceeded the budget limit of ₦{budget_limit:,.2f}!")

#  update the category filter dropdown
def update_category_filter():
    categories = {"All"} | {t["category"] for t in transactions}  
    filter_menu["menu"].delete(0, "end")  
    for category in categories:
        filter_menu["menu"].add_command(label=category, command=tk._setit(filter_var, category))
    filter_var.set("All")  

# add a new transaction
def add_transaction():
    t_type = type_var.get()
    category = category_entry.get()
    amount = amount_entry.get()
    date = date_entry.get()

    if not category or not amount or not date:
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number!")
        return
    
    transactions.append({"type": t_type, "category": category, "amount": amount, "date": date})
    update_summary()
    update_transaction_list()
    update_category_filter()  
    clear_inputs()

#  update the transaction list display
def update_transaction_list():
    transaction_listbox.delete(0, tk.END)
    for t in transactions:
        transaction_listbox.insert(tk.END, f"{t['date']} - {t['type']} - {t['category']}: ₦{t['amount']:,.2f}")

#  clear input fields
def clear_inputs():
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

#  delete a selected transaction
def delete_transaction():
    selected = transaction_listbox.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "No transaction selected!")
        return
    transactions.pop(selected[0])
    update_summary()
    update_transaction_list()
    update_category_filter()  

#  filter transactions by category
def filter_transactions():
    selected_category = filter_var.get()
    transaction_listbox.delete(0, tk.END)
    
    for t in transactions:
        if selected_category == "All" or t["category"] == selected_category:
            transaction_listbox.insert(tk.END, f"{t['date']} - {t['type']} - {t['category']}: ₦{t['amount']:,.2f}")

#  set the budget limit
def set_budget():
    global budget_limit
    try:
        budget_limit = float(budget_entry.get())
        messagebox.showinfo("Budget Set", f"Budget limit set to ₦{budget_limit:,.2f}")
        update_summary()
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid budget amount!")

# Main Window
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("500x600")
root.configure(bg="#2C3E50")  


frame = tk.Frame(root, bg="#34495E", padx=10, pady=10)
frame.pack(pady=10, padx=10, fill="both", expand=True)

# Title Label
title_label = tk.Label(frame, text="💰 My Personal Finance Tracker", font=("Arial", 16, "bold"), fg="white", bg="#2980B9", pady=5)
title_label.pack(fill="x")

input_frame = tk.Frame(frame, bg="#34495E")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Category:", fg="white", bg="#34495E").grid(row=0, column=0, sticky="w", padx=5, pady=3)
category_entry = tk.Entry(input_frame, bg="white", fg="black")
category_entry.grid(row=0, column=1, pady=3)

tk.Label(input_frame, text="Amount (₦):", fg="white", bg="#34495E").grid(row=1, column=0, sticky="w", padx=5, pady=3)
amount_entry = tk.Entry(input_frame, bg="white", fg="black")
amount_entry.grid(row=1, column=1, pady=3)

tk.Label(input_frame, text="Date (YYYY-MM-DD):", fg="white", bg="#34495E").grid(row=2, column=0, sticky="w", padx=5, pady=3)
date_entry = tk.Entry(input_frame, bg="white", fg="black")
date_entry.grid(row=2, column=1, pady=3)

# Type (Income/Expense)
type_var = tk.StringVar(value="Expense")
tk.Label(input_frame, text="Type:", fg="white", bg="#34495E").grid(row=3, column=0, sticky="w", padx=5, pady=3)
tk.Radiobutton(input_frame, text="Income", variable=type_var, value="Income", bg="#34495E", fg="white").grid(row=3, column=1)
tk.Radiobutton(input_frame, text="Expense", variable=type_var, value="Expense", bg="#34495E", fg="white").grid(row=3, column=2)

# Buttons
button_frame = tk.Frame(frame, bg="#34495E")
button_frame.pack(pady=5)

tk.Button(button_frame, text="➕ Add Transaction", command=add_transaction, bg="#27AE60", fg="white", width=18).pack(side="left", padx=5)
tk.Button(button_frame, text="❌ Delete Transaction", command=delete_transaction, bg="#C0392B", fg="white", width=18).pack(side="left", padx=5)

# Transaction List
transaction_listbox = tk.Listbox(frame, width=50, bg="white", fg="black", selectbackground="#F39C12")
transaction_listbox.pack(pady=10)

# Filter Transactions
filter_frame = tk.Frame(frame, bg="#34495E")
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Filter by Category:", fg="white", bg="#34495E").grid(row=0, column=0, padx=5)
filter_var = tk.StringVar(value="All")
filter_menu = tk.OptionMenu(filter_frame, filter_var, "All")
filter_menu.grid(row=0, column=1, padx=5)
tk.Button(filter_frame, text="Apply Filter", command=filter_transactions, bg="#3498DB", fg="white").grid(row=0, column=2, padx=5)

# Summary Labels
summary_frame = tk.Frame(frame, bg="#34495E")
summary_frame.pack(pady=5)

income_label = tk.Label(summary_frame, text="Total Income: ₦0", fg="white", bg="#2ECC71", font=("Arial", 10, "bold"), pady=2)
income_label.pack(fill="x", padx=10)

expense_label = tk.Label(summary_frame, text="Total Expenses: ₦0", fg="white", bg="#E74C3C", font=("Arial", 10, "bold"), pady=2)
expense_label.pack(fill="x", padx=10)

balance_label = tk.Label(summary_frame, text="Balance: ₦0", fg="white", bg="#F1C40F", font=("Arial", 10, "bold"), pady=2)
balance_label.pack(fill="x", padx=10)

# Run the app
root.mainloop()
