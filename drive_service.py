import pathlib
from google_exceptions import UnknownFileType
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
from general_service import GeneralService
import json

class DriveService(GeneralService):
    def __init__(self, app_type, secret_file, user_mail):
        super().__init__(app_type, secret_file, 'drive', 'v3', user_mail, ["https://www.googleapis.com/auth/drive", 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.metadata'])

    def get_mimetype(self, file_name: str) -> str:
        """Returns MIME type of selected file.

        Args:
            file_name (str): name of selected file

        Raises:
            UnknownFileType: Type of selected file is unknown

        Returns:
            str: MIME type of selected file
        """
        suffix = file_name.split(".")[1]
        with open("mimetypes.json","r") as f:
            mimetypes = json.load(f)
            try:
                return mimetypes[suffix]
            except ValueError:
                self.log.log_message(f'{file_name} is unsupported file type')
                raise UnknownFileType

    def search_in_folder(self, id: str, teamdrive_id: str = None) -> dict:
        """Lists all files in selected folder.

        Args:
            id (str): ID of folder to list all files from
            teamdrive_id (str, optional): In case the folder is on a shared/team drive, ID of such a drive needs to be provided. Defaults to None.

        Returns:
            list: All files and/or folders of selected folder. Each element of this list contains ID, MIME type and name of such element.
        """
        query = f"parents = '{id}'"
        kw_args = {
            "q":query
        }
        if teamdrive_id:
            kw_args["includeItemsFromAllDrives"] = True
            kw_args["supportsAllDrives"] = True
            kw_args["corpora"] = "drive"
            kw_args["driveId"] = teamdrive_id 
        response = self.communicate.files().list(**kw_args).execute()
        files = response.get('files')
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            kw_args["pageToken"] = nextPageToken
            response = self.communicate.files().list(**kw_args).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')
        return files

    def upload(self, what: str, where: str, to: str) -> None:
        """Uploads file to selected Google Drive folder

        Args:
            what (str): Name of selected file
            where (str): Path to selected file
            to (str): ID of selected folder
        """

        mime_type = self.get_mimetype(what)
        file_metadata = {"name": what, "parents": [to]}
        media = MediaFileUpload(str(where), mimetype=mime_type)
        file = self.communicate.files().create(
            body=file_metadata, media_body=media, fields="id").execute()
        self.log.log_message(f"file {what} successfully uploaded")

    def download(self, what_id: str, what_name: str, where: str) -> None:
        """Downloads selected file

        Args:
            what_id (str): ID of selected file
            what_name (str): Name of selected file (can be different from the name that the file is named on Google Drive; that's how it would be named on local drive)
            where (str): Path to folder, where would be the selected file stored. 
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
        """Deletes file. WARNING! There is no chance to recover. TODO: Add confirmation dialogue and optional argument for automatic deletion

        Args:
            file_id (str): ID of file selected for deletion
        """
        
        self.communicate.files().delete(fileId=file_id).execute()
        self.log.log_message(f"file ID {file_id} successfully deleted")
        
    def create_folder(self, name: str, parent: str) -> str:
        """Creates folder.

        Args:
            name (str): Name of created folder
            parent (str): ID of parent folder. If you want to create a folder in user root directory, pass "" in this argument

        Returns:
            str: ID of created folder
        """
        
        parent_list = []
        metadata = {
            'name': name,
            'mimeType':'application/vnd.google-apps.folder'
        }
        
        if parent != "": metadata["parents"] = []; metadata["parents"].append(parent)
        done = self.communicate.files().create(supportsAllDrives=True, body=metadata).execute()
        return done["id"]
