# -*- coding: utf-8 -*-

import pickle

#設定ファイルの管理
class Setting: 
	settingfilename = "setting.pickle"
	
	def __init__(self):
		#初期値設定
		self.oauthtoken = None
		self.oauthtokensecret = None
	
	def loadsetting():
		try:
			with open(Setting.settingfilename, "rb") as file:
				return pickle.load(file)
		except:
			return Setting()
	
	def savesetting(self):
		with open(Setting.settingfilename, "wb") as file:
			pickle.dump(self, file)

#実際に起動
def mainloop():
	setting.savesetting()

#初期化
setting = Setting.loadsetting()
