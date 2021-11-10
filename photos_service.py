from general_service import GeneralService

class PhotoService(GeneralService):
    def __init__(self, app_type, secret_file):
        super().__init__(app_type, secret_file,'photoslibrary','v1', ['https://www.googleapis.com/auth/photoslibrary', 'https://www.googleapis.com/auth/photoslibrary.sharing'])
        