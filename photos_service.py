from requests.api import request
from general_service import GeneralService
from google_exceptions import BadInputType
import requests
import pickle
import os

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
        """
        works like cycled get_media_info(), it may run over the API limit quicker
        """

        if type(media_ids) != list:
            raise BadInputType("input type of 'media_ids' should be list")
        
        ret_val = []
        for id in media_ids:
            ret_val.append(self.get_media_info(id))
        return ret_val

    def upload(self, where, name):
        token = pickle.load(open(self.pickle_file, 'rb'))
        upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
        header = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': 'application/octet-stream',
            'X-Goog-Upload-Protocol': 'raw',
            'X-Goog-Upload-File-Name':str(name)
        }
        img = open(where, 'rb').read()
        req_response = requests.post(upload_url, headers=header, data=img)

        request_body = {
            'newMediaItems':[
                {
                    'simpleMediaItem': {
                        'uploadToken': req_response.content.decode('utf8')

                    }
                }
            ]
        }

        response = self.communicate.mediaItems().batchCreate(body=request_body).execute()
        return response

    def add_to_album(self, media_ids, album_id):
        if type(media_ids) != list:
            if type(media_ids) == str:
                media_ids = [media_ids]
            else:    
                raise BadInputType("input type of 'media_ids' should be list or a string")
        request_body = {
            'mediaItemIds':media_ids
        }

        response = self.communicate.albums().batchAddMediaItems(
            albumId= album_id,
            body=request_body
        ).execute()
        return response

    def remove_from_album(self, media_ids, album_id):
        if type(media_ids) != list:
            if type(media_ids) == str:
                media_ids = [media_ids]
            else:    
                raise BadInputType("input type of 'media_ids' should be list or a string")
        request_body = {
            'mediaItemIds':media_ids
        }

        response = self.communicate.albums().batchRemoveMediaItems(
            albumId=album_id,
            body=request_body
        ).execute()
        return response

    def download_file(self, media_id, donwload_folder, file_name):
        url = self.get_media_info(media_id)["baseUrl"]
        resp = requests.get(url)
        self.log.log_message(f"downloading {file_name}")
        with open(os.path.join(donwload_folder, file_name), "wb") as f:
            f.write(resp.content)
