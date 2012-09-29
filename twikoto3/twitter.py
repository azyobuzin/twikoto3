# -*- coding: utf-8 -*-

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

    def createmanager(self):
        #TODO:プロキシ対応など
        return QtNetwork.QNetworkAccessManager()

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
