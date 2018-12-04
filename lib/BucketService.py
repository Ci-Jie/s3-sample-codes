# -*- coding: utf-8 -*-
import boto3

class BucketService:

	def __init__(self, host, access_key, secret_key):
		self.__host = host
		self.__access_key = access_key
		self.__secret_key = secret_key

	def request(self):
		return boto3.client(
			's3',
			aws_access_key_id = self.__access_key,
			aws_secret_access_key = self.__secret_key,
			endpoint_url = self.__host,
		)

	# example 1.1
	def create(self, name):
		try:
			if not self.exist(name):
				self.request().create_bucket(
					Bucket = name
				)
				return 'The bucket is created.'
			else:
				return 'The bucket already exists.'
		except:
			return 'An error occurred.'

	# example 1.2
	def delete(self, name):
		try:
			if self.exist(name):
				self.request().delete_bucket(
					Bucket = name
				)
				return 'The bucket is deleted.'
			else:
				return 'The bucket is not exist.'
		except:
			return 'An error occurred.'

	# example 1.3
	def list(self):
		# try:
			res = self.request().list_buckets()
			if res['ResponseMetadata']['HTTPStatusCode'] == 200:
				buckets = []
				for bucket in res['Buckets']:
					buckets.append({
						'name': bucket['Name'],
						'creationData': bucket['CreationDate'].__str__()
					})
				return buckets
			else:
				return 'An error occurred.'
		# except:
		# 	return 'An error occurred.'

	# example 1.4
	def add_acl(self, user_name, permission, bucket_name):
		try:
			if not self.__grant_exist(user_name, bucket_name):
				res = self.request().get_bucket_acl(
					Bucket = bucket_name
				)
				if res['ResponseMetadata']['HTTPStatusCode'] == 200:
					res['Grants'].append({
						'Grantee': {
							'DisplayName': user_name,
							'ID': user_name,
							'Type': 'CanonicalUser'
						},
						'Permission': permission
					})
					self.request().put_bucket_acl(
						AccessControlPolicy = {
							'Grants': res['Grants'],
							'Owner': {
								'DisplayName': res['Owner']['DisplayName'],
								'ID': res['Owner']['ID']
							}
						},
						Bucket = bucket_name,
					)
					return 'Add permission in bucket is successfully.'
				else:
					return 'An error occurred.'
			else:
				return 'An error occurred.'
		except:
			return 'An error occurred.'

	# example 1.5
	def set_acl(self, user_name, permission, bucket_name):
		try:
			if self.__grant_exist(user_name, bucket_name):
				res = self.request().get_bucket_acl(
					Bucket = bucket_name
				)
				if res['ResponseMetadata']['HTTPStatusCode'] == 200:
					for grant in res['Grants']:
						if grant['Grantee']['DisplayName'] == user_name:
							grant['Permission'] = permission
							break
					self.request().put_bucket_acl(
						AccessControlPolicy = {
							'Grants': res['Grants'],
							'Owner': {
								'DisplayName': res['Owner']['DisplayName'],
								'ID': res['Owner']['ID']
							}
						},
						Bucket = bucket_name,
					)
					return 'Set permission in bucket is successfully.'
				else:
					return 'An error occurred.'
			else:
				return 'An error occurred.'
		except:
			return 'An error occurred.'


	# example 1.6
	def get_acl(self, bucket_name):
		try:
			return self.request().get_bucket_acl(
				Bucket = bucket_name
			)
		except:
			return 'An error occurred.'

	# example 1.7
	def exist(self, name):
		try:
			res = self.request().list_buckets()
			if res['ResponseMetadata']['HTTPStatusCode'] == 200:
				for bucket in self.request().list_buckets()['Buckets']:
					if name == bucket['Name']:
						return True
				return False
		except:
			return 'An error occurred.'

	def __grant_exist(self, user_name, bucket_name):
		res = self.request().get_bucket_acl(
			Bucket = bucket_name
		)
		for grant in res['Grants']:
			if grant['Grantee']['DisplayName'] == user_name:
				return True
		return False
