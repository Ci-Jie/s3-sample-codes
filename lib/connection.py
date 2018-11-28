import boto3, os
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

def client():
	client = boto3.client(
		's3',
		aws_access_key_id = os.getenv("ACCESS_KEY"),
		aws_secret_access_key = os.getenv("SECRET_KEY"),
		endpoint_url = os.getenv("HOST_IP"),
	)
	return client

def resource():
	resource = boto3.resource(
		's3',
		aws_access_key_id = os.getenv("ACCESS_KEY"),
		aws_secret_access_key = os.getenv("SECRET_KEY"),
		endpoint_url = os.getenv("HOST_IP"),
	)
	return resource