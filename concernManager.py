from py2neo import neo4j
from userManagement import __getUserByEmail
from utils import NotFoundError,getGraph
import json

#input: current(current user email); concern (is a )
#output: creates a newConcern related to current user.
def addConcernToUser_aux(current, concern):
    title = concern.get('title')
    description = concern.get('description')
    image_url= concern.get('image_url')
    user = __getUserByEmail(current)
    newConcern, = getGraph().create({"title" : title, "description" : description, "image_url" : image_url})
    newConcern.add_labels("idea")
    __addConcernToIndex(title, newConcern)
    getGraph().create((user, "CREATES", newConcern))

def __addConcernToIndex(title,newConcern):
    getConcernsIndex().add("title",title,newConcern)
    

def getConcernsIndex():
    return getGraph().get_or_create_index(neo4j.Node, "Concerns")
    
def deleteOneConcern(id):
    concern = getGraph().node(id)
    print (concern[0])
    #getConcernsIndex().get("title", concern.get("title")).delete()

def getAllConcerns(email):
    print ("getAllConcerns")
    currentUser = __getUserByEmail(email)
    rels = list(getGraph().match(start_node=currentUser, rel_type="CREATES"))
    concerns = []
    for rel in rels:
        currentConcern = rel.end_node.get_properties()
        currentConcern["id"] = rel.end_node._id
        concerns.append(currentConcern)
    return concerns

