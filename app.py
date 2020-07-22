from  tkinter import * 
import tkinter as tk
from tkinter import ttk
import requests
from plyer import notification
from bs4 import BeautifulSoup
import time

"<---------------Config-properties of window----->"
Window=Tk()
Window.configure(bg="#99FFFF")
Window.title("Covid19-Tracker")
Window.resizable(0,0)
Window.geometry("1050x450+200+80")
global data,data1

"<------------Functions-------------->"
def getdata(url):
	return requests.get(url).text


def current_data():
	"""
	This Function Web-scraps the current cases in INDIA
	
	"""
	Data = getdata('https://www.mohfw.gov.in/')#getting data from url
	soup = BeautifulSoup(Data, 'html.parser') #parsing it to bs4


	mystr='' #creating null string
	for ul in soup.find_all("div",class_="site-stats-count"): #finding the statewise count
		mystr+=ul.get_text()
	counts=mystr.split("\n\n\n\n")[1:5]	#separating the values 
	l=[]  #creating the list to append valu
	for items in counts:
		l.append(items)

	return l[0].split('\n')[0], l[1].split('\n')[0],l[0].split('\n')[0], l[3].split('\n')[0];




def stateswise_current_data(state):

	"""
	This Function Web-scraps the current cases in INDIA
	
	"""

	Data = getdata('https://www.mohfw.gov.in/')#getting data from url
	soup = BeautifulSoup(Data, 'html.parser')#parsing it to bs4


	mystring=""
	for tr in soup.find_all('tbody')[0].find_all('tr'):
		mystring+=tr.get_text()
	mystring = mystring[1:]
	itemlist=mystring.split("\n\n")
	for item in itemlist[0:35]:
		list_states=item.split("\n")
		if list_states[1] == state:
			return list_states[2],list_states[3],list_states[4],list_states[5];

def fetch_selected():
	"""
	This Function Will fetch the selected state and will displaye the data for it

	"""
	global data1,data

	for row in tree.get_children():
		tree.delete(row)

	data1=stateswise_current_data(statechoosen.get())
	
	data = [ ['1',statechoosen.get(), data1[0],data1[1],data1[2],data1[3]],]
	tree.insert("",'end',values=(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5]))


def notification_funct():
	"""
	This function will fetch selected state_name and make notification for it

	"""

	selected_state_for_notification=stateswise_current_data(notifychoosen.get())
	
	notification.notify(
	    title=notifychoosen.get(),
	    message='Activecases: '+selected_state_for_notification[0]+"\n"+"Cured: "+selected_state_for_notification[1]+'\n'+"Deaths: "+selected_state_for_notification[2]+'\n'+"Total Confirm Cases : "+selected_state_for_notification[3],
	    app_icon='C:\\Users\\Dell\\Desktop\\FlaskDemo\\Covid-project\\icon.ico',  # e.g. 'C:\\icon_32x32.ico'
	    timeout=3,  # seconds
	     )




"<-----------widgets-------------->"





frame = Frame(Window)
frame.place(x=20,y=100)

tree =ttk.Treeview(frame, columns = (1,2,3,4,5,6), height =1, show = "headings",)
tree.pack()

style = ttk.Style()
style.configure("Treeview.Heading", font=('sans-serif', 12))
style.configure("Treeview.column", font=('sans-serif', 12))
style.configure('App.TCombobox', font=('sans-serif', 12))

tree.heading(1, text="S.No")
tree.heading(2, text="Name of State / UT")
tree.heading(3, text="Active Cases*")
tree.heading(4, text="Cured/Discharged/Migrated*")
tree.heading(5, text="Deaths**")
tree.heading(6, text="Total Confirmed cases*")


tree.column(1, width = 100,stretch=tk.YES,anchor='center')
tree.column(2, width = 200,stretch=tk.YES,anchor='center')
tree.column(3, width = 150,stretch=tk.YES,anchor='center')
tree.column(4, width = 220,stretch=tk.YES,anchor='center')
tree.column(5, width = 170,stretch=tk.YES,anchor='center')
tree.column(6, width = 170,stretch=tk.YES,anchor='center')

# Adding combobox drop down list 

n = tk.StringVar() 
statechoosen = ttk.Combobox(Window, width = 27,textvariable = tk.StringVar() ,font=('sans-serif', 10)) 
statechoosen.grid(column = 1, row = 15) 

notifychoosen = ttk.Combobox(Window, width = 27,textvariable = n ,font=('sans-serif', 10)) 
notifychoosen.grid(column = 2, row = 15) 

notifychoosen['values']= ('Andaman and Nicobar Islands', 'Andhra Pradesh',' Arunachal Pradesh', 'Assam', 
                          'Bihar','July','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu','Delhi','Goa','Gujarat',
                          "Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Madhya Pradesh",
                          "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim",
                          "Tamil Nadu","Telangana","Tripura","Uttarakhand","Uttar Pradesh","West Bengal",
                          )

statechoosen['values']= (
	                     'Andaman and Nicobar Islands', 'Andhra Pradesh','Arunachal Pradesh', 'Assam', 
                          'Bihar','July','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu','Delhi','Goa','Gujarat',
                          "Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Madhya Pradesh",
                          "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim",
                          "Tamil Nadu","Telangana","Tripura","Uttarakhand","Uttar Pradesh","West Bengal",
                          )
notifychoosen.current(19)
statechoosen.current(19)


"""
   Setting default selected statewise  data in tree view

"""
data1=stateswise_current_data(statechoosen.get())
data = [ ['1',statechoosen.get(), data1[0],data1[1],data1[2],data1[3]],]

for val in data:
    tree.insert('', 'end', values = (val[0], val[1], val[2],val[3],val[4],val[5]) )

 


show_info=Button(Window,text='Show info',relief=GROOVE,command=fetch_selected)
show_info.place(x=10,y=30)

set_notification=Button(Window,text='Set-Notification',relief=GROOVE,command=notification_funct)
set_notification.place(x=220,y=30)

data=current_data()

Label_text = Label(Window,text='COVID19-INDIA STATEWISE-STATUS',font=('Bold',18),bg="#99FFFF") # covid heading
Label_text.place(x=280,y=60)

Label_text = Label(Window,text='COVID19-INDIA',font=('Bold',25),bg="#99FFFF") # covid heading
Label_text.place(x=250,y=200)

Label_current_time = Label(Window,text="as on :"+time.ctime(),font=('Bold',15),fg="#FF0000",bg="#99FFFF") # current time
Label_current_time.place(x=500,y=210)

Label_Activecases = Label(Window,text="Active Cases",font=('Bold',20),fg="#000080",bg="#99FFFF") #text -Activecases
Label_Activecases.place(x=200,y=360)

Label_Activecases_counts = Label(Window,text=" "+data[0],font=('Bold',18),fg="#000080",bg="#99FFFF") #text -Activecases_counts
Label_Activecases_counts.place(x=200,y=300)


Label_Cured = Label(Window,text="Cured",font=('Bold',20),fg="#008000",bg="#99FFFF")#text -Cured
Label_Cured.place(x=450,y=360)

Label_Cured_count = Label(Window,text=data[1],font=('Bold',18),fg="#008000",bg="#99FFFF")#text -Cured-data
Label_Cured_count.place(x=450,y=300)

Label_Deaths = Label(Window,text="Deaths",font=('Bold',20),fg="#FF0000",bg="#99FFFF")#text -Deaths
Label_Deaths.place(x=600,y=360)

Label_Deaths_count= Label(Window,text=data[2],font=('Bold',18),fg="#FF0000",bg="#99FFFF")#text -Deaths
Label_Deaths_count.place(x=600,y=300)

Label_Migrated = Label(Window,text="Migrated",font=('Bold',20),fg="#FF8C00",bg="#99FFFF")# text -Migrated
Label_Migrated.place(x=750,y=360)

Label_Migrated_counts = Label(Window,text=" "+data[3],font=('Bold',18),fg="#FF8C00",bg="#99FFFF")# text -Migrated
Label_Migrated_counts.place(x=750,y=300)



Window.mainloop()