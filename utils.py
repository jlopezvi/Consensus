from py2neo import neo4j
import os
from urllib.parse import urlparse


def getGraph():
     #print(neo4j, neo4j._file_)
     return neo4j.GraphDatabaseService("http://localhost:7474/db/data")
     #return neo4j.GraphDatabaseService("http://app55594714-V1ivYS:QZgiH1f3jWNWOC2yUYZK@hobby-kjjhomhijildgbkehfaomgol.dbs.graphenedb.com:24789")
     #print(neo4j, neo4j.__file__)
     #return neo4j.GraphDatabaseService("http://localhost:7474/db/data")
     #return neo4j.GraphDatabaseService("http://app55594714-V1ivYS:QZgiH1f3jWNWOC2yUYZK@hobby-kjjhomhijildgbkehfaomgol.dbs.graphenedb.com:24789")

     if os.environ.get('GRAPHENEDB_URL'):
         graph_db_url = urlparse(os.environ.get('GRAPHENEDB_URL'))
         neo4j.authenticate("{host}:{port}".format(host=graph_db_url.hostname, port=graph_db_url.port), graph_db_url.username, graph_db_url.password)

         graph_db = neo4j.GraphDatabaseService('http://{host}:{port}/db/data'.format(host=graph_db_url.hostname, port=graph_db_url.port))
     else:
         graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data')
     return graph_db
