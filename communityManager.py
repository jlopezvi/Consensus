from utils import NotFoundError,getGraph
from py2neo import neo4j
from userManagement import __getUserByEmail

def saveCommunity(community):
    try:
       __getCommunity(community)
       return "Community %s already exists" % community
    except NotFoundError as e:
       __newCommunity(community)
       return "Community %s was successfully added" % community

def addCommunityToContact(name, email):
    userFound = __getUserByEmail(email)
    communityFound = __getCommunity(name)
    getGraph().create((userFound, "BELONGS_TO", communityFound))

def getCommunities(email):
    currentUser = __getUserByEmail(email)
    rels = list(getGraph().match(start_node=currentUser, rel_type="BELONGS_TO"))
    communities = []
    for rel in rels:
        communities.append(rel.end_node.get_properties())
        #print getGraph().node(rel.end_node)
    return communities

def deleteCommunity(name):
    communityFound = __getCommunity(name)
    communityFound.delete()

def __getCommunity(communityName):
    communityFound = __getCommunityIndex().get("name", communityName)
    if communityFound :
         return communityFound[0]
    raise NotFoundError("Community named %s does not exist" % communityName)

def __addToCommunityIndex(name, newCommunity) :
     __getCommunityIndex().add("name", name, newCommunity)

def __newCommunity(community):
    name = community.get('name')
    newCommunity, = getGraph().create({"name" : name, "description" : community.get('description')})
    __addToCommunityIndex(name, newCommunity)


def __getCommunityIndex():
    return getGraph().get_or_create_index(neo4j.Node, "Communities")
