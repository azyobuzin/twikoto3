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
