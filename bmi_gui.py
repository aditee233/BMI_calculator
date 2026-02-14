import sqlite3
from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime

# -------- DATABASE -------- #

conn = sqlite3.connect("bmi_data.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS bmi_records(
name TEXT,
height REAL,
weight REAL,
bmi REAL,
category TEXT,
date TEXT
)
""")
conn.commit()

# -------- FUNCTIONS -------- #

def calculate_bmi():

    try:
        name = name_entry.get()
        height = float(height_entry.get())
        weight = float(weight_entry.get())

        if name == "":
            messagebox.showerror("Error","Enter name")
            return

        if height <= 0 or weight <= 0:
            messagebox.showerror("Error","Invalid height or weight")
            return

        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        result.set(f"BMI: {bmi} ({category})")

        cur.execute("INSERT INTO bmi_records VALUES (?,?,?,?,?,?)",
                    (name,height,weight,bmi,category,str(datetime.now())))

        conn.commit()

    except:
        messagebox.showerror("Error","Enter valid numbers")


def show_history():

    name = name_entry.get()

    if name == "":
        messagebox.showerror("Error","Enter name first")
        return

    cur.execute("SELECT bmi,date FROM bmi_records WHERE name=?", (name,))
    data = cur.fetchall()

    if not data:
        messagebox.showinfo("Info","No records found")
        return

    hist = Toplevel()
    hist.title("BMI History")

    for row in data:
        Label(hist,text=f"{row[1][:16]}  BMI: {row[0]}").pack()


def show_graph():

    name = name_entry.get()

    if name == "":
        messagebox.showerror("Error","Enter name first")
        return

    cur.execute("SELECT bmi FROM bmi_records WHERE name=?", (name,))
    data = cur.fetchall()

    if not data:
        messagebox.showinfo("Info","No data to plot")
        return

    bmi_vals = [x[0] for x in data]

    plt.plot(bmi_vals,marker="o")
    plt.title(f"{name}'s BMI Trend")
    plt.xlabel("Attempts")
    plt.ylabel("BMI")
    plt.show()

# -------- GUI -------- #

root = Tk()
root.title("Advanced BMI Calculator")
root.geometry("350x360")

Label(root,text="Advanced BMI Calculator",font=("Arial",14)).pack(pady=5)

Label(root,text="Name").pack()
name_entry = Entry(root)
name_entry.pack()

Label(root,text="Height (cm)").pack()
height_entry = Entry(root)
height_entry.pack()

Label(root,text="Weight (kg)").pack()
weight_entry = Entry(root)
weight_entry.pack()

Button(root,text="Calculate BMI",command=calculate_bmi).pack(pady=5)

result = StringVar()
Label(root,textvariable=result,font=("Arial",12)).pack(pady=5)

Button(root,text="View History",command=show_history).pack(pady=5)
Button(root,text="Show BMI Graph",command=show_graph).pack(pady=5)

root.mainloop()
