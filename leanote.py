#!/usr/bin/python
# -*- coding: utf-8 -*-

from requests import Session
import json

class Leanote(Session):
	def __init__(self, baseUrl):
		Session.__init__(self)
		self.baseUrl = baseUrl

	def login(self, email, password):
		url = self.baseUrl + '/api/auth/login'
		data = {
			"email": email,
			"pwd": password
		}
		response = self.post(url, data=data)
		jsonObj = response.json()
		print('login: %s' % jsonObj)
		assert jsonObj['Ok']
		self.token = jsonObj['Token']

	def getNotebooks(self):
		url = self.baseUrl + '/api/notebook/getNotebooks?token=%s' % self.token
		response = self.get(url)
		jsonObj = json.loads(response.content)
		return jsonObj

	def addNote(self, note):
		url = self.baseUrl + '/api/note/addNote?token=%s' % self.token
		response = self.post(url, data = note)
		print('addNote: %s' % response)

	def updateNote(self, note):
		url = self.baseUrl + '/api/note/updateNote?token=%s' % self.token
		response = self.post(url, data = note)
		print('updateNote: %s' % response)

	def getNotes(self, notebookId):
		url = self.baseUrl + '/api/note/getNotes?token=%s&notebookId=%s' % (self.token, notebookId)
		response = self.get(url)
		jsonObj = json.loads(response.content, cls=Note)
		return jsonObj

	def getNoteAndContent(self, noteId):
		url = self.baseUrl + '/api/note/getNoteAndContent?token=%s&noteId=%s' % (self.token, noteId)
		response = self.get(url)
		jsonObj = json.loads(response.content)
		return jsonObj

	def getNoteContent(self, noteId):
		url = self.baseUrl + '/api/note/getNoteContent?token=%s&noteId=%s' % (self.token, noteId)
		response = self.get(url)
		jsonObj = json.loads(response.content)
		return jsonObj
