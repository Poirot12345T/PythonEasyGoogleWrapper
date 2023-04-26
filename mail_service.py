from general_service import GeneralService
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes

class MailService(GeneralService):
    def __init__(self, app_type, client_secret_file, user_mail):
        super().__init__(app_type, client_secret_file, 'gmail', 'v1', user_mail, ['https://mail.google.com/'])

    def compose_mail(self, to: str, subject: str, mail_body: str, attachments = None) -> None:
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        message.attach(MIMEText(mail_body, 'plain'))

        if attachments:
            for attach in attachments:
                cont_type, encoding = mimetypes.guess_type(attach)
                main_type, sub_type = cont_type.split('/', 1)
                filename = os.path.basename(attach)
                with open(attach, 'rb') as f:
                    attachf = MIMEBase(main_type, sub_type)
                    attachf.set_payload(f.read())
                    attachf.add_header('Content-Disposition','attachment',filename=filename)
                    encoders.encode_base64(attachf)
                    message.attach(attachf)
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        self.communicate.users().messages().send(
            userId='me',
            body={'raw':raw_message}
        ).execute()
        self.log.log_message(f'mail to {to} with subject {subject} successfully sent')
    