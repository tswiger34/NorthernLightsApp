from utils.logging_config import *
import tkinter as tk
from tkinter import messagebox
import json
import os
logger = setup_logging()
class SetupWizard:
    """
    This class is used for the setup wizard which the user interacts with to save their information including
    their alert preferences, email, location, phone number, and time zone

    Methods:
    - launch_setup_wizard:
    - save_user_data:
    - setup_wizard:
    
    Attributes:
    - config_dir (str): the root directory where the configuration file is stored
    - config_path (str): The file path for the configuration file
    - root (Tk): The top level widget created by Tkinter

    """
    def __init__(self):
        self.config_dir = os.path.expanduser(r"~\.northern_lights_alert")
        self.config_path = os.path.join(self.config_dir, "data/user_config.json")
        self.launch_setup_wizard()
    
    def launch_setup_wizard(self):
        """
        Responsible for initializing and launching the setup wizard on the users screen.
        """
        # Create the setup wizard window
        self.root = tk.Tk()
        self.root.title("Northern Lights Alert - Setup Wizard")
        self.setup_wizard()
        self.root.mainloop()

    def save_user_data(self, email:str, password:str, city:str) -> None:
        """
        Saves the user data as a json file in the specified path, which the user inputs to the wizard. 
        Makes the directory if it does not exist.
        """
        os.makedirs(self.config_dir, exist_ok=True)
        data_dir = f"{self.config_dir}/data"
        os.makedirs(data_dir, exist_ok=True)
        data = {
            "TextAlerts": 0,
            "EmailAlerts":1,
            "Email": email,
            "APP_PASS": password,
            "City": city
        }

        with open(self.config_path, "w") as config_file:
            json.dump(data, config_file)
        messagebox.showinfo("Setup Complete", "Your information has been saved!")
        try:
            self.root.destroy()
        except Exception as e:
            logger.warning(f"There was an exception: {e}")
            return

    def setup_wizard(self) -> None:
        """
        Specifies the fields of the setup wizard and how the user interacts with it.
        """
        # Create the main window
        self.root.title("Northern Lights Alerts - Setup Wizard")

        # Labels and entry fields
        tk.Label(self.root, text="Email:").grid(row=0, column=0, padx=10, pady=5)
        email_entry = tk.Entry(self.root, width=30)
        email_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        password_entry = tk.Entry(self.root, show="*", width=30)
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="City:").grid(row=2, column=0, padx=10, pady=5)
        city_entry = tk.Entry(self.root, width=30)
        city_entry.grid(row=2, column=1, padx=10, pady=5)

        # Save button
        tk.Button(self.root, text="Save", command=lambda: self.save_user_data(
            email_entry.get(), password_entry.get(), city_entry.get()
        )).grid(row=3, column=0, columnspan=2, pady=10)

        # Run the GUI event loop
        self.root.mainloop()