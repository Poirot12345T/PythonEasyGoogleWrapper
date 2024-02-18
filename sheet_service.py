from general_service import GeneralService

class SheetService(GeneralService):
    def __init__(self, app_type, secret_file, user_mail):
        super().__init__(app_type, secret_file, 'sheets', 'v4', user_mail, ['https://www.googleapis.com/auth/spreadsheets'])
        self.sheet = self.communicate.spreadsheets()

    def get_selected_data(self, spreadsheet_id: str, list_name: str, begin_cell: str, end_cell: str) -> list:
        """
        Returns 2D array from selected range of spreadsheet
        """
        range_def = f"{list_name}!{begin_cell}:{end_cell}"
        call_result = self.sheet.values().get(spreadsheetId=spreadsheet_id, range=range_def).execute()
        return call_result.get('values',[])
    
    def get_spreadsheet(self, spreadsheet_id: str, list_name: str) -> list:
        """
        Returns all data from spreadsheet
        """
        range_def = f"{list_name}"
        call_result = self.sheet.values().get(spreadsheetId=spreadsheet_id, range=range_def).execute()
        return call_result.get('values',[])
        
    def write_data(self, spreadsheet_id: str, sheet_name: str, start_cell: str, data: tuple, rowcol: str = "ROWS"):
        """Writes data to sheet.

        Args:
            spreadsheet_id (str): ID of specified spreadsheet to write into
            sheet_name (str): Name of list in spreadseet
            start_cell (str): left-up cell of written data.
            data (tuple): 2D tuple array of written data.
            rowcol (str, optional): Sets "major axis". If "ROWS" selected, data are written in the same "oreintation" as visualised in IDE. Setting "COLUMNS" makes transposition.  Defaults to "ROWS".
        """
        
        values = {
            'majorDimension': rowcol,
            'values':data
        }

        self.sheet.values().update(
            spreadsheetId=spreadsheet_id,
            valueInputOption="USER_ENTERED",
            range=f"{sheet_name}!{start_cell}",
            body=values
            ).execute()
