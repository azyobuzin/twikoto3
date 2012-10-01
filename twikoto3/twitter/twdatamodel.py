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

from twikoto3 import oauth

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
