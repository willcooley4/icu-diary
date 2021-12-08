import firebase_admin
from firebase import Firebase
from firebase_admin import credentials
from firebase_admin import storage as s
import datetime


# Import UUID4 to create token
from uuid import uuid4

cred = credentials.Certificate("icu-diary-firebase-adminsdk-etde8-244db35487.json")

config = {
  'apiKey': "AIzaSyAa83ZWl-i_3pWpsMncl9G1553oXSuPD0s",
  'authDomain': "icu-diary.firebaseapp.com",
  'projectId': "icu-diary",
  'storageBucket': "icu-diary.appspot.com",
  'messagingSenderId': "353609023120",
  'appId': "1:353609023120:web:8556c4b6583b6a6a6fa215",
  'measurementId': "G-Z3SGGCH5QY",
  'databaseURL': ''
}

default_app = firebase_admin.initialize_app(cred, config)

bucket = s.bucket()
blob = bucket.blob('dagny.jpg')

# Create new token
new_token = uuid4()

# Create new dictionary with the metadata
metadata  = {"firebaseStorageDownloadTokens": new_token}

# Set metadata to blob
blob.metadata = metadata

# Upload file
# blob.upload_from_filename(filename='dagny.jpg', content_type='image/jpg')
# blob.download_from_filename(filename='dagny.jpg', content_type='image/jpg')
# storage = Firebase(config).storage()
# storage.child("images/dagny.jpg").download("dagny.jpg")
# print(storage.child("dagny.jpg").get_url(new_token))

print(blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'))