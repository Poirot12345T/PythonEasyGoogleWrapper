import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from google_exceptions import UnableToConnect
from google.auth.exceptions import RefreshError

def create_service(client_secret_file, api_name, api_version, scopes):

    cred = None

    pickle_file = f'token_{api_name}_{api_version}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)
    if not cred or not cred.valid:
        while True:
            if cred and cred.expired and cred.refresh_token:
                try:
                    cred.refresh(Request())
                    break
                except RefreshError:
                    os.remove(pickle_file)
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)
                break

    if api_name == 'photoslibrary':
        service = build(api_name, api_version, credentials=cred, static_discovery=False)
        return service
    else: 
        service = build(api_name, api_version, credentials=cred)
        