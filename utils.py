from py2neo import neo4j
import os


def getGraph():
     #return neo4j.GraphDatabaseService("http://localhost:7474/db/data")
     #return neo4j.GraphDatabaseService("http://app55594714-V1ivYS:QZgiH1f3jWNWOC2yUYZK@hobby-kjjhomhijildgbkehfaomgol.dbs.graphenedb.com:24789")

     if os.environ.get('GRAPHENEDB_URL'):
         from urllib.parse import urlparse
         graph_db_url = urlparse(os.environ.get('GRAPHENEDB_URL'))
         neo4j.authenticate("{host}:{port}".format(host=graph_db_url.hostname, port=graph_db_url.port), graph_db_url.username, graph_db_url.password)

         graph_db = neo4j.GraphDatabaseService('http://{host}:{port}/db/data'.format(host=graph_db_url.hostname, port=graph_db_url.port))
     else:
         graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data')
     return graph_db


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
