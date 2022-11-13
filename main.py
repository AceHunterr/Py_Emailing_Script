import base64
from email.mime.text import MIMEText

from email.encoders import encode_7or8bit
import httplib2
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret_21065374534-alivqjauc9ffabg6btuo02m7u4t0g7nd.apps.googleusercontent.com.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

# Start the OAuth flow to retrieve credentials
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
credentials = STORAGE.get()
if credentials is None or credentials.invalid:
  credentials = run_flow(flow, STORAGE, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
gmail_service = build('gmail', 'v1', http=http)

# create a message to send
message = MIMEText("Body of the email!!")
message['to'] = "21BMA003@nith.ac.in"
message['from'] = "aggarwalmehul26@gmail.com"
message['subject'] = "Automated Email by Python"

s = message.as_string()
b = base64.urlsafe_b64encode(s.encode('utf-8'))
body= {'raw': b.decode('utf-8')}

print(body)

# send it
try:
  message = (gmail_service.users().messages().send(userId="me", body=body).execute())
  print('Message Id: %s' % message['id'])
  print(message)
except Exception as error:
  print('An error occurred: %s' % error)


# import os
# print(os.environ.get('client_secret'))
# print(os.environ.get('client_id'))
# print(os.environ.get('access_token'))