from django.http import HttpResponse
from django.http import JsonResponse
from sklearn import svm
import signValidation.sign_valid as sign
import joblib
import os
import numpy as np
import signValidation.gcs as gcs
from google.cloud import storage
#import signValidation.pdfwrite
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

import os


def data(request):

    path = request.path
    scheme = request.scheme
    imageURL = request.GET.get('imageUrl')
    method = request.method
    address = request.META['REMOTE_ADDR']
    user_agent = request.META['HTTP_USER_AGENT']

    #imageURL = imageURL.decode()
    print("\nimage URL is : ",imageURL)

    # check whther url is correct or not
    val = URLValidator()
    try:
        val(imageURL)
    except ValidationError:
        msg = 'Invalid URL : check again'
        #return HttpResponse(msg, content_type='text/html', charset='utf-8')
        return JsonRespone(msg)

    body = imageURL.split('/')

    fileName = body[len(body)-1]
    userName = body[len(body)-2]
    bucketName = body[len(body)-3]

    msg = f'''
<html>
path: {path}<br>
imageURL = {imageURL}<br>
imageName: {fileName}<br>
userName: {userName}<br>
bucketName: {bucketName}<br>
method: {method}<br>
</html>
'''

    gcloud = gcs.GCS()
    # providing the path of authentication file
    authFile = os.path.join('./signValidation/','gcloudKey.json')
    # authenticating
    gcloud.authentication(authFile)

    storage_client = storage.Client()

    # providing the path for the image to be downladed
    imgDownloadPath = os.path.join('./signValidation/GCPDownload/',fileName)
    # downlaoding the image from google cloud
    gcloud.download_blob(bucketName, userName+"/"+fileName, imgDownloadPath)

    '''
	# Get the pdf name to be downloaded
	pdfDownloadPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'aof.pdf')
	gcloud.download_blob(buckets[0].name, 'abc/aof.pdf', pdfDownloadPath)
	'''

    # classifying the downloaded image
    image = sign.Sign_Valid('./signValidation/GCPDownload/')
    features = image.process()
    features = np.array(features)
    clf = joblib.load('./signValidation/SignClassifierSVM.pkl')
    clf_prediction = clf.predict(features)

    if clf_prediction[0] == 0:
        imageValid = 'YES'
    else :
        imageValid = 'NO'

    data = {
'image_URL':imageURL,
'image_Name':fileName,
'user_ID':userName,
'bucket_Name':bucketName,
'imageValid':imageValid
}

    '''
	# Upload the aof to cloud
	gcloud.upload_blob(buckets[0].name, pdfDownloadPath, 'abc/testfolderdownload55.png' )
	'''

    #return HttpResponse(msg, content_type='text/html', charset='utf-8')
    return JsonResponse(data)