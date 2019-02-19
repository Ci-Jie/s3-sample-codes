# -*- coding: utf-8 -*-
import boto3


class BucketService:

	def __init__(self, host, access_key, secret_key):
		self._host = host
		self._access_key = access_key
		self._secret_key = secret_key

	def client(self):
		return boto3.client(
			's3',
			aws_access_key_id=self._access_key,
			aws_secret_access_key=self._secret_key,
			endpoint_url=self._host,
		)

	# example 1.1
	def create(self, name):
		if not self.exist(name):
			self.client().create_bucket(
				Bucket=name
			)
			return 'The bucket is created.'
		else:
			return 'The bucket already exists.'

	# example 1.2
	def delete(self, name):
		if self.exist(name):
			self.client().delete_bucket(
				Bucket=name
			)
			return 'The bucket is deleted.'
		else:
			return 'The bucket is not exist.'

	# example 1.3
	def list(self):
		res = self.client().list_buckets()
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

	# example 1.4
	def add_acl(self, user_name, permission, bucket_name):
		if not self._grant_exist(user_name, bucket_name):
			res = self.client().get_bucket_acl(
				Bucket=bucket_name
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
				self.client().put_bucket_acl(
					AccessControlPolicy={
						'Grants': res['Grants'],
						'Owner': {
							'DisplayName': res['Owner']['DisplayName'],
							'ID': res['Owner']['ID']
						}
					},
					Bucket=bucket_name,
				)
				return 'Add permission in bucket is successfully.'
			else:
				return 'An error occurred.'
		else:
			return 'An error occurred.'

	# example 1.5
	def set_acl(self, user_name, permission, bucket_name):
		if self._grant_exist(user_name, bucket_name):
			res = self.client().get_bucket_acl(
				Bucket=bucket_name
			)
			if res['ResponseMetadata']['HTTPStatusCode'] == 200:
				for grant in res['Grants']:
					if grant['Grantee']['DisplayName'] == user_name:
						grant['Permission'] = permission
						break
				self.client().put_bucket_acl(
					AccessControlPolicy={
						'Grants': res['Grants'],
						'Owner': {
							'DisplayName': res['Owner']['DisplayName'],
							'ID': res['Owner']['ID']
						}
					},
					Bucket=bucket_name,
				)
				return 'Set permission in bucket is successfully.'
			else:
				return 'An error occurred1.'
		else:
			return 'An error occurred2.'

	# example 1.6
	def get_acl(self, bucket_name):
		return self.client().get_bucket_acl(
			Bucket=bucket_name
		)

	# example 1.7
	def exist(self, name):
		res = self.client().list_buckets()
		if res['ResponseMetadata']['HTTPStatusCode'] == 200:
			for bucket in self.client().list_buckets()['Buckets']:
				if name == bucket['Name']:
					return True
			return False

	def _grant_exist(self, user_name, bucket_name):
		res = self.client().get_bucket_acl(
			Bucket=bucket_name
		)
		for grant in res['Grants']:
			if grant['Grantee']['DisplayName'] == user_name:
				return True
		return False