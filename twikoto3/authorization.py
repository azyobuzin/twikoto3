# -*- coding: utf-8 -*-

import urllib.request
from PyQt4 import QtCore, QtGui, QtNetwork
import twikoto3
from twikoto3 import twitter
from twikoto3.extension import *

class InputPinDialog(QtGui.QDialog):
    def __init__(self, uri, parent = None):
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
        self.layout_buttons.addWidget(self.button_ok)

        self.button_cancel = QtGui.QPushButton("Cancel")
        self.button_cancel.clicked.connect(lambda: self.close())
        self.layout_buttons.addWidget(self.button_cancel)

        self.layout.addLayout(self.layout_buttons)

        self.setLayout(self.layout)
        self.setWindowTitle("Twitter 認証")
        self.setWhatsThis("Twitterにログインして、ついこと 3 のアクセスを許可してください。")

requesttoken_reply = none
requesttoken = None

def authorize():
    requesttoken_reply = twikoto3.twitter.getrequesttoken()
    requesttoken_reply.finished.connect(requesttoken_callback)
    requesttoken_reply.error.connect(requesttoken_error)

def requesttoken_callback():
    requesttoken = twitter.OAuthToken.parse(requesttoken_reply.readAll())
    dialog = InputPinDialog("https://api.twitter.com/oauth/authorize?oauth_token=" + requesttoken.token)
    dialog.show()

def requesttoken_error(error):
    pass
