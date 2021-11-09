from logger import Logger
from google_service_creation import create_service
import pickle
from google.auth.transport.requests import Request

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
