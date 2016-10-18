from py2neo import neo4j

def getGraph() :
     #print(neo4j, neo4j.__file__)
     #return neo4j.GraphDatabaseService("http://localhost:7474/db/data")
     return neo4j.GraphDatabaseService("http://hobby-kjjhomhijildgbkehfaomgol.dbs.graphenedb.com:24789/db/data")
