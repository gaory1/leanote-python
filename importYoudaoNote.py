#!/usr/bin/python
# -*- coding: utf-8 -*-

from leanote import Leanote
from lxml import etree
import os
import time
import json
import sys

def removeTag(node, tagName):
	for i in node.getchildren():
		tag = i.tag.replace('{http://note.youdao.com}', '')
		if tag == tagName:
			node.remove(i)
		else:
			removeTag(i, tagName)

def getNoteText(xmlFileName):
	with open(xmlFileName) as f:
		content = f.read()
	content = content.replace('&nbsp;', ' ')\
		.replace('<br>', '\n') \
		.replace('<br >', '\n') \
		.replace('<br />', '\n')\
		.replace('<br/>', '\n')
	if not content.startswith('<?xml'):
		content = '<html>' + content + '</html>'
	root = etree.fromstring(content)
	removeTag(root, 'coId')

	notags = etree.tostring(root, encoding='utf8', method='text')
	return notags


def addSingleNote(xmlFile, jsonFile, notebookId, tags = []):
	noteContent = getNoteText(xmlFile)
	with open(jsonFile) as f:
		jsonObj = json.load(f)
	title = jsonObj['fileEntry']['name'].replace('.note', '')
	createTime = int(jsonObj['fileEntry']['createTimeForSort'])
	modifyTime = jsonObj['fileEntry']['modifyTimeForSort']
	createTimeStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(createTime))
	modifyTimeStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modifyTime))
	noteContent = noteContent + '<br/><p style="text-align: right;">' + modifyTimeStr + '</p>'
	note = {
		'NotebookId': notebookId,
		'Title': title,
		'Tags': tags,
		'Content': noteContent,
		'IsMarkdown': False,
		'CreatedTime': createTimeStr,
		'UpdatedTime': modifyTimeStr
	}
	leanote.addNote(note)

def addFolder(dir, notebookId):
	os.chdir(dir)
	for xmlFile in os.listdir(dir):
		if not xmlFile.endswith('.xml'):
			continue
		jsonFile = xmlFile.replace('.xml', '.json')
		addSingleNote(xmlFile, jsonFile, notebookId)

if __name__ == '__main__':
	if len(sys.argv) != 6:
		print('args: <url> <email> <password> <dir> <notebookName>')
		exit(1)
	url = sys.argv[1]
	email = sys.argv[2]
	password = sys.argv[3]
	dir = sys.argv[4]
	notebook = sys.argv[5]

	leanote = Leanote(url)
	leanote.login(email, password)

	# find notebook id
	notebookId = None
	notebooks = leanote.getNotebooks()
	for book in notebooks:
		if book['Title'].encode('utf-8') == notebook:
			notebookId = book['NotebookId']
			break
	if notebookId is None:
		print('notebook not found')
		exit(1)
	addFolder(dir, notebookId)
