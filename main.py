# -*- coding: utf-8 -*-

import lib.bucket as bucket
import lib.object as object

def main():
	# print bucket.create('Bucket')
	print bucket.list()
	# print bucket.delete('bucket')
	# print object.upload('Bucket', 'tmp/image.png', 'test5.png')
	# print object.get('Bucket', 'test.png')
	# print object.list('Bucket')
	# print object.download('Bucket', 'test.png', 'tmp/downloadfile.png')
	# print object.delete('Bucket', 'test1.png')

if __name__ == "__main__":
    main()