#pip install --upgrade google-api-python-client


# from __future__ import print_function

from JumpScale import j

import httplib2
import os

from apiclient import discovery
from apiclient import errors
from apiclient import http

import oauth2client
from oauth2client import client
from oauth2client import tools

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

bitly = bitly_api.Connection(access_token="e04d9379d6fd844dd3cb391c0ad6a572c5b83437")

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

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
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def insert_permission(service, file_id, value, perm_type, role):
  """Insert a new permission.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to insert permission for.
    value: User or group e-mail address, domain name or None for 'default'
           type.
    perm_type: The value 'user', 'group', 'domain' or 'default'.
    role: The value 'owner', 'writer' or 'reader'.
  Returns:
    The inserted permission if successful, None otherwise.
  """
  new_permission = {
      'value': value,
      'type': perm_type,
      'role': role,
      'withLink' : True,
  }
  try:
    return service.permissions().insert(
        fileId=file_id, body=new_permission).execute()
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
  return None

def copy_file(service, origin_file_id, copy_title):
    """Copy an existing file.

    Args:
    service: Drive API service instance.
    origin_file_id: ID of the origin file to copy.
    copy_title: Title of the copy.

    Returns:
    The copied file if successful, None otherwise.

    https://developers.google.com/drive/v2/reference/files/copy#examples
    """
    copied_file = {'title': copy_title}
    try:
        return service.files().copy(fileId=origin_file_id, body=copied_file).execute()
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
    return None

def download_file(service, file_id, path):
    """Download a Drive file's content to the local filesystem.

    Args:
    service: Drive API Service instance.
    file_id: ID of the Drive file that will downloaded.
    """

    local_fd=open(path,"wb+")
    request = service.files().get_media(fileId=file_id)
    media_request = http.MediaIoBaseDownload(local_fd, request)

    while True:
        try:
            download_progress, done = media_request.next_chunk()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return
        if download_progress:
            print 'Download Progress: %d%%' % int(download_progress.progress() * 100)
        if done:
            print 'Download Complete'
            return

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)

    # results = service.files().list(maxResults=10).execute()
    # items = results.get('items', [])
    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print('{0} ({1})'.format(item['title'], item['id']))

    # file_id=item['id']
    # print item
    # # download_file(service, file_id, "test.xls")

    title="1_GIG Overview Use Case - Gener8 - Technology"
    q="title = \"1_GIG Overview Use Case - Gener8 - Technology\""

    results = service.files().list(maxResults=10,q=q).execute()


    file_id="10-52dT4UT_snZDuqi7-wsTZ1d3qTCWn524HAwliGSsQ"

    insert_permission(service, file_id, value=None, perm_type="anyone", role="reader")

    bitly.shorten('http://google.com/')

    

    from IPython import embed
    print ("DEBUG NOW 77")
    embed()
    
    

if __name__ == '__main__':
    main()