import pathlib
from google_exceptions import UnknownFileType
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
from general_service import GeneralService
import json

class DriveService(GeneralService):
    def __init__(self, app_type, secret_file, user_mail):
        super().__init__(app_type, secret_file, 'drive', 'v3', user_mail, ["https://www.googleapis.com/auth/drive"])

    def get_mimetype(self, file_name: str) -> str:
        """
        returns a MIME type of the file
        """
        suffix = file_name.split(".")[1]
        with open("mimetypes.json","r") as f:
            mimetypes = json.load(f)
            try:
                return mimetypes[suffix]
            except ValueError:
                self.log.log_message(f'{file_name} is unsupported file type')
                raise UnknownFileType

    def search_in_folder(self, id: str) -> dict:
        """
        returns info about all files in folder as a list of dicts, where one dict includes: ID (as 'id' key), name and MIME type (key 'mimeType')
        """
        query = f"parents = '{id}'"
        response = self.communicate.files().list(q=query).execute()
        files = response.get('files')
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = self.communicate.files().list(
                q=query, pageToken=nextPageToken).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')
        return files

    def upload(self, what: str, where: str, to: str) -> None:
        """
        Uploads a file with name  "what" and path of "where", placing ingo Google's folder of ID "to".
        """

        mime_type = self.get_mimetype(what)
        file_metadata = {"name": what, "parents": [to]}
        media = MediaFileUpload(str(where), mimetype=mime_type)
        file = self.communicate.files().create(
            body=file_metadata, media_body=media, fields="id").execute()
        self.log.log_message(f"file {what} successfully uploaded")

    def download(self, what_id: str, what_name: str, where: str) -> None:
        """
        Downloads file selected by ID and stores it in a file with "what_name" name and in "where" folder
        """

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
            self.log.log_message(f"file {what_name} successfully downloaded")

    def delete(self, file_id: str) -> None:
        """
        Removes file with ID put into the function from Google Drive completely
        No trash recovery available!
        Be sure this function is somehow secured in your implementation as you have no chance to recover the file
        TODO: add "are you sure?" dialog
        """
        self.communicate.files().delete(fileId=file_id).execute()
        self.log.log_message(f"file ID {file_id} successfully deleted")
