from py2neo import neo4j

# Implementing API exceptions
# http://flask.pocoo.org/docs/0.11/patterns/apierrors/
class NotFoundError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
#class NotFoundError(Exception):
#     def __init__(self, value):
#         self.value = value
#     def __str__(self):
#         return repr(self.value)


def getGraph() :
     #print(neo4j, neo4j.__file__)
     return neo4j.GraphDatabaseService("http://localhost:7474/db/data")
