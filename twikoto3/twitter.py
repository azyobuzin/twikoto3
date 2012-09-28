# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtNetwork
from twikoto3 import oauth

class Twitter:
    def __init__(self, consumerkey, consumersecret, oauthtoken, oauthtokensecret):
        self.consumerkey = consumerkey
        self.consumersecret = consumersecret
        self.oauthtoken = oauthtoken
        self.oauthtokensecret = oauthtokensecret

    def createrequest(self, method, uri, callback, verifier, params):
        req = QtNetwork.QNetworkRequest(QtCore.QUrl(uri))
        req.setRawHeader("Authorization", oauth.createauthorizationheader(method, uri, None, self.consumerkey, self.consumersecret, self.oauthtoken, self.oauthtokensecret, oauth.HMACSHA1, callback, verifier, params))
        return req

    def createmanager(self):
        #TODO:プロキシ対応など
        return QtNetwork.QNetworkAccessManager()

    #OAuth
    def getrequesttoken(self, callback = "oob"):
        req = self.createrequest("POST", "https://api.twitter.com/oauth/request_token", callback, None, None)
        return self.createmanager().get(req)

class OAuthToken:
    def __init__(token, secret):
        self.token = token
        self.secret = secret

    def parse(source):
        dic = oauth.parsewwwformurlencoded(source)
        re = OAuthToken(dic["oauth_token"], dic["oauth_token_secret"])
