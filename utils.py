from py2neo import neo4j
import os
try:
     from urlparse import urlparse
except ImportError:
     from urllib.parse import urljoin


def getGraph():
     #print(neo4j, neo4j.__file__)
     #return neo4j.GraphDatabaseService("http://localhost:7474/db/data")
     #return neo4j.GraphDatabaseService("http://app55594714-V1ivYS:QZgiH1f3jWNWOC2yUYZK@hobby-kjjhomhijildgbkehfaomgol.dbs.graphenedb.com:24789")

     if os.environ.get('GRAPHENEDB_URL'):
          try:
               graph_db_url = urlparse(os.environ.get('GRAPHENEDB_URL'))
          except ImportError:
               graph_db_url = urljoin(os.environ.get('GRAPHENEDB_URL'))
          graph_db = neo4j.GraphDatabaseService(
               'http://{host}:{port}{path}'.format(
                    host=graph_db_url.hostname,
                    port=graph_db_url.port,
                    path=graph_db_url.path
               ), graph_db_url.username, graph_db_url.password)
     else:
          graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data')
     return graph_db