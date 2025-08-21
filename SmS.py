# import modules
from tkinter import *
import time
import ttkthemes
from tkinter import ttk
import pymysql
from tkinter import messagebox

# ---------------- FUNCTIONALITY ---------------------- #

def add_student():
    def add_data():
        if (
            idEntry.get() == '' or
            NameEntry.get() == '' or
            MobileNoEntry.get() == '' or
            emailEntry.get() == '' or
            addressEntry.get() == '' or
            genderEntry.get() == '' or
            dobEntry.get() == ''
        ):
            messagebox.showerror('Error', 'All fields are required', parent=addWindwow)
        else:
            currentdate = time.strftime('%Y-%m-%d')
            currenttime = time.strftime('%H:%M:%S')

            try:
                # Convert DOB to YYYY-MM-DD format
                dob = dobEntry.get().replace("/", "-")
                parts = dob.split("-")
                if len(parts[0]) != 4:  # if entered as DD-MM-YYYY
                    day, month, year = parts
                    dob = f"{year}-{month}-{day}"
            except Exception as e:
                messagebox.showerror('Error', f'Invalid date format: {e}', parent=addWindwow)
                return

            query = "INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            mycursor.execute(query, (
                idEntry.get(),
                NameEntry.get(),
                MobileNoEntry.get(),
                emailEntry.get(),
                addressEntry.get(),
                genderEntry.get(),
                dob,
                currentdate,
                currenttime
            ))
            con.commit()

            result = messagebox.askyesno(
                'Success',
                'Student added successfully. Do you want to clean the form?',
                parent=addWindwow
            )
            if result:
                idEntry.delete(0, END)
                NameEntry.delete(0, END)
                MobileNoEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
            else:
                pass
            
            query = "SELECT * FROM students"
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            for data in fetched_data:
                list_data = list(data)

    addWindwow = Toplevel()
    addWindwow.resizable(0, 0)
    addWindwow.title('Add Student')
    addWindwow.geometry('+0+0')
    addWindwow.grab_set()

    # Labels & Entries
    idLabel = Label(addWindwow, text='Id', font=('arial', 20, 'bold'))
    idLabel.grid(row=0, column=0, pady=20, padx=20, sticky='w')
    idEntry = Entry(addWindwow, font=('times new roman', 19, 'bold'), bd=2, width=20)
    idEntry.grid(row=0, column=1, pady=20, padx=20)

    NameLabel = Label(addWindwow, text='Name', font=('arial', 20, 'bold'))
    NameLabel.grid(row=1, column=0, pady=20, padx=20, sticky='w')
    NameEntry = Entry(addWindwow, font=('times new roman', 19, 'bold'), bd=2, width=20)
    NameEntry.grid(row=1, column=1, pady=20, padx=20)

    MobileNoLabel = Label(addWindwow, text='Mobile no', font=('arial', 20, 'bold'))
    MobileNoLabel.grid(row=2, column=0, pady=20, padx=20, sticky='w')
    MobileNoEntry = Entry(addWindwow, font=('times new roman', 19, 'bold'), bd=2, width=20)
    MobileNoEntry.grid(row=2, column=1, pady=20, padx=20)

    emailLabel = Label(addWindwow, text='Email', font=('arial', 20, 'bold'))
    emailLabel.grid(row=3, column=0, pady=20, padx=20, sticky='w')
    emailEntry = Entry(addWindwow, font=('times new roman', 19, 'bold'), bd=2, width=20)
    emailEntry.grid(row=3, column=1, pady=20, padx=20)

    addressLabel = Label(addWindwow, text='Address', font=('arial', 20, 'bold'))
    addressLabel.grid(row=4, column=0, pady=20, padx=20, sticky='w')
    addressEntry = Entry(addWindwow, font=('times new roman', 19, 'bold'), bd=2, width=20)
    addressEntry.grid(row=4, column=1, pady=20, padx=20)

    genderLabel = Label(addWindwow, text='Gender', font=('arial', 20, 'bold'))
    genderLabel.grid(row=5, column=0, pady=20, padx=20, sticky='w')
    genderEntry = Entry(addWindwow, font=('times new roman', 19, 'bold'), bd=2, width=20)
    genderEntry.grid(row=5, column=1, pady=20, padx=20)

    dobLabel = Label(addWindwow, text='D.O.B', font=('arial', 20, 'bold'))
    dobLabel.grid(row=6, column=0, pady=20, padx=20, sticky='w')
    dobEntry = Entry(addWindwow, font=('times new roman', 19, 'bold'), bd=2, width=20)
    dobEntry.grid(row=6, column=1, pady=20, padx=20)

    add_student_button = ttk.Button(addWindwow, text='Add Student', command=add_data)
    add_student_button.grid(row=7, columnspan=2, pady=20, padx=20)


# ---------------- Clock & Slider ---------------- #
def clock():
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)


count = 0
text = ''
def slider():
    global text, count
    if count == len(S):
        count = 0
        text = ''
    text += S[count]
    sliderlabel.config(text=text)
    count += 1
    sliderlabel.after(100, slider)


# ---------------- Database Connection ---------------- #
def connect_database():
    connectWindow = Toplevel()
    connectWindow.title('Database Connection')
    connectWindow.geometry('500x350+720+230')
    connectWindow.resizable(0, 0)
    connectWindow.grab_set()

    hostnameLabel = Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, pady=20, padx=20)
    hostEntry = Entry(connectWindow, font=('times new roman', 19, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, pady=20, padx=20)

    UsernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    UsernameLabel.grid(row=1, column=0, pady=20, padx=20)
    UserEntry = Entry(connectWindow, font=('times new roman', 19, 'bold'), bd=2)
    UserEntry.grid(row=1, column=1, pady=20, padx=20)

    PasswordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    PasswordLabel.grid(row=2, column=0, pady=20, padx=20)
    PasswordEntry = Entry(connectWindow, font=('times new roman', 19, 'bold'), bd=2, show="*")
    PasswordEntry.grid(row=2, column=1, pady=20, padx=20)

    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(
                host='localhost',
                user='root',
                password='Admin123'
            )
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Please enter correct credentials', parent=connectWindow)
            return

        query = "CREATE DATABASE IF NOT EXISTS student_management"
        mycursor.execute(query)
        query = "USE student_management"
        mycursor.execute(query)
        query = '''CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            Name VARCHAR(100), 
            mobile_no VARCHAR(15), 
            email VARCHAR(100), 
            address TEXT, 
            gender VARCHAR(10), 
            dob DATE, 
            added_date DATE, 
            added_time TIME
        )'''
        mycursor.execute(query)
        messagebox.showinfo('Success', 'Database connected successfully', parent=connectWindow)
        connectWindow.destroy()

        # Enable buttons
        addStudentButton.config(state=NORMAL)
        searchButton.config(state=NORMAL)
        DeleteStudentButton.config(state=NORMAL)
        UpdateStudentButton.config(state=NORMAL)
        ShowStudentButton.config(state=NORMAL)
        ExportStudentButton.config(state=NORMAL)

    connectButton = ttk.Button(connectWindow, text='Connect', command=connect)
    connectButton.grid(row=3, columnspan=2, pady=20)


# ---------------- GUI ---------------- #
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x750+0+0')
root.title('Student Management System')
root.resizable(0, 0)

# Date and time label
datetimeLabel = Label(root, font=('times new roman', 15, 'bold'))
datetimeLabel.place(x=5, y=10)
clock()

# Slider
S = 'Student Management System'
sliderlabel = Label(root, font=('Arial', 29, 'italic bold'), width=30)
sliderlabel.place(x=200, y=0)
slider()

# Connect Database button
connectButton = ttk.Button(root, text='Connect Database', command=connect_database)
connectButton.place(x=1000, y=20)

# Left Frame
leftFrame = Frame(root)
leftFrame.place(x=50, y=90, width=300, height=600)

try:
    LogoImageLeft = PhotoImage(file='students.png')
    logo_label = Label(leftFrame, image=LogoImageLeft)
    logo_label.grid(row=0, column=0)
except:
    logo_label = Label(leftFrame, text="Logo Here", font=("Arial", 20))
    logo_label.grid(row=0, column=0)

addStudentButton = ttk.Button(leftFrame, text='Add Student', width=20, state=DISABLED, command=add_student)
addStudentButton.grid(row=1, column=0, pady=16)

searchButton = ttk.Button(leftFrame, text='Search Student', width=20, state=DISABLED)
searchButton.grid(row=2, column=0, pady=16)

DeleteStudentButton = ttk.Button(leftFrame, text='Delete Student', width=20, state=DISABLED)
DeleteStudentButton.grid(row=3, column=0, pady=16)

UpdateStudentButton = ttk.Button(leftFrame, text='Update Student', width=20, state=DISABLED)
UpdateStudentButton.grid(row=4, column=0, pady=16)

ShowStudentButton = ttk.Button(leftFrame, text='Show Student', width=20, state=DISABLED)
ShowStudentButton.grid(row=5, column=0, pady=16)

ExportStudentButton = ttk.Button(leftFrame, text='Export Student', width=20, state=DISABLED)
ExportStudentButton.grid(row=6, column=0, pady=16)

ExitStudentButton = ttk.Button(leftFrame, text='Exit Student', width=20, command=root.destroy)
ExitStudentButton.grid(row=7, column=0, pady=16)

# Right Frame
RightFrame = Frame(root)
RightFrame.place(x=350, y=90, width=800, height=600)

scrollbarX = Scrollbar(RightFrame, orient=HORIZONTAL)
scrollbarY = Scrollbar(RightFrame, orient=VERTICAL)

StudentTable = ttk.Treeview(
    RightFrame,
    columns=('ID','Name','Mobile No','email','Address','Gender','DOB','Added Date','Added Time'),
    xscrollcommand=scrollbarX.set,
    yscrollcommand=scrollbarY.set
)

scrollbarX.config(command=StudentTable.xview)
scrollbarY.config(command=StudentTable.yview)
scrollbarX.pack(side=BOTTOM, fill=X)
scrollbarY.pack(side=RIGHT, fill=Y)

StudentTable.pack(fill=BOTH, expand=1)

# Headings
StudentTable.heading('ID', text='Id')
StudentTable.heading('Name', text='Name')
StudentTable.heading('Mobile No', text='Mobile No')
StudentTable.heading('email', text='Email')
StudentTable.heading('Address', text='Address')
StudentTable.heading('Gender', text='Gender')
StudentTable.heading('DOB', text='D.O.B')
StudentTable.heading('Added Date', text='Date Added')
StudentTable.heading('Added Time', text='Time Added')
StudentTable.config(show='headings')

root.mainloop()
