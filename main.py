import tkinter
from tkinter import messagebox
import pyperclip
import json
import os


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_random_password():
    # Password Generator Project
    import random

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q',
               'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    return ''.join(password_list)


def password_gen():  # generate random password based on some rules
    password_entry.delete(0, tkinter.END)
    new_password = generate_random_password()
    password_entry.insert(tkinter.END, new_password)
    pyperclip.copy(new_password)  # copy that password into clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()

    # codes to save data into json. create a dictionary
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    # shows warning if either username/email or password is empty
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="WARNING", message="Please don't leave any field EMPTY!")
    else:
        # create some dialogue pop-up to make sure the user wants to save the info
        is_ok = messagebox.askokcancel(title=f"Website: {website}", message=f"These are details entered:\n"
                                                                            f"    - Username/Email: {email}\n"
                                                                            f"    - Password: {password}\n"
                                                                            f"Is it ok to save?")
        if is_ok:
            # clear out the 2 fields from beginning to end
            data = new_data
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)  # reading old data
                    data.update(new_data)  # update the old data with new one
            except FileNotFoundError:  # ignore if the file is not created because below create the file
                pass
            finally:  # create a new file anyway
                with open("data.json", "w") as file:  # append to the end of file
                    website_entry.delete(first=0, last=tkinter.END)
                    password_entry.delete(first=0, last=tkinter.END)
                    website_entry.focus()
                    json.dump(data, file, indent=4)
                    messagebox.showinfo(title="Password saved", message=f"Password saved to file: {file.name}")


# ---------------------------- DELETE PASSWORD ------------------------------- #
def delete():
    is_ok = messagebox.askyesno(title="Delete All Saved Passwords", message="Are you sure to delete all of them?")
    if is_ok:
        try:
            # os.remove("data.txt")
            os.remove("data.json")
        except FileNotFoundError:
            messagebox.showinfo(title="Passwords Deleted", message="All password saved has already been deleted")


# ---------------------------- SEARCH WEBSITE ------------------------------- #
def search():
    website = website_entry.get().title()  # get website that user inputted
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]

            # delete the old inputted field
            website_entry.delete(0, tkinter.END)
            email_entry.delete(0, tkinter.END)
            password_entry.delete(0, tkinter.END)

            # insert the saved website, email and password to the field
            website_entry.insert(0, website)
            email_entry.insert(0, email)
            password_entry.insert(0, password)
            # show popup for password found
            messagebox.showinfo(title="Website Found",
                                message=f"Saved password from your website: {website.upper()} has been found!")
        else:
            messagebox.showwarning(title="Website Not Found",
                                   message=f"No password for website '{website.upper()}' found")


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.config(padx=30, pady=20)
window.title("PASSWORD MANAGER")

# create the logo
canvas = tkinter.Canvas(width=200, height=189, highlightthickness=0)
canvas_img = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 99, image=canvas_img)  # place the image at x = 100, y = 100
canvas.grid(row=0, column=1, padx=20, pady=20)

# create field for user to input their website
website_label = tkinter.Label(text="Website:")
website_label.grid(row=1, column=0)
website_entry = tkinter.Entry(width=24)
website_entry.focus()
website_entry.grid(row=1, column=1)

# create field for user to input email/user_name
email_label = tkinter.Label(text="Email/Username:")
email_label.grid(row=2, column=0)
email_entry = tkinter.Entry(width=49)
email_entry.grid(row=2, column=1, columnspan=2)  # start at column 1, extend 2 columns

# create a field to input password and a button to generate random password
password_label = tkinter.Label(text="Password:")
password_label.grid(row=3, column=0)
password_entry = tkinter.Entry(width=24)
password_entry.grid(row=3, column=1)

password_button = tkinter.Button(text="Generate Password", command=password_gen, width=20)
password_button.grid(row=3, column=2)

# button to add all data to save in a file
add_button = tkinter.Button(text="Add", width=42, command=save)
add_button.grid(row=4, column=1, columnspan=2)

# button to delete all saved password
delete_button = tkinter.Button(text="Delete All Saved Password!", width=42, command=delete)
delete_button.grid(row=5, column=1, columnspan=2)

# button to search the info according to the website
search_button = tkinter.Button(text="Search Email/Password", command=search, width=20)
search_button.grid(row=1, column=2)

window.mainloop()
