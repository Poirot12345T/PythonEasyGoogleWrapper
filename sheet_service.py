from general_service import GeneralService

class SheetService(GeneralService):
    def __init__(self, app_type, secret_file, user_mail):
        super().__init__(app_type, secret_file, 'sheets', 'v4', user_mail, ['https://www.googleapis.com/auth/spreadsheets'])
        self.sheet = self.communicate.spreadsheets()

    def get_spreadsheet_data(self, spreadsheet_id: str, list_name: str, begin_cell: str, end_cell: str) -> list:
        """
        Returns 2D array from selected range of spreadsheet
        """
        range_def = f"{list_name}!{begin_cell}:{end_cell}"
        call_result = self.sheet.values().get(spreadsheetId=spreadsheet_id, range=range_def).execute()
        return call_result.get('values',[])

        
