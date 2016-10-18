from py2neo import neo4j
import os
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparseere


def getGraph():
     #print(neo4j, neo4j.__file__)
     #return neo4j.GraphDatabaseService("http://localhost:7474/db/data")
     #return neo4j.GraphDatabaseService("http://app55594714-V1ivYS:QZgiH1f3jWNWOC2yUYZK@hobby-kjjhomhijildgbkehfaomgol.dbs.graphenedb.com:24789")

     if os.environ.get('GRAPHENEDB_URL'):
          graph_db_url = urljoin(os.environ.get('GRAPHENEDB_URL'))
          graph_db = neo4j.GraphDatabaseService(
               'http://{host}:{port}{path}'.format(
                    host=graph_db_url.hostname,
                    port=graph_db_url.port,
                    path=graph_db_url.path
               ), user_name=graph_db_url.username, password=graph_db_url.password)
     else:
          graph_db = neo4j.GraphDatabaseService('http://localhost:7474/db/data')
     return graph_db