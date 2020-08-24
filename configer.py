from json import load,dump
from os import access,F_OK


default={
	"lang":"en"
}


class Config:
	def __init__(self):
		if access('config.json',F_OK):
			with open('config.json',encoding='utf-8') as file:
				self.data=load(file)
		else:
			self.data=default
			self.update()

	def __getitem__(self,key):
		return self.data[key]

	def __setitem__(self,key,value):
		self.data[key]=value
		self.update()

	def update(self):
		with open('config.json','w',encoding='utf-8') as file:
			dump(self.data,file)


config=Config()