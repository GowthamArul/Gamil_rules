import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://mail.google.com/']
our_email = 'your_Gmail_id@gmail.com'


def _gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def mark_as_read(message_id):
    service = _gmail_authenticate()
    return service.users().messages().batchModify(
      userId='me',
      body={
          'ids': [message_id],
          'removeLabelIds': ['UNREAD']
      }
    ).execute()

def mark_as_unread(message_id):
    service = _gmail_authenticate()
    return service.users().messages().batchModify(
        userId='me',
        body={
            'ids': [message_id],
            'addLabelIds': ['UNREAD']
        }
    ).execute()

def get_mail_ids():
    service = _gmail_authenticate()
    unread_msgs = service.users().messages().list(userId='me').execute()
    messages = unread_msgs.get('messages')
    return messages
    
def move_trash(msg):
    service = _gmail_authenticate()
    return service.users().messages().trash(userId='me', id=msg).execute()

def get_label(label):
    service = _gmail_authenticate()
    payload =  service.users().labels().list(userId='me').execute()
    item_id = [i for i in payload['labels'] if i['name'] == label]
    return item_id[0]

def move_to(msg, label):
    service = _gmail_authenticate()
    label_body = {'removeLabelIds': ['IMPORTANT', 'CATEGORY_UPDATES', 'INBOX'],
                  'addLabelIds': [label]}
    return service.users().messages().modify(userId='me', id=msg, body=label_body ).execute()
