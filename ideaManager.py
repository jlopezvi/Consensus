from py2neo import neo4j
from participantManager import _get_participant_node, _getIfContactRelationshipExists
from utils import getGraph, save_file
from flask import jsonify
import json
from datetime import datetime,date


# class Idea:
#     #                           {'concern':'this is my concern <140',
#     #                           'proposal':'this is my proposal <140',
#     #                            'image_url':'.../image.jpg', 'timestamp':'01.12.2012',
#     #                            'moreinfo':'I have to say this and this and this...',
#     #                            'supporters_goal_num': 500, 'volunteers_goal_num': 5}
#     def __init__(self, idea_dict):
#         self.concern = idea_dict['concern']
#         self.proposal = idea_dict['proposal']
#         self.image_url = idea_dict['image_url']
#         self.timestamp = idea_dict['timestamp']
#         self.moreinfo = idea_dict['moreinfo']
#         self.supporters_goal_num = idea_dict['supporters_goal_num']
#         self.volunteers_goal_num = idea_dict['volunteers_goal_num']


#Used By < add_idea_to_user >
def add_idea_to_user_aux(user_email, idea_dict, ideapic_file_body):
    user = _get_participant_node(user_email)
    newidea_index = idea_dict.get('proposal')
    image_url = 'static/images/concerns/social_coffee_break.jpg'
    if _getIdeaByIdeaIndex(newidea_index):
        return jsonify({"result":"Wrong", "result_msg":"proposal already exists"})
    if ideapic_file_body is not None:
        ruta_dest = '/static/images/concerns/'
        filename = str(user_email) + str(datetime.now()) + '.png'
        image_url = save_file(ruta_dest, ideapic_file_body, filename)
    dateFormat = (datetime.now()).strftime("%d.%m.%Y")
    newidea_node, = getGraph().create({"concern": idea_dict.get('concern'), "proposal": idea_dict.get('proposal'),
                                       "image_url": image_url,
                                       "moreinfo_concern": idea_dict.get('moreinfo_concern'),
                                       "moreinfo_proposal": idea_dict.get('moreinfo_proposal'),
                                       "supporters_goal_num": idea_dict.get('supporters_goal_num'),
                                       "volunteers_goal_num": idea_dict.get('volunteers_goal_num')})
    newidea_node.add_labels("idea")
    _addIdeaToIndex(newidea_index, newidea_node)
    getGraph().create((user, "CREATED", newidea_node, {"timestamp":dateFormat}))
    return jsonify({"result":"OK", "result_msg":"added idea to database"})


# Used By < modify_idea >
def modify_idea_aux(user_email, idea_dict,ideapic_file_body):
    idea_index = idea_dict['current_proposal']
    idea_data = _getIdeaByIdeaIndex(idea_index)
    user = _get_participant_node(user_email)
    if idea_data is not None:
        fields = ['concern','proposal','moreinfo_concern','moreinfo_proposal',
                   'supporters_goal_num','volunteers_goal_num']
        data= {}
        if 'proposal' in idea_dict:
            idea_index = idea_dict['proposal']
            if _getIdeaByIdeaIndex(idea_index):
                return jsonify(result= 'Wrong New Idea: Proposal already exists')
            dateFormat = (datetime.now()).strftime("%d.%m.%Y")
            IdeaRelationshipFound = getGraph().match_one(start_node=user, rel_type="CREATED", end_node=idea_data)
            IdeaRelationshipFound["timestamp"] = dateFormat
            IdeaRelationshipFound["if_proposal_edited"] = True
            _removeFromIdeaIndex(idea_dict['current_proposal'], idea_data)
            _addIdeaToIndex(idea_dict['proposal'], idea_data)
            add_notification_to_participants(idea_data, 'edited')
        for k,v in idea_dict.items():
            if k in fields:
                data[k]=v
        for k,v in data.items():
            idea_data[k]=v
        if ideapic_file_body is not None:
            ruta_dest = '/static/images/concerns/'
            filename = str(user_email) +  str(datetime.now()) +'.png'
            image_url = save_file(ruta_dest, ideapic_file_body, filename)
            idea_data["image_url"] = image_url
        return jsonify(result= 'OK, Idea was modified')
    return jsonify(result= 'Idea Does not exist')


# input: participant email
# output: json {'ideas': [idea_node1, idea_node2,...] }
def get_ideas_created_by_participant(participant_email):
    participant = _get_participant_node(participant_email)
    ideas=[]
    rels = list(getGraph().match(start_node=participant, rel_type="CREATED"))
    for rel in rels:
        idea = get_idea_data(rel.end_node)
        ideas.append(idea)
    return jsonify({'ideas': ideas})


def get_ideas_data_created_by_participant_aux(currentuser_email, participant_email):
    currentuser = _get_participant_node(currentuser_email)
    participant = _get_participant_node(participant_email)
    ifpublicprofile = participant.get_properties()['ifpublicprofile']
    ideas_data = []
    if currentuser_email == participant_email or _getIfContactRelationshipExists(participant, currentuser) is True \
            or ifpublicprofile is True:
        ifallowed = True
        rels = list(getGraph().match(start_node=participant, rel_type="CREATED"))
        for rel in rels:
            idea_data = get_idea_data(rel.end_node)
            ideas_data.append(idea_data)
    else:
        ifallowed = False
    return jsonify({'result': 'OK',"ifallowed": ifallowed,'ideas_data': ideas_data})


# Used by ideas_for_newsfeed_aux / ideas_for_home_aux / get_ideas_data_created_by_participant_aux
# Output: << return  idea_data>>
# idea_data = {
    # 'idea_id' : 12343,
    # 'author_photo_url' : 'assets/profile/perfil-mediano.png', 'author_username' : 'Daniela', 'author_email' : 'a@',
    # 'duration' : '2 days',
    # 'supporters_goal_num' : 200, 'supporters_num' : 5, 'volunteers_goal_num' : 5, 'volunteers_num' : 2,
    # 'image_url' : 'url-to-picture',
    # 'concern': 'Some text for the concern',
    # 'proposal': 'Some text for the proposal',
    # 'support_rate' : 95,
    # 'support_rate_MIN' : 90,
    # 'supporters': [
    # { 'email': 'b@', 'username': 'Maria' }, { 'email': 'c@', 'username': 'Pedro' }
    #             ],
    # 'rejectors':[
    # { 'email': 'd@', 'username': 'Elisa' }
    #               ]
    # }
def get_idea_data(new_idea_node):
    from app import SUPPORT_RATE_MIN
    author_email = getGraph().match_one(end_node=new_idea_node, rel_type="CREATED").start_node.get_properties()['email']
    author_photo_url = _get_participant_node(author_email).get_properties()['image_url']
    author_username = _get_participant_node(author_email).get_properties()['username']
    #TODO: add numerical index to ideas
    idea_id=0
    timestamp = datetime.strptime(new_idea_node.get_properties()['timestamp'], '%d.%m.%Y')
    duration = str((datetime.now() - timestamp).days) + ' days'
    voters_num = len(list(getGraph().match(end_node=new_idea_node, rel_type="VOTED_ON")))
    #TODO: puede ser optimizado
    supporters_num= _get_vote_statistics_for_idea(new_idea_node)[0]
    #rejecters_num= getall_vote_properties(new_idea_node)[1]
    volunteers_num=_get_vote_statistics_for_idea(new_idea_node)[2]
    if voters_num == 0 :
        support_rate = 100
    else:
        support_rate = (supporters_num / voters_num)*100
    supporters = []
    rejectors = []
    for vote in (list(getGraph().match(end_node=new_idea_node, rel_type="VOTED_ON"))):
        if vote["type"]== "supporter":
            email = vote.start_node.get_properties()['email']
            username = vote.start_node.get_properties()['username']
            supporters.append({'email' : email, 'username':username })
        else:
            email = vote.start_node.get_properties()['email']
            username = vote.start_node.get_properties()['username']
            rejectors.append({'email' : email, 'username':username })
    idea_data=new_idea_node.get_properties()
    idea_data.update({'idea_id' : idea_id,
                      'author_photo_url': author_photo_url, 'author_username' : author_username,
                      'duration': duration,
                      'author_email' : author_email, 'supporters_num' : supporters_num,
                      'volunteers_num': volunteers_num,
                      'support_rate': support_rate, 'support_rate_MIN': SUPPORT_RATE_MIN,
                      'supporters' : supporters, 'rejectors' : rejectors})
    return idea_data


#used by get_idea_data
def _get_vote_statistics_for_idea(node_idea):
   rejectors_num=0
   supporters_num=0
   volunteers_num=0
   for vote_rel in (list(getGraph().match(end_node=node_idea, rel_type="VOTED_ON"))):
       if vote_rel["type"] == "supporter":
           supporters_num+=1
       else:
           rejectors_num+=1
       if vote_rel["volunteered"] == "yes":
           volunteers_num+=1
   return (supporters_num,rejectors_num,volunteers_num)



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


def _removeFromIdeaIndex(proposal, idea_data):
    _getIdeasIndex().remove("proposal", proposal, idea_data)


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
    currentUser = _get_participant_node(email)
    rels = list(getGraph().match(start_node=currentUser, rel_type="CREATED"))
    ideas = []
    for rel in rels:
        currentIdea = rel.end_node.get_properties()
        currentIdea["id"] = rel.end_node._id
        ideas.append(currentIdea)
    return ideas


def vote_on_idea_aux(user_email, inputdict):
    user = _get_participant_node(user_email)
    idea_proposal=inputdict['idea_proposal']
    idea = _getIdeaByIdeaIndex(idea_proposal)
    vote_type=inputdict['vote_type']
    vote_ifvolunteered=inputdict['vote_ifvolunteered']
    vote_timestamp=inputdict['vote_timestamp']
    if if_voting_relationship_exists(user,idea):
        if if_voting_relationship_exists_of_given_type(user, idea, vote_type, vote_ifvolunteered):
            return jsonify({'result':'Wrong: User vote exists'})
        else:
            response = create_or_modify_voting_relationship_to_given_type(user, idea, vote_type, vote_ifvolunteered, vote_timestamp)
            return response
    else:
        response = create_or_modify_voting_relationship_to_given_type(user, idea, vote_type, vote_ifvolunteered, vote_timestamp)
        supporters_num= _get_vote_statistics_for_idea(idea)[0]
        volunteers_num=_get_vote_statistics_for_idea(idea)[2]
        if supporters_num >= (idea['supporters_goal_num']) and volunteers_num >= (idea['volunteers_goal_num']):
            add_notification_to_participants(idea, 'successful')
        return response


def if_voting_relationship_exists(participant, idea):
    voting_rel = getGraph().match_one(start_node=participant, rel_type="VOTED_ON", end_node=idea)
    if voting_rel is not None: return True
    else: return False


def if_voting_relationship_exists_of_given_type(participant, idea, vote_type, vote_ifvolunteered):
    voting_rel = getGraph().match_one(start_node=participant, rel_type="VOTED_ON", end_node=idea)
    if voting_rel is not None:
        if voting_rel["type"] == vote_type and voting_rel["ifvolunteered"] == vote_ifvolunteered:
            return True
    return False


def create_or_modify_voting_relationship_to_given_type(participant, idea, vote_type, vote_ifvolunteered, vote_timestamp):
    voting_rel = getGraph().match_one(start_node=participant, rel_type="VOTED_ON", end_node=idea)
    if voting_rel is not None:
        voting_rel["type"] = vote_type
        voting_rel["ifvolunteered"] = vote_ifvolunteered
        voting_rel["timestamp"] = vote_timestamp
        return jsonify({"result": "OK: User vote was modified"})
    else:
        getGraph().create((participant, "VOTED_ON", idea, {"type":vote_type, "timestamp": vote_timestamp, "ifvolunteered": vote_ifvolunteered}))
        return jsonify({"result": "OK: User vote was created"})


# Used By <modify_idea_aux> and <vote_on_idea_aux>
def add_notification_to_participants(idea, notification_type):
    timestamp = (datetime.now()).strftime("%d.%m.%Y")
    for participant in (list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))):
        notification_rel_found = getGraph().match_one(start_node=idea, rel_type="HAS_NOTIFICATION_FOR", end_node=participant.start_node)
        if notification_rel_found is None:
            getGraph().create((idea, "HAS_NOTIFICATION_FOR",participant.start_node, {"type":notification_type,"timestamp":timestamp}))
        else:
            notification_rel_found["type"] = notification_type
            notification_rel_found["timestamp"] = timestamp
    if notification_type == 'successful':
        author_participant = getGraph().match_one(rel_type="CREATED", end_node=idea)
        notification_rel_found = getGraph().match_one(start_node=idea, rel_type="HAS_NOTIFICATION_FOR", end_node=author_participant.start_node)
        if notification_rel_found is None:
            getGraph().create((idea, "HAS_NOTIFICATION_FOR", author_participant.start_node, {"type":notification_type,"timestamp":timestamp}))
        else:
            notification_rel_found["type"] = notification_type
            notification_rel_found["timestamp"] = timestamp
    return


# Used By <remove_notification_to_participant>
def remove_notification_to_participant_aux(email, proposal_index):
    idea = _getIdeaByIdeaIndex(proposal_index)
    participant = _get_participant_node(email)
    notification_rel_found = getGraph().match_one(start_node=idea, rel_type="HAS_NOTIFICATION_FOR", end_node=participant)
    if notification_rel_found is not None:
        getGraph().delete(notification_rel_found)
        return jsonify({"result":"OK", "result_msg":"Notification Relationship was deleted"})
    return jsonify({"result":"Wrong", "result_msg":"Notification Relationship does not exist"})
