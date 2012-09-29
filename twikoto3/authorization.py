# -*- coding: utf-8 -*-

import urllib.request
from PyQt4 import QtCore, QtGui, QtNetwork
import twikoto3
from twikoto3 import twitter
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
    requesttoken = twikoto3.twitter.getrequesttoken()
    dialog = InputPinDialog("https://api.twitter.com/oauth/authorize?oauth_token=" + requesttoken.token, inputedpin)
    dialog.show()

def inputedpin(dialog, verifier):
    if verifier | noneoremptystr():
        return

    try:
        accesstoken = twikoto3.twitter.getaccesstoken(verifier)

        twikoto3.setting.oauthtoken = accesstoken.token
        twikoto3.setting.oauthtokensecret = accesstoken.secret
        twikoto3.setting.userid = accesstoken.userid
        twikoto3.setting.screenname = accesstoken.screenname
        twikoto3.setting.savesetting()

        dialog.close()
    except Exception as ex:
        QtGui.QMessageBox.critical(dialog, "認証失敗", str(ex))
