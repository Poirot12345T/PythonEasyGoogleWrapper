import pathlib
from logger import Logger
from google_service_creation import create_service
from google_exceptions import UnknownFileType
import pickle
from time import sleep
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.http import MediaIoBaseDownload

class GeneralService:
    def __init__(self, app_type, client_secret_file, api_name, api_version, *scopes):    
        self.log = Logger(app_type, f'{api_name} service init')
        broken_scopes = [scope for scope in scopes[0]]
        self.communicate = create_service(client_secret_file, api_name, api_version, broken_scopes)
        self.log.log_message('service created sucessfully')
        self.pickle_file = f'token_{api_name}_{api_version}.pickle'
        with open(self.pickle_file, 'rb') as pickle_content:
            cred = pickle.load(pickle_content)
            self.cred_expiry = cred.expiry
            self.cred = cred
            
    def refresh(self):
        self.cred.refresh(Request())
        with open(self.pickle_file, 'wb') as token:
            pickle.dump(self.cred, token)
        self.cred_expiry = self.cred.expiry

        
class DriveService(GeneralService):
    def __init__(self, app_type, secret_file):
        super().__init__(app_type, secret_file, 'drive', 'v3', ["https://www.googleapis.com/auth/drive"])
        
    def get_mimetype(self, file_name):
        """
        returns a MIME type of the file
        """
        suffix = file_name.split('.')[1].lower()
        if suffix == "mov":
            return "video/quicktime"
        elif suffix == "jpg":
            return "image/jpeg"
        elif suffix == "txt":
            return "text/plain"
        else:
            self.log.log_message(f'{file_name} is unsupported file type')
            raise UnknownFileType
    
    def search_in_folder(self, id):
        """
        returns info about all files in folder as a list of dicts, where one dict includes: ID (as 'id' key), name and MIME type (key 'mimeType')
        """
        query = f"parents = '{id}'"
        response = self.communicate.files().list(q=query).execute()
        files = response.get('files')
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = self.communicate.files.list(q=query, pageToken=nextPageToken).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')
        return files

    def upload(self, what, where, to): 
        mime_type = self.get_mimetype(what)
        file_metadata = {"name": what,"parents":[to]}
        media = MediaFileUpload(str(where), mimetype=mime_type)
        file = self.communicate.files().create(body=file_metadata,media_body=media,fields="id").execute()
    
    def download(self, what_id, what_name, where):
        request = self.communicate.files().get_media(fileId=what_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print("Download progress {0}".format(status.progress() * 100))

        fh.seek(0)

        with open(pathlib.Path(where, what_name), "wb") as f:
            f.write(fh.read())
            f.close()
    
    def delete(self, file_id):
        self.communicate.files().delete(fileId=file_id).execute()
