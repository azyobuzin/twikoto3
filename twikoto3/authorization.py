# -*- coding: utf-8 -*-

"""
    twikoto3 - Twitter Client
    Copyright (C) 2012 azyobuzin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import urllib.request
from PyQt4 import QtCore, QtGui, QtNetwork
import twikoto3
from twikoto3 import mainwindow, twitter
from twikoto3.extension import *

class InputPinDialog(QtGui.QDialog):
    def __init__(self, uri, okaction, parent = None):
        super(InputPinDialog, self).__init__(parent)

        self.layout = QtGui.QVBoxLayout()

        self.label_openbrowser = QtGui.QLabel("1. 次のURIをブラウザで開いて、ついこと 3 を認証してください：")
        self.layout.addWidget(self.label_openbrowser)

        self.lineedit_uri = QtGui.QLineEdit(uri)
        self.lineedit_uri.setReadOnly(True)
        self.layout.addWidget(self.lineedit_uri)
        self.lineedit_uri.selectAll()

        self.label_inputpin = QtGui.QLabel("2. PINを入力してください：")
        self.layout.addWidget(self.label_inputpin)

        self.lineedit_pin = QtGui.QLineEdit()
        self.layout.addWidget(self.lineedit_pin)

        self.layout_buttons = QtGui.QHBoxLayout()

        self.button_ok = QtGui.QPushButton("OK")
        self.button_ok.clicked.connect(lambda: okaction(self, self.lineedit_pin.text()))
        self.layout_buttons.addWidget(self.button_ok)

        self.button_cancel = QtGui.QPushButton("Cancel")
        self.button_cancel.clicked.connect(lambda: self.close())
        self.layout_buttons.addWidget(self.button_cancel)

        self.layout.addLayout(self.layout_buttons)

        self.setLayout(self.layout)
        self.setWindowTitle("Twitter 認証")
        self.setWhatsThis("Twitterにログインして、ついこと 3 のアクセスを許可してください。")

def authorize():
    thread = twikoto3.twitter.getrequesttoken()
    thread.start()
    thread.wait()

    requesttoken = thread.response

    twikoto3.twitter.oauthtoken = requesttoken.token
    twikoto3.twitter.oauthtokensecret = requesttoken.secret

    dialog = InputPinDialog("https://api.twitter.com/oauth/authorize?oauth_token=" + requesttoken.token, inputedpin)
    dialog.show()

def inputedpin(dialog, verifier):
    if verifier | noneoremptystr():
        return

    dialog.button_ok.setEnabled(False)

    thread = twikoto3.twitter.getaccesstoken(verifier)

    def finished():
        if thread.response is not None:
            accesstoken = thread.response

            twikoto3.twitter.oauthtoken = accesstoken.token
            twikoto3.twitter.oauthtokensecret = accesstoken.secret

            twikoto3.setting.oauthtoken = accesstoken.token
            twikoto3.setting.oauthtokensecret = accesstoken.secret
            twikoto3.setting.userid = accesstoken.userid
            twikoto3.setting.screenname = accesstoken.screenname
            twikoto3.setting.savesetting()

            mainwindow.MainWindow.getinstance().show()
            dialog.close()
        else:
            dialog.button_ok.setEnabled(True)
            QtGui.QMessageBox.critical(dialog, "認証失敗", str(ex))

    thread.finished.connect(finished)
    thread.start()
