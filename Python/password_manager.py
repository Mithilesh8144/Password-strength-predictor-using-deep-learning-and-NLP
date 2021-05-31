from tkinter import*
import sqlite3, hashlib
from tkinter.ttk import *
from tkinter import ttk

from tkinter import messagebox
from tkinter import simpledialog
from functools import partial
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

#DATABASE PART
#DATABASE ONE IS FOR STORING USERS WHERE THE USERNAME IS A PRIMARY KEY
with sqlite3.connect('Password_manager.db') as db:
    cursor=db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS USERS_(
username TEXT PRIMARY KEY,
password TEXT NOT NULL);
""")
#DATABASE TWO IS FOR STORING WEBSITE INFORMATION WHILE HAVING A FOREIGN KEY REFERENCE TO THE USERS_ DB
command2="""CREATE TABLE IF NOT EXISTS 
PASSWORDS_(

USER TEXT,
website TEXT,
userid TEXT ,
password TEXT NOT NULL,
FOREIGN KEY(USER) REFERENCES USERS_(username))"""

cursor.execute(command2)

#load tokenizer and model 
with open('lstm_passwrd2.pickle', 'rb') as handle:
    tokenizer2 = pickle.load(handle)
model=load_model('PASSWORD_STRENGTH2.h5')



window=Tk()
s=ttk.Style()
s.theme_use('clam')


window.title("PASSWORD MANAGER")

window.geometry("200x300")

def popUp(text):
    output=simpledialog.askstring("input string",text)
    return output

def hashpassword(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()
    return hash

#function to handle when the user wants to log in
def existing_user():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("200x300")
    label1=Label(window,text="Enter the username")
    label1.config(anchor=CENTER)
    label1.pack()

    txt1=Entry(window, width=30)
    txt1.focus()
    txt1.pack()
    
    label2=Label(window,text="Enter the password")
    label2.config(anchor=CENTER)
    label2.pack()

    txt2=Entry(window,show="*", width=30)
    #txt2.focus()
    txt2.pack()
    
    def checkpassword():
        name=txt1.get()
        passw=txt2.get()
        passw=hashpassword(passw.encode('utf-8'))
        print(passw)
        cursor.execute("SELECT * FROM USERS_ WHERE username = :usern AND password = :passw",
                      {'usern':name,'passw':passw})
        if(len(cursor.fetchall())>0):
            password_manager(name)
        else:
            messagebox.showinfo("Information","PLEASE CHECK USERNAME AND PASSWORD AGAIN")


    button1=Button(window,text="SUBMIT", command=checkpassword)
    button1.pack()
    
    button2=Button(window, text="MAIN MENU",command=main_)
    button2.pack()



  
#function for a new user
def New_user():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("200x300")

    label1=Label(window,text="Create USER")
    label1.config(anchor=CENTER)
    label1.pack()

    txt1=Entry(window, width=30)
    txt1.focus()
    txt1.pack()

    label2=Label(window,text="Create PASSWORD")
    label2.config(anchor=CENTER)
    label2.pack()

    txt2=Entry(window, width=30)
    #txt2.focus()
    txt2.pack()


    label3=Label(window,text="Re-enter the password")
    label3.config(anchor=CENTER)
    label3.pack()

    txt3=Entry(window, width=30)
    #txt2.focus()
    txt3.pack()
    def save_password():
        name=txt1.get()
        cursor.execute("SELECT * FROM USERS_ WHERE username=?",(name,)
            )
        if (len(cursor.fetchall()) > 0): 
            messagebox.showinfo("Information","USERNAME ALREADY EXISTS")
        else:
            if(txt2.get()==txt3.get()):
                hashed_password=hashpassword(txt2.get().encode('utf-8'))

                insert_values="""INSERT INTO USERS_(username,password)
                VALUES(?,?)"""
                cursor.execute(insert_values,(txt1.get(),hashed_password))
                db.commit()
                messagebox.showinfo("Information","ACCOUNT CREATED")
                existing_user()

            else:
                label3.config(text="PLEASE Re-enter SAME PASSWORD")
            
        

    button1=Button(window,text="SUBMIT", command=save_password)
    button1.pack()

    button2=Button(window, text="MAIN MENU",command=main_)
    button2.pack()


#pre-processing required for finding the strength of the password
def split_letters(word): #to split each of the characters in word(tokenization of words on the basis of characters)
    return [char for char in word]

def predict_():
    index=tokenizer2.word_index
    text1="ENTER PASSWORD"
    word=popUp(text1)

    
    l=split_letters(word)
    m=[]
    for letter in l:
        m.append(index[letter])
    m=np.array(m)
    m=np.reshape(m,(1,-1))
 
    l=pad_sequences(m,maxlen=15,padding='pre')
    k=model.predict(l)
    p=np.argmax(k,axis=1)
    if p[0]==0:
        messagebox.showinfo("Information","WEAK")

    elif p[0]==1:
        messagebox.showinfo("Information","WEAK")
    else:
        messagebox.showinfo("Information","STRONG")



def main_():
    window.geometry("200x300")
    for widget in window.winfo_children():
        widget.destroy()
   
    s = ttk.Style()
    label= Label(window,text="Welcome")
    label.config(anchor=CENTER)
    label.pack()
    button1=Button(window,text="Use Existing User",command=existing_user)
    button1.pack()
    button2=Button(window,text="Create New User",command=New_user)
    button2.pack()
    button3=Button(window,text="TRY PASSWORD STRENGTH PREDICTOR",command=predict_)
    button3.pack(side=BOTTOM)



   
    

def password_manager(name):
    for widget in window.winfo_children():
        widget.destroy()
    def addEntry():
        text1="WEBSITE"
        text2="USERNAME"
        text3="PASSWORD"
        website=popUp(text1)
        username=popUp(text2)
        password=popUp(text3)
        
        insert_fields= """INSERT INTO PASSWORDS_(USER,website,userid,password)
        VALUES(?,?,?,?)"""

        cursor.execute(insert_fields, (name,website,username,password))
        db.commit()
        password_manager(name)

    def delEntry():
        text1="Enter website to be deleted"
        website=popUp(text1)
        cursor.execute("DELETE FROM PASSWORDS_  WHERE USER = :user AND website = :website_",
            {'user':name,'website_':website})
        db.commit()
        password_manager(name)

    def updateEntry():
        text1="Enter website to be updated"
        text2="Enter new USERNAME"
        text3="Enter new PASSWORD"
        website=popUp(text1)
        username=popUp(text2)
        password=popUp(text3)
        cursor.execute("""UPDATE PASSWORDS_ SET userid = :username, password = :password_
                       WHERE USER = :user_ AND website=:website_""",
                       {'username':username,'password_':password,'user_':name,'website_':website})
        db.commit()
        password_manager(name)
    window.geometry("200x300")

    label=Label(window,text="PASSWORD MANAGER"+name)
    label.grid(column=1,row=1)
    
    button =Button(window, text="ADD ENTRY", command = addEntry)
    button.grid(column=0,row=2)

    button2 =Button(window, text="DELETE ENTRY", command = delEntry)
    button2.grid(column=1,row=2)

    button3 =Button(window, text="UPDATE ENTRY", command = updateEntry)
    button3.grid(column=2,row=2)

    label1=Label(window,text="WEBSITE")
    label1.grid(row=3, column=0)


    label2=Label(window,text="USERNAME")
    label2.grid(row=3, column=1)


    label3=Label(window,text="PASSWORD")
    label3.grid(row=3, column=2)

    cursor.execute("SELECT * FROM PASSWORDS_ WHERE USER=?",(name,))

    if(cursor.fetchall()!= None):
        i=0
        while True:
            cursor.execute("SELECT * FROM PASSWORDS_ WHERE USER=?",(name,))
            array=cursor.fetchall()

            label1=Label(window,text=(array[i][1]))
            label1.grid(row=i+4, column=0,padx=90)


            label2=Label(window,text=(array[i][2]))
            label2.grid(row=i+4, column=1,padx=90)


            label3=Label(window,text=(array[i][3]))
            label3.grid(row=i+4, column=2,padx=90)

            i=i+1

            cursor.execute("SELECT * FROM PASSWORDS_ WHERE USER=?",(name,))
            if(len(cursor.fetchall())<= i):
                break
    button3=Button(window,text="TRY PASSWORD STRENGTH PREDICTOR",command=predict_)
    button3.grid(row=i+4,column=1)

    button4=Button(window,text="QUIT",command=window.destroy)
    button.grid(row=-1,column=1)


main_()
window.mainloop()