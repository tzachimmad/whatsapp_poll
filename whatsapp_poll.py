from __future__ import print_function
import httplib2
from whatsapp_parser import create_csv_file
import os

from apiclient import errors
from apiclient.http import MediaFileUpload
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

# drive file parameters
FILE_ID = '1GU5e-RFYRsYL1-YYL3ooMHE2VOHnz09oE8LZrmQa4I0'
FILE_LINK = 'https://docs.google.com/spreadsheets/d/1GU5e-RFYRsYL1-YYL3ooMHE2VOHnz09oE8LZrmQa4I0/edit?usp=sharing'
TITLE = 'Matomy Air'
MIME_TYPE = 'csv'
#upload file path
FILE_UPLOAD = 'output.csv'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

from apiclient import errors
from apiclient.http import MediaFileUpload

def csv_to_drive():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)   
    file = service.files().get(fileId=FILE_ID).execute()
    media_body = MediaFileUpload(FILE_UPLOAD, mimetype=MIME_TYPE, resumable=True)
    service.files().update(fileId=FILE_ID,body = {'title':[TITLE],'mime_type':MIME_TYPE},
        newRevision=1,
        media_body='output.csv').execute()

def main():
    create_csv_file()
    csv_to_drive()
    print("Link to file: "+FILE_LINK)

if __name__ == '__main__':
    main()