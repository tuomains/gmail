from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import emailSender
import Action
import re
import sys
import time

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
    to_email_address = ""
    sender = emailSender.EmailSender()
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = results.get('messages', [])
    

    if not messages:
        time.sleep(10)
    else:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            #print(msg['snippet'])
            if "Googleta" in msg['snippet']:
                print("Message with Googleta in snippet found")
                search = msg['snippet'].replace("Google","")
                for h in msg['payload']['headers']:
                    if h['name'] == "From":
                        to_email_address = re.search(r"(?<=<).*?(?=>)", h['value']).group(0)
                        break
                a = Action.Action()
                response = a.make_google_search(search)
                if "img" in msg['snippet']:
                    s = sender.CreateMessageWithAttachment("jaakko.botti@gmail.com",to_email_address,"testi",response,file_dir="",filename="screenshot.jpg")
                    print(s)
                else:
                    s = sender.CreateMessage("jaakko.botti@gmail.com",to_email_address,"testi",response)
                sender.SendMessage(service,'me',s)
                sender.DeleteMessage(service,'me',msg_id=message['id'])
    return len(messages)

if __name__ == '__main__':
    while True:
        count = main()
        print("Messages in inbox "+str(count), flush=True)