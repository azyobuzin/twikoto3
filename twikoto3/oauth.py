# -*- coding: utf-8 -*-

#YacqOAuthから移植

import base64
import hashlib
import hmac
import random
import time
import urllib.parse
from twikoto3.extension import *

HMACSHA1 = "HMAC-SHA1"
RSASHA1 = "RSA-SHA1"
PLAINTEXT = "PLAINTEXT"

OAUTHVERSION = "1.0"

ALLOWEDCHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-._~"

def percentencode(text):
	return "".join(c if ALLOWEDCHARS.find(c) != -1 else "".join("%%%X" % b for b in c.encode("utf-8")) for c in text)

def normalizeuri(uri):
	parseduri = urllib.parse.urlparse(uri)
	return "%s://%s%s%s" % (parseduri.scheme, parseduri.hostname, "" if parseduri.port is None or (parseduri.scheme == "http" and parseduri.port == 80) or (parseduri.scheme == "https" and parseduri.port == 443) else ":" + str(parseduri.port), parseduri.path)

def normalizeparameters(params):
	return "&".join(percentencode(item[0]) + "=" + percentencode(item[1]) for item in sorted(dict(params).items(), key = lambda item: item[0]))

def parsewwwformurlencoded(source):
	return dict(_.split("=") | let(lambda s: (urllib.parse.unquote(s[0]), urllib.parse.unquote(s[1]) if len(s) > 1 else "")) for _ in (source[1:] if source.startswith("?") else source).split("&") if _ != "")

def towwwformurlencoded(source):
	return "&".join(urllib.parse.quote(item[0]) + "=" + urllib.parse.quote(item[1]) for item in dict(source).items())

def timestamp():
	return str(int(time.time()))

def nonce():
	return "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for i in range(42))

def signparametersbase(realm, consumerkey, token, signaturemethod, timestamp, nonce, callback, verifier):
	dic = { "oauth_version": OAUTHVERSION }
	
	if not realm | noneoremptystr(): dic["realm"] = realm
	if not consumerkey | noneoremptystr(): dic["oauth_consumer_key"] = consumerkey
	if not token | noneoremptystr(): dic["oauth_token"] = token
	if not signaturemethod | noneoremptystr(): dic["oauth_signature_method"] = signaturemethod
	if not timestamp | noneoremptystr(): dic["oauth_timestamp"] = timestamp
	if not nonce | noneoremptystr(): dic["oauth_nonce"] = nonce
	if not callback | noneoremptystr(): dic["oauth_callback"] = callback
	if not verifier | noneoremptystr(): dic["oauth_verifier"] = verifier
	
	return dic

def signaturebase(httpmethod, uri, signparams, params):
	return "&".join((
		httpmethod.upper(),
		percentencode(normalizeuri(uri)),
		percentencode(normalizeparameters(
			dict(signparams)
			| apply(lambda dic: dic.update(params | none(())))
			| apply(lambda dic: dic.update(parsewwwformurlencoded(urllib.parse.urlparse(uri).query)))
		))
	))

def signaturekey(consumersecret, tokensecret):
	return percentencode(consumersecret | none("")) + "&" + percentencode(tokensecret | none(""))

def signature(basestring, key, signaturemethod):
	if signaturemethod == HMACSHA1:
		return base64.b64encode(hmac.new(key.encode("ascii"), basestring.encode("ascii"), hashlib.sha1).digest()).decode("ascii")
	elif signaturemethod == PLAINTEXT:
		return key
	else:
		raise NotImplementedError()

def signparameters(httpmethod, uri, realm, consumerkey, consumersecret, token, tokensecret, signaturemethod, callback, verifier, params):
	isplaintext = signaturemethod == PLAINTEXT
	signparams = signparametersbase(realm, consumerkey, token, signaturemethod, None if isplaintext else timestamp(), None if isplaintext else nonce(), callback, verifier)
	signparams["oauth_signature"] = signature(signaturebase(httpmethod, uri, signparams, params), signaturekey(consumersecret, tokensecret), signaturemethod)
	return signparams

def createauthorizationheader(httpmethod, uri, realm, consumerkey, consumersecret, token, tokensecret, signaturemethod, callback, verifier, params):
	return "OAuth " + ",".join(
		percentencode(item[0]) + "=" + percentencode(item[1])
		for item in signparameters(httpmethod, uri, realm, consumerkey, consumersecret, token, tokensecret, signaturemethod, callback, verifier, params).items()
	)
