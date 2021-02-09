from ctypes import windll

import win32gui
import win32process
import wmi
from pypresence import Presence
from win10toast import ToastNotifier

import client

with open('config.txt') as configfile:
    apps = eval(configfile.read())

c = wmi.WMI()
toaster = ToastNotifier()

global rpclient
global toggle

toggle = True


def window():
    w = windll.user32.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(w)
    for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
        exe = p.name
    if exe:
        return exe[:-4].lower()



def update():

    if not toggle:
        if client.rpclient is not None:
            client.rpclient.close()
            return

    appname = str(window())

    cid = ""
    params = {}

    for i in apps:
        if appname == i['exe']:
            if client.rpclient is not None:
                client.rpclient.close()
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

    if cid == "":
        if client.rpclient is not None:
            client.rpclient.close()
            return

    if toggle:
        print(appname)
        print(cid)
        if cid != "":
            client.rpclient = Presence(cid)
            client.rpclient.connect()
            if params != '':
                toaster.show_toast("Adobe RPC",
                                   "You're now using "+params['state'],
                                   icon_path="cc.ico",
                                   duration=3,
                                   threaded=True)
                print('notempty')
                client.rpclient.update(**params)
