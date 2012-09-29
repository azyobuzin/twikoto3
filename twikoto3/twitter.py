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
from twikoto3 import oauth

class Twitter:
    def __init__(self, consumerkey, consumersecret, oauthtoken, oauthtokensecret):
        self.consumerkey = consumerkey
        self.consumersecret = consumersecret
        self.oauthtoken = oauthtoken
        self.oauthtokensecret = oauthtokensecret

    def addoauthheader(self, req, method, callback, verifier, params):
        req.add_header("Authorization", oauth.createauthorizationheader(method, req.full_url, None, self.consumerkey, self.consumersecret, self.oauthtoken, self.oauthtokensecret, oauth.HMACSHA1, callback, verifier, params))

    #OAuth
    def getrequesttoken(self, callback = "oob"):
        req = urllib.request.Request("https://api.twitter.com/oauth/request_token")
        self.addoauthheader(req, "GET", callback, None, None)
        token = OAuthToken.parse(urllib.request.urlopen(req).read().decode("utf-8"))
        self.oauthtoken = token.token
        self.oauthtokensecret = token.secret
        return token

    def getaccesstoken(self, verifier):
        req = urllib.request.Request("https://api.twitter.com/oauth/access_token")
        self.addoauthheader(req, "GET", None, verifier, None)
        token = AccessToken.parse(urllib.request.urlopen(req).read().decode("utf-8"))
        self.oauthtoken = token.token
        self.oauthtokensecret = token.secret
        return token

    #Tweets
    def updatestatus(self, status, inreplytostatusid = -1):
        params = { "status": status }
        if inreplytostatusid > -1:
            params["in_reply_to_status_id"] = str(inreplytostatusid)
        req = urllib.request.Request("https://api.twitter.com/1.1/statuses/update.json", data = oauth.towwwformurlencoded(params).encode("ascii"))
        self.addoauthheader(req, "POST", None, None, params)
        urllib.request.urlopen(req).close()
        #TODO:パース

class OAuthToken:
    def __init__(self, token, secret):
        self.token = token
        self.secret = secret

    def parse(source):
        dic = oauth.parsewwwformurlencoded(source)
        return OAuthToken(dic["oauth_token"], dic["oauth_token_secret"])

class AccessToken(OAuthToken):
    def __init__(self, token, secret, userid, screenname):
        super(AccessToken, self).__init__(token, secret)
        self.userid = userid
        self.screenname = screenname

    def parse(source):
        dic = oauth.parsewwwformurlencoded(source)
        return AccessToken(dic["oauth_token"], dic["oauth_token_secret"], dic["user_id"], dic["screen_name"])
