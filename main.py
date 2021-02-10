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

    client.app = None

    client.notified = False

    return


def update():
    # if toggle is set to on, check if adobe app is open and set rich presence or exit.
    if toggle:
        print('hi')
        appname = str(window())
        print(appname + " preliminary")
        desc = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        cid = ""
        params = {}

        for i in apps:
            if str(appname) == str(i['exe']):
                for n in ids.lst:
                    if appname == n['exe']:
                        cid = n['clientid']
                        params['large_image'] = n['large_image']

                        if i['show_title']:
                            params['details'] = desc

                        if client.timer['app'] != appname:
                            client.timer['start'] = time.time()

                        params['start'] = client.timer['start']

                        print(appname + " matched")

                        break
                break

        print(cid)

        # Set app name to compare for next time, must be done before potential return
        client.timer['app'] = appname

        if cid == "":
            clearpresence()

        else:
            if client.active_presence != cid:
                print(str(Presence(cid)) + "expected")
                clearpresence()
                client.rpclient = Presence(cid)
                client.rpclient.connect()
                client.rpclient.update(**params)
                print(str(client.rpclient) + 'updated new')

            if client.active_presence == cid:
                client.rpclient.update(**params)
                print(str(client.rpclient) + 'existing')

        client.active_presence = cid

        if params != '' and cid:
            if not client.notified:
                toaster.show_toast("Adobe RPC",
                                   "You're now using " + str(appname),
                                   icon_path="favicon.ico",
                                   duration=3,
                                   threaded=True)
                print('nonempty')
                client.notified = True

    return
