import tkinter as tk
from tkinter import messagebox
import json

def save_user_data(email, password, city):
    data = {
        "email": email,
        "password": password,
        "city": city
    }
    with open("user_config.json", "w") as config_file:
        json.dump(data, config_file)
    messagebox.showinfo("Setup Complete", "Your information has been saved!")

def setup_wizard():
    # Create the main window
    root = tk.Tk()
    root.title("Northern Lights Alerts - Setup Wizard")

    # Labels and entry fields
    tk.Label(root, text="Email:").grid(row=0, column=0, padx=10, pady=5)
    email_entry = tk.Entry(root, width=30)
    email_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(root, show="*", width=30)
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="City:").grid(row=2, column=0, padx=10, pady=5)
    city_entry = tk.Entry(root, width=30)
    city_entry.grid(row=2, column=1, padx=10, pady=5)

    # Save button
    tk.Button(root, text="Save", command=lambda: save_user_data(
        email_entry.get(), password_entry.get(), city_entry.get()
    )).grid(row=3, column=0, columnspan=2, pady=10)

    # Run the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    setup_wizard()
