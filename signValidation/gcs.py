# first set the path of the authentication key file
# run the following command from cmd prompt (where path is full path of authetication file)
# set GOOGLE_APPLICATION_CREDENTIALS=[PATH]

from google.cloud import storage
import os


class GCS:


	# Downloads a blob from the bucket.
	def download_blob(self, bucket_name, source_blob_name, destination_file_name):
		storage_client = storage.Client()
		bucket = storage_client.get_bucket(bucket_name)
		blob = bucket.blob(source_blob_name)

		blob.download_to_filename(destination_file_name)

		print('\n\nBlob {} downloaded to {}.'.format(source_blob_name, destination_file_name))


	# Uploads a file to the bucket.
	def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
	    storage_client = storage.Client()
	    bucket = storage_client.get_bucket(bucket_name)
	    blob = bucket.blob(destination_blob_name)

	    blob.upload_from_filename(source_file_name)

	    print('\n\nFile {} uploaded to {}.\n\n'.format(source_file_name, destination_blob_name))


	# Authentication: Explicitly use service account credentials by specifying the private key file.
	def authentication(self, keyFile):
		storage_client = storage.Client().from_service_account_json(keyFile)
		#print("\nauthenticated\n")

'''

gcloud = GCS()
gcloud.authentication('gcloudKey.json')

storage_client = storage.Client()
#Make an authenticated API request
buckets = list(storage_client.list_buckets())
#print(buckets)

# get the image name to be downloaded
imgDownloadPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'testfolderdownload.png')
gcloud.download_blob(buckets[0].name, 'abc/abctest1.png', imgDownloadPath)

# get the image name to be uploaded
imgUploadPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'testfolderdownload.png')
gcloud.upload_blob(buckets[0].name, imgUploadPath, 'abc/testfolderdownload55.png' )

'''
