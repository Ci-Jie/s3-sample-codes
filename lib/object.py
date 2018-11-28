# -*- coding: utf-8 -*-

from connection import resource, client

def delete(bucket_name, key_name):
	try:
		client().delete_object(
			Bucket = bucket_name,
			Key = key_name
		)
		return 'success'
	except:
		return 'failed'

def download(bucket_name, key_name, object_name):
	try:
		resource().meta.client.download_file(bucket_name, key_name, object_name)
		return 'success'
	except:
		return 'failed'

def get(bucket_name, object_name):
	try:
		return client().get_object(
			Bucket = bucket_name,
			Key = object_name
		)
	except:
		return 'failed'

def list(bucket_name):
	try:
		return client().list_objects(
			Bucket = bucket_name
		)
	except:
		return 'failed'

def upload(bucket_name, object_name, key_name):
	try:
		resource().meta.client.upload_file(object_name, bucket_name, key_name)
		return 'success'
	except:
		return 'failed'