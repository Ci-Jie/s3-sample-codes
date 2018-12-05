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
	print admin.get_usage('admin')
	# print admin.get_usage('user')
	# print admin.enable_user('user2')
	# print admin.disable_user('user2')
	# print admin.set_max_buckets('user2', 500)
	# print admin.enable_user_quota('user1')
	# print admin.disable_user_quota('user1')
	# print admin.set_user_max_size('user1', 1000)
	# print admin.set_user_max_objects('user1', 100)
	# print admin.get_user_quota('user')
	# print admin.enable_bucket_quota('user1')
	# print admin.disable_bucket_quota('user1')
	# print admin.set_bucket_max_size('user1', 1200)
	# print admin.set_bucket_max_objects('user1', 12)
	# print admin.get_bucket_quota('user1')
	# print admin.get_usage('user1')
	# print admin.get_user('user2')
	# print admin.create_user('user1', 'user1@asus.com')
	# admin.create_user('test', 'test', 'test@asus.com')

	# s3_admin = AdminService(
	# 	os.getenv("ADMIN_ACCESS_KEY"),
	# 	os.getenv("ADMIN_SECRET_KEY")
	# )
	# print s3_admin
	# admin_bucket = BucketService(
	# 	os.getenv("HOST_IP"),
	# 	os.getenv("ADMIN_ACCESS_KEY"),
	# 	os.getenv("ADMIN_SECRET_KEY")
	# )
	# admin_bucket = BucketService(
	# 	'http://{}:{}'.format(os.getenv("HOST"), os.getenv("PORT")),
	# 	os.getenv("ADMIN_ACCESS_KEY"),
	# 	os.getenv("ADMIN_SECRET_KEY")
	# )
	# admin_object = ObjectService(
	# 	os.getenv("HOST_IP"),
	# 	os.getenv("ADMIN_ACCESS_KEY"),
	# 	os.getenv("ADMIN_SECRET_KEY")
	# )
	# print admin_bucket.create('Bucket4')
	# print admin_bucket.delete('Bucket4')
	# print admin_bucket.list()
	# print admin_bucket.add_acl('admin', 'FULL_CONTROL', 'Bucket1')
	# print admin_bucket.set_acl('user2', 'FULL_CONTROL', 'Bucket1')
	# print admin_bucket.get_acl('Bucket1')
	# print admin_object.upload('Bucket1', 'tmp/image.png', 'abc.png')
	# print admin_object.get('Bucket1', 'aa.png')
	# print admin_object.list_all('Bucket1')
	# print admin_object.list_spec_marker('Bucket1', 'test')
	# print admin_object.list_spec_count('Bucket1', 3)
	# print admin_object.list_spec_prefix('Bucket1', 't')
	# print admin_object.add_acl('user2', 'FULL_CONTROL', 'Bucket1', 'abc.png')
	# print admin_object.set_acl('user2', 'FULL_CONTROL', 'Bucket1', 'abc.png')
	# print admin_object.get_acl('Bucket1', 'abc.png')
	# print admin_object.download('Bucket1', 'abc.png', 'tmp/downloadfile.png')
	# print admin_object.delete('Bucket1', 'abc.png')


if __name__ == "__main__":
    main()