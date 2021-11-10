from general_service import GeneralService

class SheetService(GeneralService):
    def __init__(self, app_type, secret_file):
        super().__init__(app_type, secret_file, 'sheets', 'v4', ['https://www.googleapis.com/auth/spreadsheets'])