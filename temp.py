import threading
from threading import Timer, Thread

import win32gui
import win32process
import psutil
import wmi
from pypresence import Presence
import client

with open('config.txt') as configfile:
    apps = eval(configfile.read())

c = wmi.WMI()
w = win32gui

global rpclient
global toggle


def window():
    w.GetWindowText(w.GetForegroundWindow())

    pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow())

    return psutil.Process(pid[-1]).name()[:-4].lower()


def update():
    appname = str(window())

    print(str(toggle))

    cid = ""
    params = {}

    for i in apps:
        if appname == i['exe']:
            # since details can't be empty
            params['details'] = ''

            if i['exe'] == 'adobe premiere pro':
                print('connected')
                cid = "807790581177778186"
                params['state'] = str(i['name'])
                params['large_image'] = 'premiere_pro'
                params['small_image'] = 'cc'

            elif i['exe'] == 'afterfx':
                print('connected')
                cid = "808468724075069491"
                params['state'] = str(i['name'])
                params['large_image'] = 'after_effects'
                params['small_image'] = 'cc'

            elif i['exe'] == 'photoshop':
                print('connected')
                cid = "808468822608314409"
                params['state'] = str(i['name'])
                params['large_image'] = 'photoshop'
                params['small_image'] = 'cc'

            if i['show_title']:
                desc = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                params['details'] = desc

            break

    if toggle:
        print(appname)
        print(cid)
        if cid != "":
            client.rpclient = Presence(cid)  # Initialize the Presence client
            client.rpclient.connect()
            client.rpclient.update(**params)

        if cid == "":
            if client.rpclient is not None:
                client.rpclient.close()