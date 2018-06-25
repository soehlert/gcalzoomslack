#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is to go to gcal, grab any meeting invites I have. Then,
it will parse out the zoom number and paste it into slack at
the time of the meeting
"""

__author__ = "Sam Oehlert"
__version__ = "0.1.0"

import datetime

from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.discovery import build

# Setup the calendar API
SCOPES = 'https://www.google.apis.com/auth/calendar.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the API
now = datetime.datetime.utcnow().isoformat() + 'Z'  # z is for utc time
print('Getting the upcoming 10 events')
events_results = service.events().list(calendarId='primary', timeMin=now,
                                       maxResults=10, singleEvents=True,
                                       orderBy='startTime').execute()

events = events_results.get('items', [])

if not events:
    print('No upcoming events')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])
