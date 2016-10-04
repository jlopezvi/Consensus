from py2neo import neo4j
from participantManager import _getParticipantByEmail, getFollowerContacts
from utils import getGraph
from flask import jsonify
import json


class Idea:
    #                           {'concern':'this is my concern <140',
    #                           'proposal':'this is my proposal <140',
    #                            'image_url':'.../image.jpg', 'datestamp':'01.12.2012',
    #                            'moreinfo':'I have to say this and this and this...',
    #                            'supporters_goal': 500, 'volunteers_goal': 5}
    def __init__(self, idea_dict):
        self.concern = idea_dict['concern']
        self.proposal = idea_dict['proposal']
        self.image_url = idea_dict['image_url']
        self.datestamp = idea_dict['datestamp']
        self.moreinfo = idea_dict['moreinfo']
        self.supporters_goal = idea_dict['supporters_goal']
        self.volunteers_goal = idea_dict['volunteers_goal']


# input: user_email, idea (object from class Idea)
# output: json {"result"="added idea to database"}/{"result"="idea already exists"}
def addIdeaToUser_aux(user_email, idea):
    print("1")
    user = _getParticipantByEmail(user_email)
    idea_index = idea.proposal
    print("2")
    if _getIdeaByIdeaIndex(idea_index) :
        return jsonify(result="idea already exists")
    newIdea, = getGraph().create({"concern": idea.concern, "proposal": idea.proposal, "image_url": idea.image_url,
                                  "datestamp": idea.datestamp, "moreinfo": idea.moreinfo,
                                  "supporters_goal": idea.supporters_goal, "volunteers_goal": idea.volunteers_goal})
    newIdea.add_labels("idea")
    print("3")
    _addIdeaToIndex(idea_index, newIdea)
    getGraph().create((user, "CREATES", newIdea))
    #calls dynamic function to spread idea
    spreadIdeaToFollowers_aux(user_email, idea_index)
    print("5")
    return jsonify(result="added idea to database")

def spreadIdeaToFollowers_aux(participant_email, idea_index) :
    followers = getFollowerContacts(participant_email)
    idea=_getIdeaByIdeaIndex(idea_index)
    print("6")
    for follower in followers :
        if _getIfVotingRelationshipExists(follower,idea) is False:
            print("7")
            _ideaIsNewForParticipant(idea,follower)
    return "spreadIdeaToFollowers invoked"


#participant, idea are graph nodes
def _getIfVotingRelationshipExists(participant, idea) :
    votingRelationshipFound = getGraph().match_one(start_node=participant, end_node=idea, rel_type="VOTED")
    if votingRelationshipFound is not None:
         return True
    return False

def _ideaIsNewForParticipant(idea,participant) :
    getGraph().create((idea, "IS NEW FOR", participant))

def _addIdeaToIndex(proposal, newIdea):
    _getIdeasIndex().add("proposal", proposal, newIdea)

def _getIdeaByIdeaIndex(idea_index) :
    ideaFound = _getIdeasIndex().get("proposal", idea_index)
    if ideaFound :
        return ideaFound[0]
    return None


def _getIdeasIndex():
    return getGraph().get_or_create_index(neo4j.Node, "Ideas")


def deleteOneIdea(id):
    idea = getGraph().node(id)
    print(idea[0])
    # getIdeasIndex().get("title", idea.get("title")).delete()


def getAllIdeas(email):
    print("getAllIdeas")
    currentUser = _getParticipantByEmail(email)
    rels = list(getGraph().match(start_node=currentUser, rel_type="CREATES"))
    ideas = []
    for rel in rels:
        currentIdea = rel.end_node.get_properties()
        currentIdea["id"] = rel.end_node._id
        ideas.append(currentIdea)
    return ideas
