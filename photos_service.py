from general_service import GeneralService

class PhotoService(GeneralService):
    def __init__(self, app_type, secret_file):
        super().__init__(app_type, secret_file,'photoslibrary','v1', ['https://www.googleapis.com/auth/photoslibrary', 'https://www.googleapis.com/auth/photoslibrary.sharing'])
        
    def get_user_albums(self) -> list:
        response = self.communicate.albums().list(pageSize=50, excludeNonAppCreatedData=False).execute()
        next_page_token = response.get("nextPageToken")
        albums = response.get("albums")
        while next_page_token:
            circular_response = self.communicate.albums().list(pageSize=50, excludeNonAppCreatedData=False, pageToken=next_page_token).execute()
            whiled_album = circular_response.get("albums")
            next_page_token = circular_response.get("nextPageToken")
            if whiled_album:
                albums.append(whiled_album)
        return albums

    def get_album_info(self, album_id) -> dict:
        return self.communicate.albums().get(albumId=album_id).execute()