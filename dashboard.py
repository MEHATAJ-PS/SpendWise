import tkinter as tk
import customtkinter as ctk
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Dashboard(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title(f"SpendWise - {username}")
        self.geometry("1050x700")
        self.data_file = f"data/{self.username}_expenses.json"
        os.makedirs("data", exist_ok=True)
        self.expenses = self.load_expenses()

        # Layout: Sidebar + Main Area
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Sidebar Buttons
        ctk.CTkLabel(self.sidebar, text=f"Welcome\n{username}", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Dashboard", command=self.show_dashboard).pack(pady=5, fill="x")
        ctk.CTkButton(self.sidebar, text="Pie Chart", command=self.show_pie_chart).pack(pady=5, fill="x")
        ctk.CTkButton(self.sidebar, text="Daily Chart", command=self.show_daily_chart).pack(pady=5, fill="x")
        ctk.CTkButton(self.sidebar, text="Monthly Chart", command=self.show_monthly_chart).pack(pady=5, fill="x")
        ctk.CTkButton(self.sidebar, text="Yearly Chart", command=self.show_yearly_chart).pack(pady=5, fill="x")

        self.show_dashboard()

    def load_expenses(self):
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_expenses(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.expenses, f, indent=2)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_frame()

        # Form Inputs
        self.amount_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Amount")
        self.amount_entry.pack(pady=5)

        self.category_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Category")
        self.category_entry.pack(pady=5)

        today = datetime.today()
        self.year_var = tk.StringVar(value=str(today.year))
        self.month_var = tk.StringVar(value=str(today.month).zfill(2))
        self.day_var = tk.StringVar(value=str(today.day).zfill(2))

        date_frame = ctk.CTkFrame(self.main_frame)
        date_frame.pack(pady=5)

        years = [str(y) for y in range(2020, today.year + 1)]
        months = [str(m).zfill(2) for m in range(1, 13)]
        days = [str(d).zfill(2) for d in range(1, 32)]

        ctk.CTkComboBox(date_frame, values=years, variable=self.year_var, width=80).pack(side="left", padx=2)
        ctk.CTkComboBox(date_frame, values=months, variable=self.month_var, width=80).pack(side="left", padx=2)
        ctk.CTkComboBox(date_frame, values=days, variable=self.day_var, width=80).pack(side="left", padx=2)

        ctk.CTkButton(self.main_frame, text="Add Expense", command=self.add_expense).pack(pady=10)

        # Expense List
        self.expense_frame = ctk.CTkScrollableFrame(self.main_frame, height=300)
        self.expense_frame.pack(fill="both", expand=False, padx=10, pady=10)
        self.refresh_expense_list()

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        year = self.year_var.get()
        month = self.month_var.get()
        day = self.day_var.get()

        try:
            date_str = f"{year}-{month}-{day}"
            datetime.strptime(date_str, '%Y-%m-%d')
            amount = float(amount)
        except:
            return  # Invalid entry

        self.expenses.append({"amount": amount, "category": category, "date": date_str})
        self.save_expenses()
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.refresh_expense_list()

    def delete_expense(self, index):
        del self.expenses[index]
        self.save_expenses()
        self.refresh_expense_list()

    def refresh_expense_list(self):
        for widget in self.expense_frame.winfo_children():
            widget.destroy()
        for idx, item in enumerate(self.expenses):
            row = ctk.CTkFrame(self.expense_frame)
            row.pack(fill="x", padx=5, pady=2)

            label = f"{item['date']} | ₹{item['amount']} | {item['category']}"
            ctk.CTkLabel(row, text=label, anchor="w").pack(side="left", expand=True)
            ctk.CTkButton(row, text="Delete", width=60, fg_color="red",
                          command=lambda i=idx: self.delete_expense(i)).pack(side="right", padx=5)

    def show_pie_chart(self):
        data = {}
        for item in self.expenses:
            cat = item['category']
            data[cat] = data.get(cat, 0) + item['amount']

        if not data:
            return

        self.display_chart(lambda ax: ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=140),
                           title="Pie Chart by Category")

    def show_monthly_chart(self):
        data = {}
        for item in self.expenses:
            month = item['date'][:7]
            data[month] = data.get(month, 0) + item['amount']

        if not data:
            return

        months = sorted(data.keys())
        values = [data[m] for m in months]

        self.display_chart(lambda ax: ax.bar(months, values),
                           title="Monthly Expense Chart", xlabel="Month", ylabel="Amount")

    def show_yearly_chart(self):
        data = {}
        for item in self.expenses:
            year = item['date'][:4]
            data[year] = data.get(year, 0) + item['amount']

        if not data:
            return

        years = sorted(data.keys())
        values = [data[y] for y in years]

        self.display_chart(lambda ax: ax.bar(years, values),
                           title="Yearly Expense Chart", xlabel="Year", ylabel="Amount")

    def show_daily_chart(self):
        data = {}
        for item in self.expenses:
            day = item['date']
            data[day] = data.get(day, 0) + item['amount']

        if not data:
            return

        days = sorted(data.keys())
        values = [data[d] for d in days]

        self.display_chart(lambda ax: ax.plot(days, values, marker='o'),
                           title="Daily Expense Chart", xlabel="Date", ylabel="Amount")

    def display_chart(self, chart_func, title="", xlabel="", ylabel=""):
        self.clear_main_frame()
        fig, ax = plt.subplots(figsize=(7, 5))
        chart_func(ax)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


# Run this directly
if __name__ == "__main__":
    app = Dashboard(username="testuser")
    app.mainloop()
