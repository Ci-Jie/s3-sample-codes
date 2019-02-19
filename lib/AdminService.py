import os, time, hmac, hashlib, base64, requests, json
from dotenv import load_dotenv
from os.path import join, dirname

os.environ['TZ'] = 'Europe/London'
time.tzset()

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)


class AdminService:

	def __init__(
		self,
		access_key=os.getenv("ADMIN_ACCESS_KEY"),
		secret_key=os.getenv("ADMIN_SECRET_KEY"),
		admin_entrypoint=os.getenv("ADMIN_ENTRYPOINT"),
		host=os.getenv("HOST"),
		port=os.getenv("PORT")
		):
		self._access_key = access_key
		self._secret_key = secret_key
		self._admin_entrypoint = admin_entrypoint
		self._host = host
		self._port = port

	def _request(self, method, path, query, data={}):
		url = 'http://{}:{}/{}/{}{}'.format(
			self._host,
			self._port,
			self._admin_entrypoint,
			path,
			query
		)
		date = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime())
		canonical = '{}\n\n\n{}\n/{}/{}'.format(
			method,
			date,
			self._admin_entrypoint,
			path
		)
		signature = base64.b64encode(hmac.new(self._secret_key.__str__(), canonical, hashlib.sha1).digest())
		headers = {
			'Host': self._host,
			'Date': date,
			'Authorization': 'AWS {}:{}'.format(self._access_key, signature)
		}
		if method == 'GET':
			res = requests.get(url, headers=headers)
		elif method == 'PUT':
			res = requests.put(url, headers=headers)
		elif method == 'POST':
			res = requests.post(url, headers=headers)
		elif method == 'DELETE':
			res = requests.delete(url, headers=headers)
		return res

	# example 3.1
	def get_user(self, username):
		res = self._request('GET', 'user', '?format=json&uid={}'.format(username))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.2
	def create_user(self, username, email=''):
		res = self._request('PUT', 'user', '?format=json&uid={}&display-name={}&email={}'.format(
			username,
			username,
			email
		))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.3
	def get_usage(self, username):
		size_kb_utilized = 0
		num_objects = 0
		res = self._request('GET', 'bucket', '?format=json&uid={}'.format(username))
		buckets = json.loads(res.content)
		for bucket in buckets:
			usage = self._request('GET', 'bucket', '?format=json&bucket={}'.format(bucket))
			if 'rgw.main' in json.loads(usage.content):
				size_kb_utilized += json.loads(usage.content)['usage']['rgw.main']['size_kb_utilized']
				num_objects += json.loads(usage.content)['usage']['rgw.main']['num_objects']
		return 'status code: {}\nmsg: {}'.format(res.status_code, {
			'size_kb_utilized': size_kb_utilized,
			'num_objects': num_objects
		})

	# example 3.4
	def get_user_quota(self, username):
		res = self._request(
			'GET', 'user', '?format=json&quota&uid={}&quota-type=user'.format(username))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.5
	def enable_user_quota(self, username):
		res = self._request('PUT', 'user', '?quota&uid={}&quota-type=user&enabled={}'.format(username, True))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.6
	def disable_user_quota(self, username):
		res = self._request('PUT', 'user', '?quota&uid={}&quota-type=user&enabled={}'.format(username, False))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.7
	def set_user_max_size(self, username, max_size_kb):
		res = self._request('PUT', 'user', '?quota&uid={}&quota-type=user&max-size-kb={}'.format(username, max_size_kb))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.8
	def set_user_max_objects(self, username, max_objects):
		res = self._request('PUT', 'user', '?quota&uid={}&quota-type=user&max-objects={}'.format(username, max_objects))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.9
	def get_bucket_quota(self, username):
		res = self._request('GET', 'user', '?quota&uid={}&quota-type=bucket'.format(username))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.10
	def enable_bucket_quota(self, username):
		res = self._request('PUT', 'user', '?quota&uid={}&quota-type=bucket&enabled={}'.format(username, True))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.11
	def disable_bucket_quota(self, username):
		res = self._request('PUT', 'user', '?quota&uid={}&quota-type=bucket&enabled={}'.format(username, False))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.12
	def set_bucket_max_size(self, username, max_size_kb):
		res = self._request('PUT', 'user', '?quota&uid={}&quota-type=bucket&max-size-kb={}'.format(username, max_size_kb))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.13
	def set_bucket_max_objects(self, username, max_objects):
		res = self._request('PUT', 'user', '?quota&uid={}&quota-type=bucket&max-objects={}'.format(username, max_objects))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.14
	def set_max_buckets(self, username, count):
		res = self._request('POST', 'user', '?format=json&uid={}&max-buckets={}'.format(username, count))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.15
	def enable_user(self, username):
		res = self._request('POST', 'user', '?format=json&uid={}&suspended={}'.format(username, 0))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.16
	def disable_user(self, username):
		res = self._request('POST', 'user', '?format=json&uid={}&suspended={}'.format(username, 1))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.17
	def add_bucket_read_permission(self, username):
		res = self._request(
			'PUT', 'user', '?caps&format=json&user-caps=buckets=read&uid={}'.format(username))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.18
	def add_bucket_write_permission(self, username):
		res = self._request(
			'PUT', 'user', '?caps&format=json&user-caps=buckets=write&uid={}'.format(username))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.19
	def remove_bucket_read_permission(self, username):
		res = self._request(
			'DELETE', 'user', '?caps&format=json&user-caps=buckets=read&uid={}'.format(username))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# example 3.20
	def remove_bucket_write_permission(self, username):
		res = self._request(
			'DELETE', 'user', '?caps&format=json&user-caps=buckets=write&uid={}'.format(username))
		return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)

	# def get_traffic(self, ):
	# 	res = self._request('GET', 'usage', '?format=json')
	# 	return 'status code: {}\nmsg: {}'.format(res.status_code, res.content)