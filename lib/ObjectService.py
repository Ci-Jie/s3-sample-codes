import boto3


class ObjectService:

	def __init__(self, host, access_key, secret_key):
		self._host = host
		self._access_key = access_key
		self._secret_key = secret_key

	def resource(self):
		return boto3.resource(
			's3',
			aws_access_key_id=self._access_key,
			aws_secret_access_key=self._secret_key,
			endpoint_url=self._host,
		)

	def client(self):
		return boto3.client(
			's3',
			aws_access_key_id=self._access_key,
			aws_secret_access_key=self._secret_key,
			endpoint_url=self._host,
		)

	# example 2.1
	def upload(self, bucket_name, object_name, key_name):
		self.resource().meta.client.put_object(object_name, bucket_name, key_name)
		return 'The file is uploaded.'

	# example 2.2
	def get(self, bucket_name, object_name):
		res = self.client().get_object(
			Bucket=bucket_name,
			Key=object_name
		)
		if res['ResponseMetadata']['HTTPStatusCode'] == 200:
			return res
		else:
			return 'An error occurred.'

	# example 2.3
	def list_all(self, bucket_name):
		res = self.client().list_objects(
			Bucket=bucket_name
		)
		if res['ResponseMetadata']['HTTPStatusCode'] == 200:
			objects = []
			if 'Content' in res.keys():
				for object in res['Contents']:
					objects.append({
						'Key': object['Key'],
						'Owner': {
							'DisplayName': object['Owner']['DisplayName'],
							'ID': object['Owner']['ID']
						},
						'Size': object['Size']
					})
				return objects
		else:
			return 'An error occurred.'

	# example 2.4
	def list_spec_marker(self, bucket_name, marker):
		res = self.client().list_objects(
			Bucket=bucket_name,
			Marker=marker
		)
		if res['ResponseMetadata']['HTTPStatusCode'] == 200:
			objects = []
			for object in res['Contents']:
				objects.append({
					'Key': object['Key'],
					'Owner': {
						'DisplayName': object['Owner']['DisplayName'],
						'ID': object['Owner']['ID']
					},
					'Size': object['Size']
				})
			return objects
		else:
			return 'An error occurred.'

	# example 2.5
	def list_spec_count(self, bucket_name, count):
		res = self.client().list_objects(
			Bucket=bucket_name,
			MaxKeys=count
		)
		if res['ResponseMetadata']['HTTPStatusCode'] == 200:
			objects = []
			for object in res['Contents']:
				objects.append({
					'Key': object['Key'],
					'Owner': {
						'DisplayName': object['Owner']['DisplayName'],
						'ID': object['Owner']['ID']
					},
					'Size': object['Size']
				})
			return objects
		else:
			return 'An error occurred.'

	# example 2.6
	def list_spec_prefix(self, bucket_name, prefix):
		res = self.client().list_objects(
			Bucket=bucket_name,
			Prefix=prefix
		)
		if res['ResponseMetadata']['HTTPStatusCode'] == 200:
			objects = []
			for object in res['Contents']:
				objects.append({
					'Key': object['Key'],
					'Owner': {
						'DisplayName': object['Owner']['DisplayName'],
						'ID': object['Owner']['ID']
					},
					'Size': object['Size']
				})
			return objects
		else:
			return 'An error occurred.'

	# example 2.7
	def get_acl(self, bucket_name, key_name):
		res = self.client().get_object_acl(
			Bucket=bucket_name,
			Key=key_name
		)
		if res['ResponseMetadata']['HTTPStatusCode'] == 200:
			return res
		else:
			return 'An error occurred.'

	# example 2.8
	def add_acl(self, user_name, permission, bucket_name, key_name):
		if not self._grant_exist(user_name, bucket_name, key_name):
			res = self.client().get_object_acl(
				Bucket=bucket_name,
				Key=key_name
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
				self.client().put_object_acl(
					AccessControlPolicy={
						'Grants': res['Grants'],
						'Owner': {
							'DisplayName': res['Owner']['DisplayName'],
							'ID': res['Owner']['ID']
						}
					},
					Bucket=bucket_name,
					Key=key_name,
				)
				return 'Add permission in object is successfully.'
			else:
				return 'An error occurred.'
		else:
			return 'An error occurred.'

  # example 2.9
	def set_acl(self, user_name, permission, bucket_name, key_name):
		if self._grant_exist(user_name, bucket_name, key_name):
			res = self.client().get_object_acl(
				Bucket=bucket_name,
				Key=key_name
			)
			if res['ResponseMetadata']['HTTPStatusCode'] == 200:
				for grant in res['Grants']:
					if grant['Grantee']['DisplayName'] == user_name:
						grant['Permission'] = permission
						break
				self.client().put_object_acl(
					AccessControlPolicy={
						'Grants': res['Grants'],
						'Owner': {
							'DisplayName': res['Owner']['DisplayName'],
							'ID': res['Owner']['ID']
						}
					},
					Bucket=bucket_name,
					Key=key_name
				)
				return 'Set permission in object is successfully.'
			else:
				return 'An error occurred.'
		else:
			return 'An error occurred.'

	# example 2.10
	def download(self, bucket_name, key_name, object_name):
		self.client().download_fileobj(bucket_name, key_name, object_name)

	# example 2.11
	def delete(self, bucket_name, key_name):
		self.client().delete_object(
			Bucket=bucket_name,
			Key=key_name
		)
		return 'The file is deleted.'

	def _grant_exist(self, user_name, bucket_name, key_name):
		res = self.client().get_object_acl(
			Bucket=bucket_name,
			Key=key_name
		)
		for grant in res['Grants']:
			if grant['Grantee']['DisplayName'] == user_name:
				return True

	def put_object(self, bucket_name, key_name):
		return self.client().put_object(
			Bucket=bucket_name,
			Key=key_name,
			Metadata={
				'test': 'test'
			}
		)

	def upload_fileobj(self, bucket_name, key_name, object_name):
		self.resource().meta.client.upload_file(object_name, bucket_name, key_name)