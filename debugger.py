#! /usr/bin/python

# A PyQt tool to help in the debugging of Sage.
# Copyright 2013 Miguel Angel Marco Buzunariz.


# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


import sys
import dbus
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import time


class Debugger(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        self.ui = uic.loadUi("debugger.ui")
        self.history = []
        self.nhistory = 0
        self.ui.show()

    def tracecommand(*args):
        window.history = []
        window.nhistory = 0
        konsoleproxy.runCommand(
            'trace(\''+str(window.ui.tracecommand.text())+'\')')
        window.prints()

    def printn(*args):
        konsoleproxy.runCommand('next')
        window.actualize()

    def printuntil(*args):
        konsoleproxy.runCommand('until')
        window.actualize()

    def printr(*args):
        konsoleproxy.runCommand('return')
        window.actualize()

    def printq(*args):
        konsoleproxy.runCommand('quit')

    def prints(*args):
        konsoleproxy.runCommand('step')
        window.actualize()

    def backbutton(*args):
        window.nhistory -= 1
        window.showhistory()

    def forwardbutton(*args):
        window.nhistory += 1
        window.showhistory()

    def showhistory(*args):
        katefilestring = window.history[window.nhistory][0]
        katefileline = window.history[window.nhistory][1]
        kateproxy.openUrl(u"file:/"+katefilestring, "ascii")
        kateproxy.setCursor(katefileline-1, 0)
        window.ui.localslist.setRowCount(0)
        listparsed = window.history[window.nhistory][2]
        for entry in listparsed:
            rowNum = window.ui.localslist.rowCount()
            window.ui.localslist.insertRow(rowNum)
            window.ui.localslist.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(entry[0]))
            window.ui.localslist.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(entry[1]))
            # window.ui.localslist.resizeColumnsToContents()
        if window.nhistory == 0:
            window.ui.backbutton.setDisabled(True)
        else:
            window.ui.backbutton.setEnabled(True)
        if window.nhistory == len(window.history)-1:
            window.ui.forwardbutton.setDisabled(True)
        else:
            window.ui.forwardbutton.setEnabled(True)

    def actualize(*args):
        tries = 0
        while True:
            tries += 1
            if tries > 20:
                return
            try:
                time.sleep(0.1)
                logfile = open(str(window.ui.logfilerequester.text()))
                logfilelines = logfile.readlines()
                stringparsed = logfilelines[-8]
                a = stringparsed.index('(')
                b = stringparsed.index(')')
                katefilestring = stringparsed[10:a-4]
                katefileline = int(stringparsed[a+1:b])
                logfile.close()
                break
            except (ValueError):
                pass
        konsoleproxy.runCommand('[(a[0],str(a[1])) for a in locals().items()]')
        time.sleep(0.2)
        logfile = open(str(window.ui.logfilerequester.text()))
        logfilelines = logfile.readlines()
        stringparsed = logfilelines[-2]
        logfile.close()
        try:
            listparsed = eval(stringparsed)
        except:
            listparsed = []
        listparsed.sort()
        window.history.append([katefilestring, katefileline, listparsed])
        window.nhistory = len(window.history)-1
        window.showhistory()
        # konsoleproxy.runCommand('globals()')


if __name__ == "__main__":
    bus = dbus.SessionBus()
    katebus = list(filter(lambda i: 'kate' in i, [
                   aa.__str__() for aa in bus.list_names()]))[0]
    konsoleproxy = bus.get_object(katebus, '/Sessions/1')
    kateproxy = bus.get_object(katebus, '/MainApplication')
    fileline = None
    app = QtWidgets.QApplication(sys.argv)
    window = Debugger()
    window.ui.nbutton.clicked.connect(window.printn)
    window.ui.qbutton.clicked.connect(window.printq)
    window.ui.sbutton.clicked.connect(window.prints)
    window.ui.rbutton.clicked.connect(window.printr)
    window.ui.untilbutton.clicked.connect(window.printuntil)
    window.ui.backbutton.clicked.connect(window.backbutton)
    window.ui.forwardbutton.clicked.connect(window.forwardbutton)
    window.ui.tracecommand.returnPressed.connect(window.tracecommand)
    sys.exit(app.exec_())
