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

from PyQt4 import QtCore, QtGui
import twikoto3
from twikoto3.extension import *
from twikoto3.twittertext import validator

class TweetTextEdit(QtGui.QTextEdit):
    def __init__(self, parent = None):
        super(TweetTextEdit, self).__init__(parent)
        self.tweetaction = None

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return and (e.modifiers() and QtCore.Qt.ControlModifier):
            self.tweetaction()
        else:
            super(TweetTextEdit, self).keyPressEvent(e)

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("ついこと 3")

        self.layout = QtGui.QVBoxLayout()

        self.textedit_tweet = TweetTextEdit()
        self.textedit_tweet.setMinimumHeight(46)
        self.textedit_tweet.textChanged.connect(self.textedit_tweet_textChanged)
        self.textedit_tweet.tweetaction = self.button_tweet_clicked
        self.layout.addWidget(self.textedit_tweet)

        self.layout_tweetbutton = QtGui.QHBoxLayout()
        self.layout.addLayout(self.layout_tweetbutton)

        self.label_textcount = QtGui.QLabel("140")
        self.layout_tweetbutton.addWidget(self.label_textcount)

        self.button_tweet = QtGui.QPushButton("Tweet")
        self.button_tweet.clicked.connect(self.button_tweet_clicked)
        self.layout_tweetbutton.addWidget(self.button_tweet)

        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

    def button_tweet_clicked(self):
        status = self.textedit_tweet.toPlainText()
        if status | noneoremptystr():
            return

        self.button_tweet.setEnabled(False)
        thread = twikoto3.twitter.updatestatus(status)

        def finished():
            self.button_tweet.setEnabled(True)
            if thread.response is not None:
                self.textedit_tweet.setPlainText("")
            else:
                QtGui.QMessageBox.critical(self, "投稿失敗", str(thread.exception))

        thread.finished.connect(finished)
        thread.start()

    def textedit_tweet_textChanged(self):
        self.label_textcount.setText(str(validator.MAX_TWEET_LENGTH - validator.getTweetLength(self.textedit_tweet.toPlainText())))

    instance = None
    def getinstance():
        if MainWindow.instance is None:
            MainWindow.instance = MainWindow()

        return MainWindow.instance
