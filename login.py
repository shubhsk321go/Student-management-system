
# import multiple modules
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

#Actions commands and check of the fields in the page
def login():
    if usernameEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Error', "Fields can't be empty")
    elif usernameEntry.get()=='Shubham' and passwordEntry.get()=='12345':
        messagebox.showinfo('Success', 'Welcome')
        Window.destroy()
        import SmS
        
    else:
        messagebox.showerror('Error', 'Please enter correct credentials')

#creating a windows for the app
Window=Tk() # module and its object name to use in the code section
Window.geometry('1400x750+0+0') #size of the app
Window.title('LogIn system of Student Management Software')
Window.resizable(False, False) #resizing disabled manually

#background image of the app
backgroundImage=ImageTk.PhotoImage(file='1.jpg') #imported the module and photo for the background image 
bgLabel=Label(Window, image=backgroundImage)
bgLabel.place(x=0, y=0)

#login frame created
LoginFrame=Frame(Window)
LoginFrame.place(x=650, y=230)

# login image added to frame 
logoimage= PhotoImage(file='loginlogo1.png')
logolabel=Label(LoginFrame, image=logoimage) #login lable created 
logolabel.grid(row=0, column=0, columnspan=2, pady=10)

usernamepic=PhotoImage(file='username.png')
usernameLabel=Label(LoginFrame, image=usernamepic, text='UserName', compound=LEFT
                    , font=('Times new roman', 17, 'bold'))
usernameLabel.grid(row=1, column=0, pady=10, padx=20)

usernameEntry=Entry(LoginFrame, font=('Times new roman', 17, 'bold'),bd=5)
usernameEntry.grid(row=1, column=1, pady=10, padx=20)

passwordpic=PhotoImage(file='padlock.png')
passwordLabel=Label(LoginFrame, image=passwordpic, text='Password', compound=LEFT
                    , font=('Times new roman', 17, 'bold'))
passwordLabel.grid(row=2, column=0, pady=10, padx=20)

passwordEntry=Entry(LoginFrame, font=('Times new roman', 17, 'bold'), bd=5)
passwordEntry.grid(row=2, column=1, pady=10, padx=20)


LoginButton=Button(LoginFrame, text='LogIn', font=('Times new roman', 14, 'bold'),width=15
                   , fg='white', bg='royalblue', activebackground='royalblue', activeforeground='white',
                   cursor='hand2', command=login)
LoginButton.grid(row=3, column=0, columnspan=2, pady=10)

#GUI ends here and start of the actions in the app

Window.mainloop()