# -*- coding: utf-8 -*-

from connection import client

def exist(name):
	for bucket in client().list_buckets()['Buckets']:
		if name == bucket['Name']:
			return True
	return False

def create(name):
	if exist(name):
		return 'failed'
	else:
		client().create_bucket(
			Bucket = name
		)
		return 'success'

def delete(name):
	try:
		client().delete_bucket(
			Bucket = name
		)
		return 'success'
	except:
		return 'failed'

def list():
	buckets = []
	try:
		for bucket in client().list_buckets()['Buckets']:
			buckets.append({
				'name': bucket['Name'],
				'creationData': bucket['CreationDate'].__str__()
			})
		return buckets
	except:
		return 'failed'