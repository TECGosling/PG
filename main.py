import tkinter as tk
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import paho.mqtt.client as mqtt  #import the client1
import time
import webbrowser
import requests
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from PIL import  ImageTk, Image
import json
import sqlite3
import django
from tkcalendar import *


#general

root = tk.Tk()
root.title('GreenHouse Controller')
root.iconbitmap('icon.ico')
root.geometry('800x480')
root.maxsize(800,480)
root.minsize(800,480)

#importing images
data_image = ImageTk.PhotoImage(Image.open('images/data40.png'))
pw_image = ImageTk.PhotoImage(Image.open('images/pw40.png'))
ubi_image = ImageTk.PhotoImage(Image.open('images/web.png'))
sett_image = ImageTk.PhotoImage(Image.open('images/settings.png'))
bg_image = ImageTk.PhotoImage(Image.open('images/Main_GUI.png'))
log_image = ImageTk.PhotoImage(Image.open('images/log.png'))
n_image = ImageTk.PhotoImage(Image.open('images/n_butt.png'))
p_image = ImageTk.PhotoImage(Image.open('images/p_butt.png'))
close_image = ImageTk.PhotoImage(Image.open('images/close.png'))
cnt_image = ImageTk.PhotoImage(Image.open('images/control.png'))
humcnt_image = ImageTk.PhotoImage(Image.open('images/hum_controlbg.png'))
refresh_image = ImageTk.PhotoImage(Image.open('images/refresh.png'))
pw2_image = ImageTk.PhotoImage(Image.open('images/pw2.png'))
SW_image = ImageTk.PhotoImage(Image.open('images/switch_UI.png'))
scnd_ie = ImageTk.PhotoImage(Image.open('images/secnd_UI.png'))
treeV_image = ImageTk.PhotoImage(Image.open('images/treeview.png'))
grph1 = ImageTk.PhotoImage(Image.open('images/grph1.png'))
grph2 = ImageTk.PhotoImage(Image.open('images/grph2.png'))
fil_I = ImageTk.PhotoImage(Image.open('images/fil_i.png'))
slct = ImageTk.PhotoImage(Image.open('images/select.png'))
cldr = ImageTk.PhotoImage(Image.open('images/caldar.png'))
info = ImageTk.PhotoImage(Image.open('images/info.png'))
hilf1 = ImageTk.PhotoImage(Image.open('images/help1.png'))
hilf2 = ImageTk.PhotoImage(Image.open('images/help2.png'))
hilf3 = ImageTk.PhotoImage(Image.open('images/help3.png'))
bck_img = ImageTk.PhotoImage(Image.open('images/back.png'))
nxt_img = ImageTk.PhotoImage(Image.open('images/next.png'))


imag_list = [hilf1, hilf2, hilf3]

client = mqtt.Client("Heiner")


temp1_stack = []
temp2_stack = []
hum1_stack = []
hum2_stack = []


#variables
cont1 = []
h = 480
w = 800
mqtt_ip = '192.168.137.97'
mqtt_port = '1883'
t = time.localtime()
date = time.strftime("%d/%b/%Y", t)
time_s = time.strftime("%X", t)
unix = time.time()
today = datetime.today().strftime('%d/%m/%y')

# Get funtions

def get_t1():
    try:
        t1 = temp1_stack.pop()
    except:
        t1 = 5
    return t1

def get_t2():
    try:
        t2 = temp2_stack.pop()
    except:
        t2 = 5
    return t2

def get_h1():
    try:
        h1 = hum1_stack.pop()
    except:
        h1 = 5
    return h1

def get_h2():
    try:
        h2 = hum2_stack.pop()
    except:
        h2 = 5
    return h2

#Plotting

def temp_plotting():
    plt.style.use('seaborn')
    dates = []
    temp1 = []
    temp2 = []
    fig, (ax1, ax2) = plt.subplots(2,1)
    fig.suptitle('Representacion Grafica de Temperaturas')
    ax2.set_xlabel('Fecha')
    ax1.set_ylabel('Temperatura Interior (°C)')
    ax2.set_ylabel('Temperatura Exterior (°C)')

    conn = sqlite3.connect('data.db') #create connection
    c = conn.cursor()
    c.execute('''SELECT *, oid FROM data''')
    data = c.fetchall()
    for row in data:
        dates.append(datetime.fromtimestamp(row[0]))
        temp1.append(row[1])
        temp2.append(row[2])

    ax1.plot_date(dates, temp1)
    ax2.plot_date(dates, temp2)
    plt.tight_layout()
    plt.show()

def hum_plotting():
    plt.style.use('seaborn')
    dates = []
    hum1 = []
    hum2 = []
    fig, (ax1, ax2) = plt.subplots(2,1)
    fig.suptitle('Representacion Grafica de Humedad')
    ax2.set_xlabel('Fecha')
    ax1.set_ylabel('Humedad Interior (%)')
    ax2.set_ylabel('Humedad Exterior (%)')

    conn = sqlite3.connect('data.db') #create connection
    c = conn.cursor()
    c.execute('''SELECT *, oid FROM data''')
    data = c.fetchall()
    for row in data:
        dates.append(datetime.fromtimestamp(row[0]))
        hum1.append(row[3])
        hum2.append(row[4])

    ax1.plot_date(dates, hum1)
    ax2.plot_date(dates, hum2)
    plt.tight_layout()
    plt.show()

#Database

def create_sqdatabase():
    conn = sqlite3.connect('data.db') #create connection
    c = conn.cursor()
    c.execute("""CREATE TABLE data (
        fecha float,
        temp1 float,
        temp2 float,
        hum1 float,
        hum2 float)""")

    conn.commit()
    conn.close()

def sub_sqdata(t1,t2,h1,h2):
    unix = time.time()
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''INSERT INTO data VALUES (:fecha, :temp1, :temp2, :hum1, :hum2)''',
            {
                'fecha': unix,
                'temp1': t1,
                'temp2': t2,
                'hum1': h1,
                'hum2': h2,


            }
              )
    conn.commit()
    conn.close()
    cont1.clear()
    hum1_stack.clear()
    hum2_stack.clear()
    temp1_stack.clear()
    temp2_stack.clear()

def show_sq():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM data")
    data = c.fetchall()
    list_y = []
    for element in data:
        list_y.append(element[1])
    conn.commit()
    conn.close()
    return list_y
def database():
    #window features
    window = tk.Toplevel()
    window.geometry('680x300')
    window.maxsize(680, 300)
    window.minsize(680, 300)
    window.title('Registros')
    window.iconbitmap('icon.ico')
    style = ttk.Style()
    style.theme_use('clam')
    bg_label = tk.Label(window, image=treeV_image).place(relheight=1, relwidth=1)

    regis_1 = ttk.Treeview(window)
    regis_1.pack(anchor = 'center')
    regis_1['columns'] = ['Temp. Exterior', 'Temp. Interior', 'Humedad Exterior', 'Humedad Interior', 'Hora']

    regis_1.column("#0", width = 0, stretch = 'NO')
    regis_1.column("#1", width=120, anchor = 'center')
    regis_1.column("#2", width=120, anchor = 'center')
    regis_1.column("#3", width=120, anchor = 'center')
    regis_1.column("#4", width=120, anchor = 'center')
    regis_1.column("#5", width=80, anchor='center')

    regis_1.heading("#1", text='Temp. Exterior')
    regis_1.heading("#2", text='Temp. Interior')
    regis_1.heading("#3", text='Humedad Exterior')
    regis_1.heading("#4", text='Humedad Interior')
    regis_1.heading("#5", text=today)
    regis_1.tag_configure('highT', background='#f5978e')

    conn = sqlite3.connect('data.db')  # create connection
    c = conn.cursor()
    c.execute('''SELECT *, oid FROM data''')
    data = c.fetchall()
    cont = 0
    for element in data:
        if datetime.fromtimestamp(element[0]).strftime('%d/%m/%y') == today:
            if float(element[1]) > 29.0:

                regis_1.insert(parent='', index='end', iid=cont, values=(
                str(element[1]) + '°C', str(element[2]) + '°C', element[3], element[4],
                datetime.fromtimestamp(element[0]).strftime('%H:%M')), tags = ('highT',))
                cont = cont + 1
            else:
                regis_1.insert(parent='', index='end', iid=cont, values=(
                str(element[1]) + '°C', str(element[2]) + '°C', element[3], element[4],
                datetime.fromtimestamp(element[0]).strftime('%H:%M')))
                cont = cont + 1


    temp_graph = tk.Button(window, image = grph1, font=20, command = temp_plotting)
    temp_graph.place(x=260, y=241, height=42, width=42)

    hum_graph = tk.Button(window, image = grph2, font=20, command = hum_plotting)
    hum_graph.place(x=319, y=241, height=42, width=42)

    filt = tk.Button(window, image = fil_I, font=20, command = date_picker)
    filt.place(x=378, y=241, height=42, width=42)

def date_picker():
    #window features
    window = tk.Toplevel()
    bg_label = tk.Label(window, image=cldr).place(relheight=1, relwidth=1)
    window.geometry('380x255')
    window.title('Registros')
    window.iconbitmap('icon.ico')
    cal = Calendar(window, selectmode="day", year=2020, month=11, day=5, date_pattern='dd/mm/yy')

    cal.place(relheight = 0.8, relwidth = 1)

    get_date = tk.Button(window, image = slct, command = lambda: database_picked(cal.get_date()))
    get_date.place(x = 169, y = 208, height = 41, width = 42 )

def database_picked(d_picked):
    # window features
    window = tk.Toplevel()
    window.geometry('630x250')
    window.maxsize(630, 250)
    window.minsize(630, 250)
    window.title('Registros')
    window.iconbitmap('icon.ico')
    style = ttk.Style()
    style.theme_use('clam')
    bg_label = tk.Label(window, image=cldr).place(relheight=1, relwidth=1)

    regis_1 = ttk.Treeview(window)
    regis_1.pack(anchor='center')
    regis_1['columns'] = ['Temp. Exterior', 'Temp. Interior', 'Humedad Exterior', 'Humedad Interior', 'Hora']

    regis_1.column("#0", width=0, stretch='NO')
    regis_1.column("#1", width=120, anchor='center')
    regis_1.column("#2", width=120, anchor='center')
    regis_1.column("#3", width=120, anchor='center')
    regis_1.column("#4", width=120, anchor='center')
    regis_1.column("#5", width=80, anchor='center')

    regis_1.heading("#1", text='Temp. Exterior')
    regis_1.heading("#2", text='Temp. Interior')
    regis_1.heading("#3", text='Humedad Exterior')
    regis_1.heading("#4", text='Humedad Interior')
    regis_1.heading("#5", text=today)
    regis_1.tag_configure('highT', background='#f5978e')

    conn = sqlite3.connect('data.db')  # create connection
    c = conn.cursor()
    c.execute('''SELECT *, oid FROM data''')
    data = c.fetchall()
    cont = 0
    for element in data:
        if datetime.fromtimestamp(element[0]).strftime('%d/%m/%y') == d_picked:
            if float(element[1]) > 29.0:

                regis_1.insert(parent='', index='end', iid=cont, values=(
                    str(element[1]) + '°C', str(element[2]) + '°C', element[3], element[4],
                    datetime.fromtimestamp(element[0]).strftime('%H:%M')), tags=('highT',))
                cont = cont + 1
            else:
                regis_1.insert(parent='', index='end', iid=cont, values=(
                    str(element[1]) + '°C', str(element[2]) + '°C', element[3], element[4],
                    datetime.fromtimestamp(element[0]).strftime('%H:%M')))
                cont = cont + 1

#weather widget

def format_response(city):
    weather_key = 'a4aa5e3d83ffefaba8c00284de6ef7c3'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': weather_key, 'q': city}
    response = requests.get(url, params=params)
    weather = response.json()

    try:
        name = weather['name']
        desc = weather['weather'][0]['description']
        temp = weather['main']['temp']
        temp1 = str(int(temp) - 273)+'°C'
        final_str = 'Ciudad: %s \nTemperatura: %s' % (name, temp1)

    except:
        final_str = 'There was a problem retrieving that information'

    return final_str

#MQTT Conection

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK")

        main_GUI()


    else:
        print("Bad connection Returned code=", rc)

def mqtt_connection(mqtt_ip):
    mqtt.Client.connected_flag = False  # create flag in class
    client = mqtt.Client("Heiner")  # create new instance
    client.on_connect = on_connect  # bind call back function
    client.on_message = on_msg
    client.on_publish = on_publish
    try:
        print("Connecting to broker ", mqtt_ip)
        client.connect(mqtt_ip)  # connect to broker.
        client.subscribe('temp1')
        client.subscribe('temp_control')
        client.subscribe('cont')
        client.subscribe('temp2')
        client.subscribe('hum1')
        client.subscribe('hum2')

        #


    except:
        print('connection error')
        error_msg()

    client.loop_start()

def on_msg(client,userdata, msg):

    cont1.append(1)

    if len(cont1)==32:
        t1 = get_t1()
        t2 = get_t2()
        h1 = get_h1()
        h2 = get_h2()
        sub_sqdata(t1,t2,h1,h2)

    if msg.topic == 'temp1':
        payload = msg.payload.decode('utf-8')
        temp1_stack.append(payload)
        label0['text'] = str(payload) + '°C'

    elif msg.topic == 'temp2':
        payload = msg.payload.decode('utf-8')
        temp2_stack.append(payload)
        label1['text'] = str(payload) + '°C'

    elif msg.topic == 'hum1':
        payload = msg.payload.decode('utf-8')
        hum1_stack.append(payload)
        label2['text'] = str(payload)+"%"

    elif msg.topic == 'hum2':
        payload = msg.payload.decode('utf-8')
        hum2_stack.append(payload)
        label3['text'] = str(payload)+'%'

    elif msg.topic == 'temp_control':
        payload = msg.payload.decode('utf-8')
        print(payload)
        messagebox.showinfo(title="Nuevo Setpoint", message="El setpoint ha sido actualizado a "+ payload + '°C')

    elif msg.topic == 'cont':
        payload = msg.payload.decode('utf-8')
        messagebox.showinfo(title="Control manual", message="Control de riego activado")


def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

#Control

def updatesetpoint(newvalue, topic):
    try:
        client1 = mqtt.Client("cont1")  # create new instance
        client1.on_connect = on_connect  # bind call back function
        client1.on_message = on_msg
        client1.on_publish = on_publish
        client1.connect(mqtt_ip)  # connect to broker.

        nvi = int(newvalue)
        client1.publish(topic, nvi)
        client1.disconnect()
    except:
        messagebox.showerror(title="Valor invalido",
                             message="El valor ingresado debe ser un numero")

def update_power(topic):
    client2 = mqtt.Client("cont_pow")  # create new instance
    client2.on_connect = on_connect  # bind call back function
    client2.on_message = on_msg
    client2.on_publish = on_publish
    client2.connect(mqtt_ip)  # connect to broker.
    client2.publish(topic,1)
    client2.disconnect()

#GUI

def error_msg():
    messagebox.showerror(title="MQTT connection", message = "Ha ocurrido un error con la conexion, verifica los parametros de red e intentalo de nuevo")

def settings():
    sett_window = tk.Toplevel()
    sett_window.geometry('500x280')
    sett_window.title('Configuracion')
    sett_window.iconbitmap('icon.ico')
    sett_entry1 = tk.Entry(sett_window, bd = 2)
    sett_entry1.place(y = 0, x = 200, height = 30, width = 190)
    test_but = tk.Button(sett_window, command = lambda: print(sett_entry1.get()))
    test_but.place(y = 0, x = 400, height = 30, width = 50)
    labe_reh = tk.Label(sett_window, text = mqtt_ip, bg = '#324049')
    labe_reh.place(y = 100, x = 200, height = 30, width = 150)

def open_ubidots():
    webbrowser.open('http://127.0.0.1:5000/')


def info_f():

    inf_window = tk.Toplevel()
    inf_window.geometry('800x480')
    inf_window.maxsize(800, 480)
    inf_window.minsize(800, 480)
    inf_window.title('Ayuda')
    inf_window.iconbitmap('icon.ico')
    global  hlp_label
    hlp_label= tk.Label(inf_window, image = imag_list[0])
    hlp_label.grid(row = 0, column = 0, columnspan = 3)

    nxt = tk.Button(inf_window, command = lambda : fwrd(2), image = nxt_img)
    bck = tk.Button(inf_window,command=lambda: bck_fun(1), state = 'disabled', image = bck_img)
    nxt.place(x = 420, y = 420, height = 40, width = 40)
    bck.place(x=340, y=420, height=40, width=40)

    def fwrd(img_number):
        global hlp_label
        global nxt
        global bck
        hlp_label.grid_forget()
        hlp_label = tk.Label(inf_window, image=imag_list[img_number - 1])
        hlp_label.grid(row=0, column=0, columnspan=3)
        nxt = tk.Button(inf_window, command=lambda: fwrd(img_number + 1), image = nxt_img)
        bck = tk.Button(inf_window, command=lambda: bck_fun(img_number - 1), image = bck_img)
        if img_number==3:
            nxt = tk.Button(inf_window, command=lambda: fwrd(img_number + 1), state = 'disabled',image = nxt_img)

        nxt.place(x=420, y=420, height=40, width=40)
        bck.place(x=340, y=420, height=40, width=40)
        print(img_number)

    def bck_fun(img_number):
        global hlp_label
        global nxt
        global bck
        hlp_label.grid_forget()
        hlp_label = tk.Label(inf_window, image=imag_list[img_number - 1])
        hlp_label.grid(row=0, column=0, columnspan=3)
        nxt = tk.Button(inf_window, command=lambda: fwrd(img_number + 1), image = nxt_img)
        bck = tk.Button(inf_window, command=lambda: bck_fun(img_number - 1), image = bck_img)
        if img_number==1:
            bck = tk.Button(inf_window, command=lambda: fwrd(img_number + 1), state = 'disabled', image = bck_img)
        nxt.place(x=420, y=420, height=40, width=40)
        bck.place(x=340, y=420, height=40, width=40)
        print(img_number)

def secnd_GUI():
    #labels
    bg_label = tk.Label(root, image = scnd_ie).place(relheight = 1, relwidth = 1)
    label = tk.Label(root, bg = '#57606f', fg = 'white', text = format_response('Santa Clara, CR'), font = ('helvetica', 22), anchor ='nw')
    label.place(x = 83, y = 15)
    labeltime = tk.Label(root, bg = '#324049', fg = '#FFFFFF', font = ('helvetica', 18), anchor ='ne')
    #labeltime.place(x = 675, y = 12)

    b_data1 = tk.Button(root, image=data_image, bg='#EAEAEA', command=database, borderwidth=0)
    b_data1.place(x=22, y=164, width=43, height=44)

    ubi_button = tk.Button(root, bg='#EFEFEF', image=ubi_image, borderwidth='0', command=open_ubidots).place(x=22, y=98,    width=43,
                                                                                                             height=44)

    global row1  # Humedad 1
    row1 = tk.Label(root, bg='white', fg='#57606f', text="60%", font=('helvetica', 25), borderwidth='10')
    row1.place(x=150, y=190, height=30)

    global row2  # Humedad 2
    row2 = tk.Label(root, bg='white', fg='#57606f', text='65%', font=('helvetica', 25), borderwidth='10')
    row2.place(x=150, y=313, height=30)

    global row3  # Humedad 3
    row3 = tk.Label(root, bg='white', fg='#57606f', text='58%', font=('helvetica', 25), borderwidth='10')
    row3.place(x=315, y=190, height=30)

    global row4  # Humedad 4
    row4 = tk.Label(root, bg='white', fg='#57606f', text="69%", font=('helvetica', 25), borderwidth='10')
    row4.place(x=315, y=313, height=30)


    #entries

    e_row1 = tk.Entry(root, bg='white', fg='#57606f', text="25%", font=('helvetica', 15), borderwidth='0')
    e_row1.place(x=500, y=176, width=100)

    e_row2 = tk.Entry(root, bg='white', fg='#57606f', text="25%", font=('helvetica', 15), borderwidth='0')
    e_row2.place(x=500, y=236, width=100)

    e_row3 = tk.Entry(root, bg='white', fg='#57606f', text="25°C", font=('helvetica', 15), borderwidth='0')
    e_row3.place(x=500, y=300, width=100)

    e_row4 = tk.Entry(root, bg='white', fg='#57606f', text="25°C", font=('helvetica', 15), borderwidth='0')
    e_row4.place(x=500, y=355, width=100)

    SW_UI = tk.Button(root, image=SW_image, bg='#f6f7fb', command=main_GUI, borderwidth=0)
    SW_UI.place(x=735, y=421, width=50, height=50)

    #buttons

    # row1
    rfr_row1 = tk.Button(root, image = refresh_image, bg = 'white', borderwidth = 0, command = lambda : updatesetpoint(e_row1.get(),'hum_r1'))
    rfr_row1.place(x = 636, y = 168, width = 44, height = 40)

    pwt_row1 = tk.Button(root, image = pw2_image, bg = 'white', borderwidth = 0, command = lambda : update_power('cont_hum_r1'))
    pwt_row1.place(x = 702, y = 168, width = 44, height = 40)

    # row2
    rfr_row2 = tk.Button(root, image = refresh_image, bg = 'white', borderwidth = 0, command = lambda : updatesetpoint(e_row2.get(),'hum_r2'))
    rfr_row2.place(x = 636, y = 227, width = 44, height = 40)

    pwt_row2 = tk.Button(root, image = pw2_image, bg = 'white', borderwidth = 0, command = lambda : update_power('cont_hum_r2'))
    pwt_row2.place(x = 702, y = 227, width = 44, height = 40)

    # row3
    rfr_row3 = tk.Button(root, image = refresh_image, bg = 'white', borderwidth = 0, command = lambda : updatesetpoint(e_row3.get(),'hum_r3'))
    rfr_row3.place(x = 636, y = 286, width = 44, height = 40)

    pwt_row3 = tk.Button(root, image = pw2_image, bg = 'white', borderwidth = 0, command = lambda : update_power('cont_hum_r3'))
    pwt_row3.place(x = 702, y = 286, width = 44, height = 40)

    # row4
    rfr_row4 = tk.Button(root, image = refresh_image, bg = 'white', borderwidth = 0, command = lambda : updatesetpoint(e_row4.get(),'hum_r4'))
    rfr_row4.place(x = 636, y = 344, width = 44, height = 40)

    pwt_row4 = tk.Button(root, image = pw2_image, bg = 'white', borderwidth = 0, command = lambda : update_power('cont_hum_r4'))
    pwt_row4.place(x = 702, y = 344, width = 44, height = 40)

    #root.mainloop()

def main_GUI():

    #labels
    bg_label = tk.Label(root, image = bg_image).place(relheight = 1, relwidth = 1)
    label = tk.Label(root, bg = '#57606f', fg = 'white', text = format_response('Santa Clara, CR'), font = ('helvetica', 22), anchor ='nw')
    label.place(x = 83, y = 15)
    labeltime = tk.Label(root, bg = '#324049', fg = '#FFFFFF', font = ('helvetica', 18), anchor ='ne')
    #labeltime.place(x = 675, y = 12)

    global label0   #Temperatura Interior
    label0 = tk.Label(root, bg = 'white',fg = '#57606f', text = "25°C", font = ('helvetica', 40), borderwidth = '10')
    label0.place( x = 475,  y = 190, height = 60)

    global label1   #Temperatura Exterior
    label1 = tk.Label(root, bg = 'white', fg = '#57606f',  text = '28°C', font = ('helvetica', 40), borderwidth = '10')
    label1.place(x = 475, y = 305, height = 60)

    global label2   #humedad Interior
    label2 = tk.Label(root, bg = 'white', fg = '#57606f',  text = '58%', font = ('helvetica', 40), borderwidth = '10')
    label2.place(x = 160, y = 190, height = 60 )

    global label3 #humedad Exterior
    label3 = tk.Label(root, bg = 'white',fg = '#57606f', text = "69%", font = ('helvetica', 40), borderwidth = '10')
    label3.place( x = 160,  y = 305, height = 60)



    #entry

    sett_entry = tk.Entry(root, bg = '#e3e4ed', font = ('helvetica', 22), bd = 0)
    sett_entry.place(x = 283, y = 419, height = 40, width = 115)

    #buttons


    b_rfrtemp = tk.Button(root, image = refresh_image, bg = '#e3e4ed', borderwidth = 0, command = lambda : updatesetpoint(sett_entry.get(),'temp_control'))
    b_rfrtemp.place(x = 454, y = 419, width = 44, height = 44)

    b_pwtemp = tk.Button(root, image = pw2_image, bg = '#e3e4ed', borderwidth = 0, command = lambda : update_power('cont'))
    b_pwtemp.place(x = 523, y = 419, width = 44, height = 44)

    b_data1 = tk.Button(root, image = data_image, bg = '#EAEAEA', command = database, borderwidth = 0)
    b_data1.place(x = 22, y = 154, width = 43, height = 44)

    hilf_butt = tk.Button(root, image = info, bg = '#EAEAEA', command = info_f, borderwidth = 0)
    hilf_butt.place(x = 22, y = 219, width = 43, height = 44)

    ubi_button = tk.Button(root, bg = '#EFEFEF',  image = ubi_image, borderwidth = '0', command = open_ubidots).place(x = 22, y = 87, width = 43, height = 44)

    SW_UI = tk.Button(root, image = SW_image, bg = '#f6f7fb', command = secnd_GUI, borderwidth = 0)
    SW_UI.place(x = 735, y = 421, width = 50, height = 50)

    root.mainloop()

def log_GUI():
    bg_label = tk.Label(root, image = log_image).place(relwidth = 1, relheight = 1)
    ip_entry = tk.Entry(root, font = 30, bd = '0')
    ip_entry.place(x = 255, y = 205, width = 295, height = 35)
    conn_butt = tk.Button(root, bg = '#EAEAEA',  image = n_image, command = lambda : mqtt_connection(ip_entry.get()), bd = '0', borderwidth = 0)
    conn_butt.place(x = 263, y = 282, height = 35, width = 110)
    conn_butt2 = tk.Button(root, bg = '#EAEAEA', image = p_image, command = lambda : mqtt_connection(mqtt_ip), bd = '0', borderwidth = 0)
    conn_butt2.place(x = 438, y = 282, height = 35, width = 110)
    root.mainloop()

while True:
    log_GUI()
