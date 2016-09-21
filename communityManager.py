from utils import getGraph
from py2neo import neo4j
from participantManagement import _getParticipantByEmail

def saveCommunity(community):
    if _getCommunity(community) :
       return "Community %s already exists" % community
    elif _getCommunity(community) is None :
       _newCommunity(community)
       return "Community %s was successfully added" % community

def addCommunityToContact(name, email):
    userFound = _getParticipantByEmail(email)
    communityFound = _getCommunity(name)
    getGraph().create((userFound, "BELONGS_TO", communityFound))

def getCommunities(email):
    currentUser = _getUserByEmail(email)
    rels = list(getGraph().match(start_node=currentUser, rel_type="BELONGS_TO"))
    communities = []
    for rel in rels:
        communities.append(rel.end_node.get_properties())
        #print getGraph().node(rel.end_node)
    return communities

def deleteCommunity(name):
    communityFound = _getCommunity(name)
    communityFound.delete()

def _getCommunity(communityName):
    communityFound = _getCommunityIndex().get("name", communityName)
    if communityFound :
         return communityFound[0]
    return None

def _addToCommunityIndex(name, newCommunity) :
     _getCommunityIndex().add("name", name, newCommunity)

def _newCommunity(community):
    name = community.get('name')
    newCommunity, = getGraph().create({"name" : name, "description" : community.get('description')})
    _addToCommunityIndex(name, newCommunity)


def _getCommunityIndex():
    return getGraph().get_or_create_index(neo4j.Node, "Communities")
