from tkinter import *
from requests import *
from sqlite3 import *
import json
import requests
import matplotlib.pyplot as plt
from tkinter.scrolledtext import *
from tkinter.messagebox import *
import pandas as pd

def check_if_empty(window):
    con=None
    try:
        con=connect("ems.db")
        cursor=con.cursor()
        cursor.execute("SELECT 1 FROM employee LIMIT 1")
        result=cursor.fetchone()
        if result is None:
            showinfo("Empty Database","No Data Present")
            return True
        else:
            
            try:
                window.deiconify()
                mw.withdraw()
            finally:
                return False
                
    except Exception as e:
        showerror("issue",e)
    finally:
        if con is not None:
            con.close()

def addW():
    mw.withdraw()
    aw.deiconify()

def close_addW():
    aw.withdraw()
    mw.deiconify()

def viewW():
    check_if_empty(vw)
    vw_scrolledText_btn.delete(1.0,END)
    con=None
    try:
        con=connect("ems.db")
        cursor=con.cursor()
        sql="select * from employee"
        cursor.execute(sql)
        data=cursor.fetchall()
        info=""
        for d in data:
            info=info + "id: " + str(d[0]) + " name: " + str(d[1]) + " sal: " + str(d[2]) + "\n"
        vw_scrolledText_btn.insert(INSERT,info)
    except Exception as e:
        showerror("issue",e)
    finally:
        if con is not None:
            con.close()

def close_viewW():
    vw.withdraw()
    mw.deiconify()

def updateW():
    check_if_empty(uw)

def close_updateW():
    uw.withdraw()
    mw.deiconify()

def deleteW():
    check_if_empty(dw)

def close_deleteW():
    dw.withdraw()
    mw.deiconify()

def loc_temp():
    try:
        send_url = "http://ip-api.com/json/"
        geo_req = requests.get(send_url)
        geo_json = json.loads(geo_req.text)
        city = geo_json['city']
        info = city
        lab.configure(text = info)
    except Exception as e:
        lab.configure(text = "issue" + str(e))
    try:
        a1 = "https://api.openweathermap.org/data/2.5/weather"
        a2 = "?q=" + city
        a3 = "&appid=" + "c6e315d09197cec231495138183954bd"
        a4 = "&units=" + "metric"
        wa = a1 + a2 + a3 + a4
        print(wa)
        res = get(wa)
        data = res.json()
        temp = data["main"]["temp"]
        tem.configure(text = str(temp)+"॰C")
    except Exception as e:
        print("issue ",e)

def addData():
    con=None
    try:
        con=connect("ems.db")
        cursor=con.cursor()
        sql="insert into employee values('%d','%s','%d')"
        try:
            id=int(aw_id_ent.get())
        except ValueError:
            showerror("issue","Please enter Valid ID")
            aw_id_ent.delete(0,END)
            aw_id_ent.focus()
            return
        if(id<1):
            showerror("issue","ID should be greater than 0")
            aw_id_ent.delete(0,END)
            aw_id_ent.focus()
            return
        cursor.execute("SELECT id FROM employee WHERE id=?",(id,))
        existing_id=cursor.fetchone()
        if existing_id:
            showerror("issue","Entered id already exists")
            aw_id_ent.delete(0,END)
            aw_id_ent.focus()
            return
        
        name=aw_name_ent.get()
        try:
            if not name.isalpha():
                showerror("issue","Enter Valid name")
                aw_name_ent.delete(0,END)
                aw_name_ent.focus()
                return
            if len(name)<2:
                showerror("issue","Name shall contain minimum of two letters")
                aw_name_ent.delete(0,END)
                aw_name_ent.focus()
                return
        except Exception as e:
            showerror("issue",e)

        try:
            salary=int(aw_salary_ent.get())
        except ValueError:
            showerror("issue","Please Enter Salary")
            aw_salary_ent.delete(0,END)
            aw_salary_ent.focus()
            return
        if salary<8000:
            showerror("issue","Minimum Salary should be 8000")
            aw_salary_ent.delete(0,END)
            aw_salary_ent.focus()
            return
        
        cursor.execute(sql%(id,name,salary))
        con.commit()
        showinfo("Success","Employee Added")
        aw_id_ent.delete(0,END)
        aw_name_ent.delete(0,END)
        aw_salary_ent.delete(0,END)
        aw_id_ent.focus()


    except Exception as e:
        showerror("Issue", e)
    finally:
        if con is not None:
            con.close()

def updateData():
    con=None
    try:
        con=connect("ems.db")
        cursor=con.cursor()
        sql="update employee set name='%s',salary='%d' where id='%d'"
        try:
            id=int(uw_id_ent.get())
        except ValueError:
            showerror("issue","Enter Valid ID")
            uw_id_ent.delete(0,END)
            uw_id_ent.focus()
            return
        if id<1:
            showerror("issue","ID should be greater than 0")
            uw_id_ent.delete(0,END)
            uw_id_ent.focus()
            return
        
        name=uw_name_ent.get()
        try:
            if not name.isalpha():
                showerror("issue","Enter Valid Name")
                uw_name_ent.delete(0,END)
                uw_name_ent.focus()
                return
        
            if len(name) <2:
                showerror("issue","Name shall contain minimum 2 letters")
                uw_name_ent.delete(0,END)
                uw_name_ent.focus()
                return
        except Exception as e:
            showerror("issue",e)

        try:
            salary=int(uw_salary_ent.get())
        except ValueError:
            showerror("issue","Please enter valid salary")
            uw_salary_ent.delete(0,END)
            uw_salary_ent.focus()
            return
        if salary<8000:
            showerror("issue","Salary should be minimum 8000")
            uw_salary_ent.delete(0,END)
            uw_salary_ent.focus()
            return
        cursor.execute(sql%(name,salary,id))
        if cursor.rowcount==1:
            showinfo("Done","Record Updated")
            uw_id_ent.delete(0,END)
            uw_name_ent.delete(0,END)
            uw_salary_ent.delete(0,END)
            uw_id_ent.focus()
        con.commit()
            
    except Exception as e:
        showerror("issue",e)
    finally:
        if con is not None:
            con.close()

def deleteData():
    con=None
    try:
        con=connect("ems.db")
        cursor=con.cursor()
        sql="delete from employee where id = '%d'"
        
        try:
            id=int(dw_id_ent.get())
        except ValueError:
            showerror("issue","Enter Valid id")
            dw_id_ent.delete(0,END)
            dw_id_ent.focus()
            return
        if id<1:
            showerror("issue","id should be minimum 1")
            dw_id_ent.delete(0,END)
            dw_id_ent.focus()
            return
        cursor.execute(sql%(id))
        if cursor.rowcount==1:
            con.commit()
            showinfo("Deleted","Record Deleted")
            
        else:
            showerror("Issue","Record Does not exist")
    except Exception as e:
        showerror("issue",e)
        con.rollback()
    finally:
        if con is not None:
            con.close()
        dw_id_ent.delete(0,END)

def chartData():
    result=check_if_empty(plt)
    if not result:
        con=connect("ems.db")
        df=pd.read_sql_query("SELECT name,salary FROM employee ORDER by salary DESC LIMIT 5",con)
        plt.figure().set_figwidth(7)
        
        plt.bar(df["NAME"],df["SALARY"])
        plt.xlabel('Name')
        plt.ylabel('Salary')
        plt.title("Employees with highest Salaries")
        
        plt.show()

        con.close()

c1="#E1EBEE"
c2="#1aac83"
c3="#ddd"
mw=Tk()
mw.title("Ayush Project")
mw.geometry("1000x700+300+50")
mw.configure(bg=c1)

f=("Calibre",36,"italic")
mw_add_btn=Button(mw,text="Add",font=f,width=10, command=addW,bg=c2,foreground=c1,borderwidth=3,relief="ridge")
mw_add_btn.pack(pady=10)
mw_view_btn=Button(mw,text="View",font=f,width=10,command=viewW,bg=c2,foreground=c1,borderwidth=3,relief="ridge")
mw_view_btn.pack(pady=10)
mw_update_btn=Button(mw,text="Update",font=f,width=10,command=updateW,bg=c2,foreground=c1,borderwidth=3,relief="ridge")
mw_update_btn.pack(pady=10)
mw_delete_btn=Button(mw,text="Delete",font=f,width=10,command=deleteW,bg=c2,foreground=c1,borderwidth=3,relief="ridge")
mw_delete_btn.pack(pady=10)
cw_charts_btn=Button(mw,text="Charts",font=f,width=10,command=chartData,bg=c2,foreground=c1,borderwidth=3,relief="ridge")
cw_charts_btn.pack(pady=10)

mw_lab_Location = Label(mw,text = "Location:", font=f,bg=c1)
mw_lab_Temp = Label(mw,text = "Temp:", font=f,bg=c1)
lab = Label(mw, font = f, wraplength = 700,bg=c1)
tem = Label(mw, font = f, wraplength = 700,bg=c1)
mw_lab_Location.place(x = 50, y = 630)
mw_lab_Temp.place(x = 560, y = 630)
lab.place(x = 280, y = 630)
tem.place(x = 720, y = 630)

loc_temp()

aw=Toplevel(mw)
aw.title("Add Employee Details")
aw.geometry("700x700+400+30")
aw.configure(bg=c1)
f=("Calibre",32,"italic")

aw_id_lab=Label(aw,text="Enter id:",font=f,bg=c1)
aw_id_lab.pack(pady=10)
aw_id_ent=Entry(aw,font=f,bg=c3)
aw_id_ent.pack(pady=10)
aw_name_lab=Label(aw,text="Enter Name:",font=f,bg=c1)
aw_name_lab.pack(pady=10)
aw_name_ent=Entry(aw,font=f,bg=c3)
aw_name_ent.pack(pady=10)
aw_salary_lab=Label(aw,text="Enter Salary:",font=f,bg=c1)
aw_salary_lab.pack(pady=10)
aw_salary_ent=Entry(aw,font=f,bg=c3)
aw_salary_ent.pack(pady=10)
aw_save_btn=Button(aw,text="Save",font=f,command=addData,bg=c2,foreground=c1,borderwidth=3,relief="ridge")
aw_save_btn.place(x=180,y=500)
aw_back_btn=Button(aw,text="Back",font=f,command=close_addW,bg=c2,foreground=c1,borderwidth=3,relief="ridge")
aw_back_btn.place(x=380,y=500)
aw.protocol("WM_DELETE_WINDOW",close_addW)
aw.withdraw()

vw=Toplevel(mw)
vw.title("View Employee Details")
vw.geometry("900x700+300+30")
vw.configure(bg=c1)

vw_scrolledText_btn=ScrolledText(vw,width=30,height=8,font=f,bg=c3)
vw_scrolledText_btn.pack(pady=10)
vw_back_btn=Button(vw,text="Back",font=f,command=close_viewW,bg=c2,foreground=c1,borderwidth=3,relief="ridge")
vw_back_btn.pack(pady=10)
vw.protocol("WM_DELETE_WINDOW",close_viewW)
vw.withdraw()

uw=Toplevel(mw)
uw.title("Update Employee Details")
uw.geometry("700x700+400+30")
uw.configure(bg=c1)

uw_id_lab=Label(uw,text="Enter id:",font=f,bg=c1)
uw_id_lab.pack(pady=10)
uw_id_ent=Entry(uw,font=f,bg=c3)
uw_id_ent.pack(pady=10)
uw_name_lab=Label(uw,text="Enter Name:",font=f,bg=c1)
uw_name_lab.pack(pady=10)
uw_name_ent=Entry(uw,font=f,bg=c3)
uw_name_ent.pack(pady=10)
uw_salary_lab=Label(uw,text="Enter Salary:",font=f,bg=c1)
uw_salary_lab.pack(pady=10)
uw_salary_ent=Entry(uw,font=f,bg=c3)
uw_salary_ent.pack(pady=10)
uw_save_btn=Button(uw,text="Save",font=f,command=updateData,bg=c2,foreground=c1,borderwidth=3,relief="ridge")
uw_save_btn.place(x=180,y=500)
uw_back_btn=Button(uw,text="Back",font=f,command=close_updateW,bg=c2,foreground=c1,borderwidth=3,relief="ridge")
uw_back_btn.place(x=380,y=500)
uw.protocol("WM_DELETE_WINDOW",close_updateW)
uw.withdraw()

dw=Toplevel(mw)
dw.title("Delete Employee Details")
dw.geometry("700x400+400+200")
dw.configure(bg=c1)

dw_id_lab=Label(dw,text="Enter id:",font=f,bg=c1)
dw_id_lab.pack(pady=10)
dw_id_ent=Entry(dw,font=f,bg=c3)
dw_id_ent.pack(pady=10)
dw_delete_btn=Button(dw,text="Delete",font=f,command=deleteData,bg=c2,foreground=c1,borderwidth=3,relief="ridge")
dw_delete_btn.place(x=180,y=200)
dw_back_btn=Button(dw,text="Back",font=f,command=close_deleteW,bg=c2,foreground=c1,borderwidth=3,relief="ridge")
dw_back_btn.place(x=380,y=200)
dw.protocol("WM_DELETE_WINDOW",close_deleteW)
dw.withdraw()


mw.mainloop()