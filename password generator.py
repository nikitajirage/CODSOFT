import random
import string
from tkinter import *
from tkinter import messagebox
import sqlite3

def initialize_db():
    with sqlite3.connect("user_passwords.db") as db:
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL, password TEXT NOT NULL);")
        db.commit()


class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Password Generator Tool')
        self.master.geometry('700x550')
        self.master.config(bg='#FFD700')
        self.master.resizable(False, False)
        self.username_var = StringVar()
        self.password_length_var = IntVar()
        self.generated_password_var = StringVar()

        self.create_widgets()
        self.initialize_db()

    def create_widgets(self):
        """Create and place widgets in the Tkinter window."""
        self.title_label = Label(self.master, text="Password Generator Tool", fg='darkblue', bg='#FFD700', font='Arial 20 bold')
        self.title_label.pack(pady=10)

        self.username_label = Label(self.master, text="Enter Username:", font='Arial 14', bg='#FFD700')
        self.username_label.pack(pady=5)
        self.username_entry = Entry(self.master, textvariable=self.username_var, font='Arial 14', width=30)
        self.username_entry.pack(pady=5)

        self.length_label = Label(self.master, text="Enter Password Length:", font='Arial 14', bg='#FFD700')
        self.length_label.pack(pady=5)
        self.length_entry = Entry(self.master, textvariable=self.password_length_var, font='Arial 14', width=10)
        self.length_entry.pack(pady=5)

        self.generated_label = Label(self.master, text="Generated Password:", font='Arial 14', bg='#FFD700')
        self.generated_label.pack(pady=5)
        self.generated_password_entry = Entry(self.master, textvariable=self.generated_password_var, font='Arial 14', width=30, fg='red')
        self.generated_password_entry.pack(pady=5)

        self.generate_button = Button(self.master, text="Generate Password", font='Arial 14', bg='green', fg='white', command=self.generate_password)
        self.generate_button.pack(pady=10)

        self.save_button = Button(self.master, text="Save Password", font='Arial 14', bg='blue', fg='white', command=self.save_password)
        self.save_button.pack(pady=5)

        self.reset_button = Button(self.master, text="Reset", font='Arial 14', bg='gray', fg='white', command=self.reset_fields)
        self.reset_button.pack(pady=5)

    def generate_password(self):
        """Generate a secure password based on user input."""
        username = self.username_var.get()
        password_length = self.password_length_var.get()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty!")
            return

        if not password_length or password_length < 6:
            messagebox.showerror("Error", "Password length must be at least 6 characters.")
            return

        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        digits = string.digits
        special = "!@#$%^&*()-_=+"
        
        all_chars = upper + lower + digits + special
        password = random.choices(upper, k=1) + random.choices(lower, k=1) + random.choices(digits, k=1) + random.choices(special, k=1)
        password += random.choices(all_chars, k=password_length - 4)
        random.shuffle(password)
        
        generated_password = ''.join(password)
        self.generated_password_var.set(generated_password)

    def save_password(self):
        """Save the generated password to the database."""
        username = self.username_var.get()
        password = self.generated_password_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Please generate a password before saving.")
            return

        with sqlite3.connect("user_passwords.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Error", "This username already exists! Please choose a different one.")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                db.commit()
                messagebox.showinfo("Success", "Password saved successfully.")

    def reset_fields(self):
        """Reset all input fields."""
        self.username_var.set("")
        self.password_length_var.set(0)
        self.generated_password_var.set("")
        self.username_entry.focus()

    def initialize_db(self):
        """Initialize the SQLite database and create the users table if necessary."""
        initialize_db()


if __name__ == '__main__':
    root = Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
