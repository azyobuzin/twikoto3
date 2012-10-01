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

import json
import traceback
import urllib.request
from PyQt4 import QtCore
from twikoto3 import oauth
from twikoto3.twitter import twdatamodel

class AsyncConnection(QtCore.QThread):
    def __init__(self, action, parse, parent = None):
        super(AsyncConnection, self).__init__(parent)
        self.action = action
        self.parse = parse
        self.headers = None
        self.response = None
        self.exception = None

    def run(self):
        try:
            res = self.action()
            self.headers = dict(res.getheaders())
            self.response = self.parse(res.read().decode("utf-8"))
            res.close()
        except Exception as ex:
            traceback.print_exc()
            self.exception = ex

class Twitter:
    def __init__(self, consumerkey, consumersecret, oauthtoken, oauthtokensecret):
        self.consumerkey = consumerkey
        self.consumersecret = consumersecret
        self.oauthtoken = oauthtoken
        self.oauthtokensecret = oauthtokensecret

    def addoauthheader(self, req, method, callback, verifier, params):
        req.add_header("Authorization", oauth.createauthorizationheader(method, req.full_url, None, self.consumerkey, self.consumersecret, self.oauthtoken, self.oauthtokensecret, oauth.HMACSHA1, callback, verifier, params))

    def asyncmethod(parse):
        def wrapped(func):
            def wrappedwrapped(*args, **kwargs):
                thread = AsyncConnection(lambda: func(*args, **kwargs), parse)
                return thread

            return wrappedwrapped
        return wrapped

    #OAuth
    @asyncmethod(twdatamodel.OAuthToken.parse)
    def getrequesttoken(self, callback = "oob"):
        req = urllib.request.Request("https://api.twitter.com/oauth/request_token")
        self.addoauthheader(req, "GET", callback, None, None)
        return urllib.request.urlopen(req)

    @asyncmethod(twdatamodel.AccessToken.parse)
    def getaccesstoken(self, verifier):
        req = urllib.request.Request("https://api.twitter.com/oauth/access_token")
        self.addoauthheader(req, "GET", None, verifier, None)
        return urllib.request.urlopen(req)

    #Tweets
    @asyncmethod(json.loads)
    def updatestatus(self, status, inreplytostatusid = -1):
        params = { "status": status }
        if inreplytostatusid > -1:
            params["in_reply_to_status_id"] = str(inreplytostatusid)
        req = urllib.request.Request("https://api.twitter.com/1.1/statuses/update.json", data = oauth.towwwformurlencoded(params).encode("ascii"))
        self.addoauthheader(req, "POST", None, None, params)
        return urllib.request.urlopen(req)
