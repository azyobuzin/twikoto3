# -*- coding: utf-8 -*-

import pickle
import sys
from PyQt4 import QtCore, QtGui, QtNetwork
from twikoto3 import authorization, twitter
from twikoto3.extension import *

class Setting:
    settingfilename = "setting.pickle"

    def __init__(self):
        #初期値設定
        self.oauthtoken = None
        self.oauthtokensecret = None
        self.userid = None
        self.screenname = None

    def authorized(self):
        return not (self.oauthtoken | noneoremptystr() or self.oauthtokensecret | noneoremptystr())

    def loadsetting():
        try:
            with open(Setting.settingfilename, "rb") as file:
                return pickle.load(file)
        except:
            return Setting()

    def savesetting(self):
        with open(Setting.settingfilename, "wb") as file:
            pickle.dump(self, file)

def main():
    app = QtGui.QApplication(sys.argv)

    if not setting.authorized():
        authorization.authorize()

    resultcode = app.exec_()

    setting.savesetting()

    return resultcode

#初期化
CONSUMERKEY = "rPk6ZkNtE5SZbbKxBkMi3w"
CONSUMERSECRET = "djSfqabHwUBQtfdeOwHk1stGHJpoOGe0f9GhG6K3c4"
setting = Setting.loadsetting()
twitter = twitter.Twitter(CONSUMERKEY, CONSUMERSECRET, setting.oauthtoken, setting.oauthtokensecret)
