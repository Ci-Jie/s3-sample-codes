# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
from os.path import join, dirname
from lib.BucketService import BucketService
from lib.ObjectService import ObjectService
from lib.AdminService import AdminService

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def main():
	admin = AdminService()
	admin.get_usage('admin')
	print(admin.get_usage('admin'))
	admin_bucket = BucketService(
		'http://{}:{}'.format(os.getenv("HOST"), os.getenv("PORT")),
		os.getenv("ADMIN_ACCESS_KEY"),
		os.getenv("ADMIN_SECRET_KEY")
	)
	admin_object = ObjectService(
		'http://{}:{}'.format(os.getenv("HOST"), os.getenv("PORT")),
		os.getenv("ADMIN_ACCESS_KEY"),
		os.getenv("ADMIN_SECRET_KEY")
	)
	# print admin_object.delete('Bucket', '12345.png')
	# print admin_object.download('Bucket', '12345.png', 'tmp/download.png')
	# print admin_bucket.create('Bucket2')
	print admin_bucket.list()
	# print admin_bucket.delete('Bucket1')
	# print admin_object.delete('Bucket1', 'test123')
	# print admin_object.put_object('Bucket', '1234')
	# print admin_object.upload_fileobj('Bucket1', 'test123','tmp/image.png')
	# print admin_object.list_all('Bucket1')
	# print admin_object.get('Bucket1', 'test123')
	# print admin.get_usage2()


if __name__ == "__main__":
    main()
