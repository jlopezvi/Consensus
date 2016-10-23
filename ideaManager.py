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
    #                            'supporters_goal_num': 500, 'volunteers_goal_num': 5}
    def __init__(self, idea_dict):
        self.concern = idea_dict['concern']
        self.proposal = idea_dict['proposal']
        self.image_url = idea_dict['image_url']
        self.datestamp = idea_dict['datestamp']
        self.moreinfo = idea_dict['moreinfo']
        self.supporters_goal_num = idea_dict['supporters_goal_num']
        self.volunteers_goal_num = idea_dict['volunteers_goal_num']


# input: user_email, idea_obj (object from class Idea)
# output: json {"result"="added idea to database"}/{"result"="proposal already exists"}
def addIdeaToUser_aux(user_email, newidea_obj):
    user = _getParticipantByEmail(user_email)
    newidea_index = newidea_obj.proposal
    if _getIdeaByIdeaIndex(newidea_index) :
        return jsonify(result="proposal already exists")
    #TODO: create numerical index. For the moment the index is the proposal, which must be unique.
    # The numerical index could be an integer field in the idea. In the launching of the app,
    # the last assigned index would be retrieved, then each idea would be assigned with an ascending integer.
    newidea_node, = getGraph().create({"concern": newidea_obj.concern, "proposal": newidea_obj.proposal,
                                       "image_url": newidea_obj.image_url,
                                       "datestamp": newidea_obj.datestamp, "moreinfo": newidea_obj.moreinfo,
                                       "supporters_goal_num": newidea_obj.supporters_goal_num,
                                       "volunteers_goal_num": newidea_obj.volunteers_goal_num})
    newidea_node.add_labels("idea")
    _addIdeaToIndex(newidea_index, newidea_node)
    getGraph().create((user, "CREATES", newidea_node))
    #calls dynamic function to spread idea
    spreadIdeaToFollowers_aux(user_email, newidea_index)
    return jsonify(result="added idea to database")

def spreadIdeaToFollowers_aux(participant_email, idea_index) :
    followers = getFollowerContacts(participant_email)
    idea=_getIdeaByIdeaIndex(idea_index)
    for follower in followers :
        if _getIfVotingRelationshipExists(follower,idea) is False:
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

def _addIdeaToIndex(proposal, new_idea_node):
    _getIdeasIndex().add("proposal", proposal, new_idea_node)

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
