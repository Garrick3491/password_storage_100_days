from tkinter import *
from tkinter import messagebox
import password_chars
from random import choice, randint, shuffle
import pyperclip
import json


def load_website():
    website = website_entry.get()
    try:
        with open("save_me.json", "r") as data_file:
            data_from_file = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Whoops!", message=f"No Data has been saved!")
    else:
        if website in data_from_file:
            email = data_from_file[website]['email']
            password = data_from_file[website]['password']
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Whoops!", message=f"No data found for {website}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_letters = [choice(password_chars.letters) for _ in range(randint(10, 15))]
    password_numbers = [choice(password_chars.numbers) for _ in range(randint(5, 6))]
    password_symbols = [choice(password_chars.symbols) for _ in range(randint(5, 6))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password_entry.insert(0, "".join(password_list))
    pyperclip.copy("".join(password_list))
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="oops", message="Please make sure you haven't left any fields empty.")

    else:
        confirmed = messagebox.askokcancel(title=website, message=f"There are the details entered: "
                                                  f"\nEmail: {email} "
                                                  f"\nPassword: {password} "
                                                  f"\nIs it ok to save?")

        if confirmed:
            data = {
                website: {
                    'website': website,
                    'email': email,
                    'password': password
                }
            }

            try:
                with open("save_me.json", "r") as data_file:
                    data_from_file = json.load(data_file)
            except FileNotFoundError:
                with open("save_me.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            else:
                data_from_file.update(data)
                with open("save_me.json", "w") as data_file:
                    json.dump(data_from_file, data_file, indent=4)
            website_entry.delete(0, END)
            password_entry.delete(0, END)
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

#Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

#Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "name@email.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
search_button = Button(text="Search", command=load_website)
search_button.grid(row=1, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()