from logger import Logger
from google_service_creation import create_service
import pickle
from google.auth.transport.requests import Request

class GeneralService:
    def __init__(self, app_type, client_secret_file, api_name, api_version, user_mail, *scopes):
        self.log = Logger(app_type, f'{api_name} service init')
        mail_without_dot = user_mail.replace(".", "-")
        broken_scopes = [scope for scope in scopes[0]]
        self.pickle_file = f'token_{mail_without_dot}_{api_name}_{api_version}.pickle'
        self.communicate = create_service(client_secret_file, api_name, api_version, self.pickle_file, broken_scopes)
        self.log.log_message('service created sucessfully')
        with open(self.pickle_file, 'rb') as pickle_content:
            cred = pickle.load(pickle_content)
            self.cred_expiry = cred.expiry
            self.cred = cred

    def refresh(self):
        """
        Refreshes token (the token expiry time is around 3 hours)
        """
        self.cred.refresh(Request())
        with open(self.pickle_file, 'wb') as token:
            pickle.dump(self.cred, token)
        self.cred_expiry = self.cred.expiry
