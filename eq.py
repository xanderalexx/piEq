import RPi.GPIO as g
import time
import requests
import json
from lxml import html
from datetime import date
from kthread import KThread

session = requests.Session()
today = date.today()
id = ""

led1 = 21
led2 = 20
led3 = 16
led4 = 12
led5 = 7
led6 = 8
button = 14
stat = 15
B = 0

g.setmode(g.BCM)
g.setup(led1, g.OUT)
g.setup(led2, g.OUT)
g.setup(led3, g.OUT)
g.setup(led4, g.OUT)
g.setup(led5, g.OUT)
g.setup(led6, g.OUT)
g.setup(stat, g.OUT)
g.setup(button, g.IN)

latitude = "35.040554";
longitude = "-117.138306";
maxradius = "251.3414";
date = today.strftime("%y-%m-%d")
url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude=" + latitude + "&longitude=" + longitude + "&maxradiuskm=" + maxradius + "&orderby=time&limit=1" + "&starttime=" + date

initdata = session.get(url)
data = json.loads(initdata.text)

def setLeds(mag):
    if mag >= 1:
        g.output(led1, g.HIGH)
    if mag >= 2:
        g.output(led2, g.HIGH)
    if mag >= 3:
        g.output(led3, g.HIGH)
    if mag >= 4:
        g.output(led4, g.HIGH)
    if mag >= 5:
        g.output(led5, g.HIGH)
    if mag >= 6:
        g.output(led6, g.HIGH)

def neweq(mag):
    count = 0
    while g.input(button) == 0:
        print("high")
        g.output(led1, g.HIGH)
        time.sleep(0.1)
        g.output(led2, g.HIGH)
        time.sleep(0.1)
        g.output(led3, g.HIGH)
        time.sleep(0.1)
        g.output(led4, g.HIGH)
        time.sleep(0.1)
        g.output(led5, g.HIGH)
        time.sleep(0.1)
        g.output(led6, g.HIGH)
        time.sleep(0.1)
        g.output(stat, g.HIGH)
        time.sleep(0.1)
        print("low")
        g.output(led1, g.LOW)
        time.sleep(0.1)
        g.output(led2, g.LOW)
        time.sleep(0.1)
        g.output(led3, g.LOW)
        time.sleep(0.1)
        g.output(led4, g.LOW)
        time.sleep(0.1)
        g.output(led5, g.LOW)
        time.sleep(0.1)
        g.output(led6, g.LOW)
        time.sleep(0.1)
        g.output(stat, g.LOW)
        time.sleep(0.1)
    setLeds(mag)

while True:
    initdata = session.get(url)
    data = json.loads(initdata.text)
    data_ = data['features'][0]['properties']
    curtime = data['features'][0]['properties']['time']
    
    if curtime == id:
        g.output(stat, g.HIGH)
        time.sleep(0.2)
        g.output(stat, g.LOW)
    else:
        id = data_['time']
        mag = data_['mag']
        if B == 0:
            A = KThread(target=neweq(round(mag, 1)))
            B = 1
        else:
            A.kill()
        A.start()
        title = data_['title']
        print(str(mag) + ": " + title + ", ")
        
        #neweq(round(mag, 1))
    time.sleep(5)
