from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import tkinter.tix as tk
from sqlite3 import *
import requests
import bs4
import matplotlib.pyplot as plt
import numpy as np

#data extraction
try: 
	wa = "https://www.brainyquote.com/quote_of_the_day"
	res = requests.get(wa)
	#print(res)

	data = bs4.BeautifulSoup(res.text, "html.parser")
	#print(data)

	info = data.find("img", {"class", "p-qotd"})
	quote = info['alt']
	#print(quote)

except Exception as e:
	print("issue", e)

def f1():
	add_window.deiconify()
	main_window.withdraw()

def f2():
	main_window.deiconify()
	add_window.withdraw()

def f3():
	view_window.deiconify()
	main_window.withdraw()
	vw_st_data.delete (1.0, END)
	info = ""
	con = None
	try:
		con = connect("ems.db")
		cursor = con.cursor() 
		sql = "select * from emp"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + "id: " + str(d[0]) + "  name: " + str(d[1]) + "  sal: " + str(d[2]) + "\n"
		vw_st_data.insert (INSERT, info)
	except Exception as e:
		showerror("issue", e)
	finally:
		if con is not None:
			con.close()

def f4():
	main_window.deiconify()
	view_window.withdraw()

def f5():
	update_window.deiconify()
	main_window.withdraw()

def f6():
	main_window.deiconify()
	update_window.withdraw()

def f7():
	delete_window.deiconify()
	main_window.withdraw()

def f8():
	main_window.deiconify()
	delete_window.withdraw()

def Nmax(list1, N):
	final_list = []
	for i in range(0, N):
		max1 = max(list1)
		final_list.append(max1)
		list1.remove(max1);
	return final_list

def f9():
	chart_window.deiconify()
	main_window.withdraw()
	con = None
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql = "select salary from emp"
		cursor.execute(sql)
		data=cursor.fetchall()
		p_lst = []
		for d in data:
			p_lst.append(d[0])
		#print(lst)
		N=5
		final_list = Nmax(p_lst, N)
		print(final_list)
		
		n_lst=[]
		for i in range(0, len(final_list)):
			sql1 = "select name from emp where salary='%d'"
			cursor.execute(sql1 % (final_list[i]))
			data1 = cursor.fetchall()
			for d in data1:
				if d[0] not in n_lst:
					n_lst.append(d[0])
		print(n_lst)
		
		fig = plt.figure()
		fig.patch.set_facecolor('xkcd:white')
		ax= plt.gca()
		ax.set_facecolor('xkcd:white')
		plt.bar(n_lst, final_list, color='green')
		plt.xlabel("Name of Employees")
		plt.ylabel("Salary of Employees")
		plt.title("Employee's Information")
		plt.show()
	except Exception as e:
		con.rollback()
		showerror("Issue", e)
	finally:
		if con is not None:
			con.close()

def f10():
	main_window.deiconify()
	chart_window.withdraw()

def f11():
	con = None
	try:
		con = connect("ems.db") 
		cursor = con.cursor()
		sql1 = "select id from emp"
		cursor.execute(sql1)
		data = cursor.fetchall()
		id_lst=[]
		for d in data:
			id_lst.append(d[0])
		sql = "insert into emp values('%d', '%s', '%d')"
		id=None
		try:
			id = int(aw_ent_id.get())
			if id < 1:
				raise Exception("Invalid id")
			elif id in id_lst:
				raise Exception("Id already exists")
		except ValueError:
			id1 = str(aw_ent_id.get())
			if len(id1) == 0:
				raise Exception("Id cannot be empty")
			elif id1.isspace():
				raise Exception("Spaces not allowed")
			else:
				raise Exception("Integers Only")
		name=aw_ent_name.get()
		if len(name) < 2: 
			raise Exception("Invalid employee name")
		elif name.isalpha():
			pass
		else:
			raise Exception("Employee name should contain alphabets only")
		salary=None
		try:
			salary=int(aw_ent_salary.get())
			if salary < 8000:
				raise Exception("Invalid Salary")
		except ValueError:
			raise Exception("Salary cannot be empty")
		cursor.execute(sql% (id, name, salary))
		con.commit()
		showinfo("success", "record added") 
		aw_ent_id.delete(0, END)
		aw_ent_name.delete(0, END)
		aw_ent_salary.delete(0, END)
		aw_ent_id.focus()

	except Exception as e:
		con.rollback()	
		showerror("issue", e)

	finally:
		if con is not None:
			con.close()

def f12():
	con= None
	try:
		con = connect("ems.db") 
		cursor = con.cursor()
		sql1 = "select id from emp"
		cursor.execute(sql1)
		data = cursor.fetchall()
		id_lst=[]
		for d in data:
			id_lst.append(d[0])
		sql =  "update emp set name = '%s' , salary = '%d' where id = '%d' " 
		id=None
		try:
			id = int(uw_ent_id.get())
			if id < 1:
				raise Exception("Invalid Id")
			elif id not in id_lst:
				raise Exception("Id doesnt exists")
		except ValueError:
			id = str(uw_ent_id.get())
			if len(id1) == 0:
				raise Exception("Id cannot be empty")
			elif id1.isspace():
				raise Exception("Spaces not allowed")
			else:
				raise Exception("Integers Only")
		name=uw_ent_name.get()
		if len(name) < 2: 
			raise Exception("Invalid employee name")
		elif name.isalpha():
			pass
		else:
			raise Exception("Employee name should contain alphabets only")
		salary=None
		try:
			salary=int(uw_ent_salary.get())
			if salary < 8000:
				raise Exception("Invalid salary")
		except ValueError:
			raise Exception("Salary cannot be empty")
		cursor.execute(sql % (name, salary, id))
		if cursor.rowcount == 1 :
			con.commit()
			showinfo("success", "record updated")
		else:
			showinfo(id," does not exists")
		uw_ent_id.delete(0, END)
		uw_ent_name.delete(0, END)
		uw_ent_salary.delete(0, END)

	except Exception as e: 
		showerror("issue ", e)
		con.rollback()

	finally:
		if con is not None:
			con.close() 

def f13():
	con= None
	try:
		con = connect("ems.db") 
		cursor = con.cursor()
		sql1 = "select id from emp"
		cursor.execute(sql1)
		data = cursor.fetchall()
		id_lst=[]
		for d in data:
			id_lst.append(d[0])
		sql =  "delete from emp where id = '%d' " 
		id=None
		try:
			id = int(dw_ent_id.get())
			if id < 1:
				raise Exception("Invalid Id")
			elif id not in id_lst:
				raise Exception("Id doesnt exists")
		except ValueError:
			id1 = str(dw_ent_id.get())
			if len(id1) == 0:
				raise Exception("Id cannot be empty")
			elif id1.isspace():
				raise Exception("Spaces not allowed")
			else:
				raise Exception("Integers Only")			
			
		cursor.execute(sql % (id))
		con.commit()
		showinfo("Record deleted")
		dw_ent_id.delete(0, END)

	except Exception as e: 
		showerror("issue ", e)
		con.rollback()

	finally:
		if con is not None:
			con.close()

main_window = Tk()
main_window.title("E. M. S")
main_window.geometry("1100x500+80+100")
main_window['bg'] = "cyan"

f = ("Arial", 18)
mw_btn_add = Button(main_window, text="Add ", font=f, width=10, command=f1)
mw_btn_view = Button(main_window, text="View ", font=f, width=10, command=f3)
mw_btn_update = Button(main_window, text="Update ", font=f, width=10,command=f5)
mw_btn_delete = Button(main_window, text="Delete ", font=f, width=10,command=f7)
mw_btn_chart = Button(main_window, text="Chart", font=f, width=10,command=f9)
mw_lbl_qotd = Label(main_window, text="Quote of the day : ", font=f)
mw_lbl_quote = Label(main_window, text=quote, font=f)
mw_btn_add.pack(pady = 7)
mw_btn_view.pack(pady = 7)
mw_btn_update.pack(pady = 7)
mw_btn_delete.pack(pady = 7)
mw_btn_chart.pack(pady = 7)
mw_lbl_qotd.pack(pady = 7)
mw_lbl_quote.pack(pady = 7)

add_window = Toplevel(main_window)
add_window.title("Add Emp")
add_window.geometry("900x500+200+100")
add_window['bg'] = "light yellow"

aw_lbl_id = Label(add_window, text="Enter id : ", font=f)
aw_ent_id = Entry(add_window, font=f, bd = 4)
aw_lbl_name = Label(add_window, text="Enter name : ", font=f)
aw_ent_name = Entry(add_window, font=f, bd = 4)
aw_lbl_salary= Label(add_window, text="Enter salary : ", font=f)
aw_ent_salary = Entry(add_window, font=f, bd = 4)
aw_btn_save = Button(add_window, text="Save", font=f, width=10, command=f11)
aw_btn_back = Button(add_window, text="Back", font=f, width=10, command=f2)

aw_lbl_id.pack(pady=7)
aw_ent_id.pack(pady=7)
aw_lbl_name.pack(pady=7)
aw_ent_name.pack(pady=7)
aw_lbl_salary.pack(pady=7)
aw_ent_salary.pack(pady=7)
aw_btn_save.pack(pady=7)
aw_btn_back.pack(pady=7)

add_window.withdraw()

view_window = Toplevel(main_window)
view_window.title("View Emp")
view_window.geometry("700x500+200+100")
view_window['bg'] = "light green"

vw_st_data = ScrolledText(view_window, width=20, height=10, font=f)
vw_btn_back = Button(view_window, text="Back", font= f, command=f4)
vw_st_data.pack(pady=7)
vw_btn_back.pack(pady=7)

view_window.withdraw()

update_window = Toplevel(main_window)
update_window.title("Update Emp")
update_window.geometry("700x500+200+100")
update_window['bg'] = "pink"

uw_lbl_id = Label(update_window, text="Enter id : ", font=f)
uw_ent_id = Entry(update_window, font=f, bd = 4)
uw_lbl_name = Label(update_window, text="Enter name : ", font=f)
uw_ent_name = Entry(update_window, font=f, bd = 4)
uw_lbl_salary = Label(update_window, text="Enter salary : ", font=f)
uw_ent_salary = Entry(update_window, font=f, bd = 4)
uw_btn_save = Button(update_window, text="Save", font=f, width=10, command=f12)
uw_btn_back = Button(update_window, text="Back", font=f, width=10, command=f6)

uw_lbl_id.pack(pady=7)
uw_ent_id.pack(pady=7)
uw_lbl_name.pack(pady=7)
uw_ent_name.pack(pady=7)
uw_lbl_salary.pack(pady=7)
uw_ent_salary.pack(pady=7)
uw_btn_save.pack(pady=7)
uw_btn_back.pack(pady=7)

update_window.withdraw()

delete_window = Toplevel(main_window)
delete_window.title("Delete Emp")
delete_window.geometry("700x500+200+100")
delete_window['bg'] = "lightcoral"

dw_lbl_id = Label(delete_window, text="Enter id : ", font=f)
dw_ent_id = Entry(delete_window, font=f, bd = 4)
dw_btn_save = Button(delete_window, text="Save", font=f, width=10, command=f13)
dw_btn_back = Button(delete_window, text="Back", font=f, width=10, command=f8)

dw_lbl_id.pack(pady=7)
dw_ent_id.pack(pady=7)
dw_btn_save.pack(pady=7)
dw_btn_back.pack(pady=7)

delete_window.withdraw()

chart_window = Toplevel(main_window)
chart_window.title("Charts")
chart_window.geometry("700x500+200+100")
chart_window['bg'] = "magenta"
cw_btn_save = Button(chart_window, text="Save", font=f, width=10, command=f9)
cw_btn_back = Button(chart_window, text="Back", font=f, width=10, command=f10)

cw_btn_save.pack(pady=7)
cw_btn_back.pack(pady=7)

chart_window.withdraw()

main_window.mainloop()