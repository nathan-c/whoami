
from __future__ import print_function
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

try:
    import argparse
    FLAGS = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    FLAGS = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = __location__ + '/client_secret.json'
APPLICATION_NAME = 'whoami'


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
                                   'sheets.googleapis.whoami.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, FLAGS)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_credentials_server():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CLIENT_SECRET_FILE, scopes=SCOPES)
    return credentials


def append_row(spreadsheet_id, value_range_body, start_range='A1', value_input_option='RAW'):
    """
    BEFORE RUNNING:
    ---------------
    1. If not already done, enable the Google Sheets API
    and check the quota for your project at
    https://console.developers.google.com/apis/api/sheets
    2. Install the Python client library for Google APIs by running
    `pip install --upgrade google-api-python-client`

    Keyword arguments:
    spreadsheet_id -- The ID of the spreadsheet to update
    start_range -- The A1 notation of a range to search for a logical table of data.
                    Values will be appended after the last row of the table.
    value_input_option -- How the input data should be interpreted.
                    'INPUT_VALUE_OPTION_UNSPECIFIED', 'RAW', 'USER_ENTERED'
    value_range_body -- Data row to add (as Dict)
    """
    credentials = get_credentials_server()
    value = {'values': [value_range_body]}
    service = discovery.build('sheets', 'v4', credentials=credentials)

    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=start_range,
                                                     valueInputOption=value_input_option, insertDataOption='INSERT_ROWS', body=value)
    response = request.execute()
    return response
