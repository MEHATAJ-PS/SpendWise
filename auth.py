import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import json
import os
from dashboard import Dashboard

class AuthWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SpendWise - Login/Register")
        self.geometry("400x300")
        self.resizable(False, False)

        # UI Elements
        ctk.CTkLabel(self, text="Username").pack(pady=5)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Password").pack(pady=5)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.pack(pady=5)

        # Ensure user data file exists
        os.makedirs("data", exist_ok=True)
        if not os.path.exists("data/users.json"):
            with open("data/users.json", "w") as f:
                json.dump({}, f)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required.")
            return

        try:
            with open("data/users.json", "r") as f:
                users = json.load(f)

            if username in users and users[username] == password:
                self.destroy()
                Dashboard(username=username).mainloop()
            elif username not in users:
                messagebox.showerror("Error", "User not registered.")
            else:
                messagebox.showerror("Error", "Incorrect password.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "User database corrupted.")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required.")
            return

        try:
            with open("data/users.json", "r") as f:
                users = json.load(f)
        except json.JSONDecodeError:
            users = {}

        if username in users:
            messagebox.showerror("Error", "User already exists.")
            return

        users[username] = password
        with open("data/users.json", "w") as f:
            json.dump(users, f)

        messagebox.showinfo("Success", "Registration successful. Please login.")
