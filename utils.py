from py2neo import neo4j


def getGraph():
     if os.environ.get('GRAPHENEDB_URL'):
         from urllib.parse import urlparse
         graph_db_url = urlparse(os.environ.get('GRAPHENEDB_URL'))
         neo4j.authenticate("{host}:{port}".format(host=graph_db_url.hostname, port=graph_db_url.port), graph_db_url.username, graph_db_url.password)

         graph_db = neo4j.GraphDatabaseService('http://{host}:{port}/db/data'.format(host=graph_db_url.hostname, port=graph_db_url.port))
     else:
         graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data')
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
    url = str(path + secure_filename(filename))
    return url


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
