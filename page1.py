from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit
from _datetime import datetime
import sqlite3
import paho.mqtt.client as mqtt
import json
today = datetime.today().strftime('%d/%m/%y')

app = Flask(__name__)
app.config['SECRET KEY'] = 'tuhermana'
socketio = SocketIO(app)




def unix():
    conn = sqlite3.connect('C:/Users/Heiner L/PycharmProjects/pythonProject1/data.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM data")
    data = c.fetchall()
    list_y = []
    for element in data:
        tim = datetime.fromtimestamp(element[0]).strftime('%d:%m - %H:%M')
        list_y.append(tim)
    conn.commit()
    conn.close()
    return list_y

def last_value():
    conn = sqlite3.connect('C:/Users/Heiner L/PycharmProjects/pythonProject1/data.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM data ORDER BY oid DESC LIMIT 1")
    value = c.fetchone()
    conn.commit()
    conn.close()
    return value

def temp_int():
    conn = sqlite3.connect('C:/Users/Heiner L/PycharmProjects/pythonProject1/data.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM data")
    data = c.fetchall()
    list_y = []
    for element in data:
        list_y.append(element[1])
    conn.commit()
    conn.close()
    return list_y

def temp_ext():
    conn = sqlite3.connect('C:/Users/Heiner L/PycharmProjects/pythonProject1/data.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM data")
    data = c.fetchall()
    list_y = []
    for element in data:
        list_y.append(element[2])
    conn.commit()
    conn.close()
    return list_y

def hum_int():
    conn = sqlite3.connect('C:/Users/Heiner L/PycharmProjects/pythonProject1/data.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM data")
    data = c.fetchall()
    list_y = []
    for element in data:
        list_y.append(element[3])
    conn.commit()
    conn.close()
    return list_y

def hum_ext():
    conn = sqlite3.connect('C:/Users/Heiner L/PycharmProjects/pythonProject1/data.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM data")
    data = c.fetchall()
    list_y = []
    for element in data:
        list_y.append(element[4])
    conn.commit()
    conn.close()
    return list_y

l_valu = last_value()


temp = [
    {'temp1': str(l_valu[1]),
     'temp2': str(l_valu[2]),
     'hum1': str(l_valu[3]),
     'hum2': str(l_valu[4]),
    'fecha': str(datetime.fromtimestamp(l_valu[0]).strftime('%d/%m/%y'))
     }
]

@app.route('/')
def home():

    return render_template('temperatura.html')

@app.route('/temperatura', methods = ['GET', 'POST'])
def temperatura():

    return render_template('temperatura.html', temps = temp)

@app.route('/humedad')
def humedad():

    return render_template('humedad.html', temps = temp)
@app.route('/control', methods = ['GET', 'POST'])
def control():
    return render_template('control.html')

@app.route('/graph')
def graph(chartID='Temp', chart_type='line', chart_height=500):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
    series = [{"name": 'Interior', "data": temp_int()}, {"name": 'Exterior', "data": temp_ext()}]
    title = {"text": ' '}
    xAxis = {"categories": unix()}
    yAxis = {"title": {"text": 'Temperatura (°C)'}}

    return render_template('graph1.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)


@app.route('/graph1')
def graph1(chartID='Temp', chart_type='line', chart_height=500):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
    series = [{"name": 'Interior', "data": hum_int()}, {"name": 'Exterior', "data": hum_ext()}]
    title = {"text": ' '}
    xAxis = {"categories": unix()}
    yAxis = {"title": {"text": 'Humedad Relativa (%)'}}

    return render_template('graph2.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)



if __name__ == '__main__':
    socketio.run(app, debug=True)

