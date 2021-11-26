from general_service import GeneralService
from google_exceptions import BadInputType

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
    
    def create_album(self, name_album) -> dict:
        request = {
            "album":{"title":name_album}
        }
        return self.communicate.albums().create(body=request).execute()

    def share_album(self, album_id, collaboration=False, commentary=False) -> dict:
        request = {
            "sharedAlbumOptions":{
                "isCollaborative":collaboration,
                "isCommentable":commentary
            }
        }
        return self.communicate.albums().share(albumId=album_id, body=request).execute()
    
    def unshare_album(self, album_id):
        self.communicate.albums().unshare(albumId=album_id).execute()

    def get_media_info(self, media_id) -> dict:
        return self.communicate.mediaItems().get(mediaItemId=media_id).execute()

    def mass_get_media_info(self, media_ids) -> list:
        if not type(media_ids) == list:
            raise BadInputType("input type should be list")
        
        ret_val = []
        for id in media_ids:
            ret_val.append(self.get_media_info(id))
        return ret_val