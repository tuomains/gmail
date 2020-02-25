"""Send an email message from the user's account.
"""

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
import logging
import datetime

from apiclient import errors


class EmailSender(): 
 FORMAT = '%(asctime)-15s [%(funcName)s] %(message)s'
 DATEFMT = '%Y-%m-%d %H:%M:%S'
 LOGFILENAME = datetime.datetime.now().strftime("%d_%m_%Y")

 logging.basicConfig(filename=LOGFILENAME+'.log',level=logging.DEBUG,filemode='w',format=FORMAT, datefmt=DATEFMT)
 logger = logging.getLogger(__name__)
 def SendMessage(self,service, user_id, message):
   """Send an email message.
 
   Args:
     service: Authorized Gmail API service instance.
     user_id: User's email address. The special value "me"
     can be used to indicate the authenticated user.
     message: Message to be sent.
 
   Returns:
     Sent Message.
   """
   try:
     message = (service.users().messages().send(userId=user_id, body=message)
                .execute())
     print('Message with id: %s sent successfully.' % message['id'])
     return message
   except errors.HttpError as error:
     print('An error occurred: %s' % error)
 
 
 def CreateMessage(self,sender, to, subject, message_text):
   """Create a message for an email.
 
   Args:
     sender: Email address of the sender.
     to: Email address of the receiver.
     subject: The subject of the email message.
     message_text: The text of the email message.
 
   Returns:
     An object containing a base64url encoded email object.
   """
   message = MIMEText(message_text,'html')
   message['to'] = to
   message['from'] = sender
   message['subject'] = subject
   raw = base64.urlsafe_b64encode(message.as_bytes())
   raw = raw.decode()
   body = {'raw': raw}
   return body
   #return {'raw': base64.urlsafe_b64encode(message.as_string())}
 
 
 def CreateMessageWithAttachment(self,sender, to, subject, message_text, file_dir,
                                 filename):
   """Create a message for an email.
 
   Args:
     sender: Email address of the sender.
     to: Email address of the receiver.
     subject: The subject of the email message.
     message_text: The text of the email message.
     file_dir: The directory containing the file to be attached.
     filename: The name of the file to be attached.
 
   Returns:
     An object containing a base64url encoded email object.
   """
   logging.debug("<<<")
   message = MIMEMultipart()
   message['to'] = to
   message['from'] = sender
   message['subject'] = subject
 
   msg = MIMEText(message_text)
   message.attach(msg)
 
   path = os.path.join(file_dir, filename)
   content_type, encoding = mimetypes.guess_type(path)

 
   if content_type is None or encoding is not None:
     content_type = 'application/octet-stream'
   main_type, sub_type = content_type.split('/', 1)
   if main_type == 'text':
     fp = open(path, 'rb')
     msg = MIMEText(fp.read(), _subtype=sub_type)
     fp.close()
   elif main_type == 'image':
     fp = open(path, 'rb')
     msg = MIMEImage(fp.read(), _subtype=sub_type)
     fp.close()
   elif main_type == 'audio':
     fp = open(path, 'rb')
     msg = MIMEAudio(fp.read(), _subtype=sub_type)
     fp.close()
   else:
     fp = open(path, 'rb')
     msg = MIMEBase(main_type, sub_type)
     msg.set_payload(fp.read())
     fp.close()
   msg.add_header('Content-Disposition', 'attachment', filename=filename)
   message.attach(msg)
 
   #return {'raw': message.as_string()}
   logging.debug(">>>")
   return msg.get_payload()

 def DeleteMessage(self,service, user_id, msg_id):
  """Delete a Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message to delete.
  """
  try:
    service.users().messages().delete(userId=user_id, id=msg_id).execute()
    print('Message with id: %s deleted successfully.' % msg_id)
  except errors.HttpError as error:
    print('An error occurred: %s' % error)