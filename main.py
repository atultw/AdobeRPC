import sys
from datetime import datetime
from ctypes import windll
import time

import win32gui
import win32process
import wmi
from pypresence import Presence
from win10toast import ToastNotifier

import client
import ids

with open('config.txt') as configfile:
    apps = eval(configfile.read())

c = wmi.WMI()
toaster = ToastNotifier()
toggle = True


def window():
    exe = "none"
    w = windll.user32.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(w)
    for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
        exe = p.name

    return exe[:-4].lower()


def clearpresence():
    # if client.rpclient:
    print('clearing client')
    try:
        client.rpclient.close()
    except AttributeError:
        print('already closed')

    client.rpclient = None

    client.timer = dict({
        'app': None,
        'start': 0
    })

    client.active_presence = None

    client.notified = False

    return



def update():
    # if toggle is set to on, check if adobe app is open and set rich presence or exit.
    if toggle:
        print('hi')
        appname = str(window())
        print(appname + " detected")
        desc = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        cid = ""
        params = {}

        for i in apps:
            if str(appname) == str(i['exe']):
                for n in ids.lst:
                    if appname == n['exe']:
                        friendlyname = i['name']

                        cid = n['clientid']
                        params['large_image'] = n['large_image']

                        if i['show_title']:
                            params['details'] = desc

                        if client.timer['app'] != appname:
                            client.timer['start'] = time.time()

                        print('the client timer is set to' + str(client.timer['app']))

                        params['start'] = client.timer['start']

                        # Set app name to compare for next time, must be done before potential return

                        print(appname + " matched")

                        break
                break

        if cid == "":
            clearpresence()
            return

        else:
            if client.active_presence != cid:
                print(str(client.active_presence) + "expected")
                clearpresence()
                client.rpclient = Presence(cid)
                client.rpclient.connect()
                client.rpclient.update(**params)
                print(cid + 'updated new')

            if client.active_presence == cid:
                if params['start'] >= 1:
                    client.rpclient.update(**params)
                else:
                    print('time was not valid')

                print(client.active_presence + 'existing')

            print(params['start'])

        client.active_presence = cid
        client.timer['app'] = appname

        if params != '' and cid:
            if not client.notified:
                toaster.show_toast("Adobe RPC",
                                   "You're now using " + str(friendlyname) if friendlyname else str(appname),
                                   icon_path="favicon.ico",
                                   duration=3,
                                   threaded=True)
                print('nonempty')
                print("")
                client.notified = True

    return
