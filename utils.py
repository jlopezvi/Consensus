from py2neo import neo4j
from flask import jsonify, url_for


def getGraph():
    if os.environ.get('GRAPHENEDB_URL'):
        from urllib.parse import urlparse
        graph_db_url = urlparse(os.environ.get('GRAPHENEDB_URL'))
        neo4j.authenticate("{host}:{port}".format(host=graph_db_url.hostname, port=graph_db_url.port), graph_db_url.username, graph_db_url.password)
        graph_db = neo4j.GraphDatabaseService('http://{host}:{port}/db/data'.format(host=graph_db_url.hostname, port=graph_db_url.port))
    else:
        # used by Nicol Ridente with local configuration
        # neo4j.authenticate('{host}:{port}.format(host='localhost', port='7474'), 'neo4j', '0000')
        graph_db = neo4j.GraphDatabaseService(‘http://localhost:7474/db/data')
    return graph_db


import os
basedir = os.path.abspath(os.path.dirname(__file__))
from werkzeug.utils import secure_filename


#Used By <_newParticipant> and 	<addIdeaToUser_aux> For Upload Files.
# for upload files
# NOTES: prepared only for one picture file extension. At the moment,'.png' is hardcoded.
def save_file(ruta_dest,file_upload,filename):
    path = basedir + ruta_dest
    file_upload.save(os.path.join(path, secure_filename(filename)))
    url = str(ruta_dest + secure_filename(filename))
    return url


# FLASK EMAIL
from flask.ext.mail import Message

def send_email(to, subject, template):
    from app import app,mail
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)



# # TODO: chose one mail method, PYTHON or Flask
# # PYTHON EMAIL
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from uuid_token import generate_confirmation_token, confirm_token
# from participantManager import _get_fullname_for_participant
#
# def send_email_new(email, opt, guest_email=None):
#     token = generate_confirmation_token(email)
#     message = MIMEMultipart()
#     if opt == 'regular':
#         print('entre a regular')
#         toEmail = email
#         confirm_url = url_for('.registration_receive_emailverification', token=token, _external=True)
#         msgSubject = "Please confirm your email"
#         msgBody = """
#                     Welcome! Thanks for signing up. Please follow this link to activate your account:
#                     <br/>
#                     <a href="{}">"{}"</a>
#                     <br/>/
#                     Cheers!
#                  """
#         message.attach(MIMEText(msgBody.format(confirm_url, confirm_url), 'html'))
#     elif opt == 'invitation':
#         toEmail = guest_email
#         confirm_url = url_for('.registration_from_invitation', token=token, guest_email=guest_email, _external=True)
#         msgSubject = ''.join([_get_fullname_for_participant(email), " invites you to join Consensus"])
#         msgBody = """
#                     Welcome! {} is inviting you to use our aplication
#                     <br/>
#                     Please, follow the next link to access to our site
#                     <br />
#                     <a href="{}">"{}"</a>
#                     <br/>/
#                     Cheers!
#                  """
#         message.attach(MIMEText(msgBody.format(_get_fullname_for_participant(email), confirm_url, confirm_url), 'html'))
#
#     fromEmail = 'noreply.consensus@gmail.com'
#     fromEmailPass = 'consensus2017'
#     message['From'] = fromEmail
#     message['To'] = toEmail
#     message['Subject'] = msgSubject
#     # Try email senging
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     try:
#         server.login(fromEmail, fromEmailPass)
#         server.sendmail(fromEmail, toEmail, message.as_string())
#         print('email sent')
#         return jsonify({"result": "OK", "result_msg": "email sent"})
#     except Exception as e:
#         email_error = e
#         print(e)
#         server.quit()
#     return jsonify({"result": "wrong", "result_msg": "email not sent", "error": email_error})
