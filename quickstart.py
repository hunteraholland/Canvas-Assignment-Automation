from __future__ import print_function
import pickle
import os.path
import requests
import os
from bs4 import BeautifulSoup as bs
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks']


def main():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('tasks', 'v1', credentials=creds)

    # # Call the Tasks API
    # results = service.tasklists().list(maxResults=10).execute()
    # items = results.get('items', [])
    #
    # if not items:
    #     print('No task lists found.')
    # else:
    #     print('Task lists:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['title'], item['id']))

    # TODO:
    # Get Assignments for the week from Canvas API
    token = os.environ['CANVAS_TOKEN']
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get(
        'https://uc.instructure.com/api/v1/users/self/upcoming_events',
        headers=headers)
    src = r.content
    json_response = r.json()

    for j in json_response:
        base = 'https://tasks.googleapis.com/tasks/v1/lists/'
        acct = os.environ['ACCT_LIST']
        mgmt = os.environ['MGMT_LIST']
        web = os.environ['WEB_LIST']
        title = j['title']
        notes = j['description']
        due = j['due_at']
        course = j['context_name']

        if 'ACCT MGR DECISIONS' in course:
            requests.post(f'{base}{acct}/tasks')
        elif 'MANAGEMENT IN IT' in course:
            requests.post(f'{base}{mgmt}/tasks')
        elif 'WEB SERVER APPLICATION DEV' in course:
            requests.post(f'{base}{web}/tasks')


if __name__ == '__main__':
    main()
