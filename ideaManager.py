from py2neo import neo4j
from participantManager import _get_participant_node, _getIfContactRelationshipExists
from utils import getGraph, save_file #, send_email
from flask import jsonify, render_template
import json, uuid
from datetime import datetime,date


# class Idea:
#     def __init__(self, idea_dict):
#         self.concern = idea_dict['concern']
#         self.proposal = idea_dict['proposal']
#         self.image_url = idea_dict['image_url']
#         self.timestamp = idea_dict['timestamp']
#         self.moreinfo = idea_dict['moreinfo']
#         self.supporters_goal_num = idea_dict['supporters_goal_num']
#         self.volunteers_goal_num = idea_dict['volunteers_goal_num']


# Used By < add_idea_to_user >
def add_idea_to_user_aux(user_email, idea_dict, ideapic_file_body):
    user = _get_participant_node(user_email)
    newidea_index = idea_dict.get('proposal')
    code_uuid = str(uuid.uuid4())
    image_url = 'static/images/concerns/social_coffee_break.jpg'
    if _getIdeaByIdeaIndex(newidea_index):
        return jsonify({"result": "Wrong", "result_msg": "proposal already exists"})
    if ideapic_file_body is not None:
        ruta_dest = '/static/images/concerns/'
        filename = code_uuid + '.png'
        image_url = save_file(ruta_dest, ideapic_file_body, filename)
    timestamp = (datetime.now()).strftime("%d.%m.%Y")
    newidea, = getGraph().create({"concern": idea_dict.get('concern'), "proposal": idea_dict.get('proposal'),
                                  "image_url": image_url, "uuid" : code_uuid,
                                  "moreinfo_concern": idea_dict.get('moreinfo_concern'),
                                  "moreinfo_proposal": idea_dict.get('moreinfo_proposal'),
                                  "supporters_goal_num": idea_dict.get('supporters_goal_num'),
                                  "volunteers_goal_num": idea_dict.get('volunteers_goal_num')})
    newidea.add_labels("idea")
    _addIdeaToIndex(newidea_index, newidea)
    getGraph().create((user, "CREATED", newidea, {"timestamp":timestamp}))
    return jsonify({"result":"OK", "result_msg":"added idea to database"})


# Used By < modify_idea >
def modify_idea_aux(idea_dict,ideapic_file_body):
    from notificationManager import _do_tasks_for_idea_editedproposal
    idea_index = idea_dict['current_proposal']
    idea = _getIdeaByIdeaIndex(idea_index)
    fields = ['concern','proposal','moreinfo_concern','moreinfo_proposal',
              'supporters_goal_num','volunteers_goal_num']
    data= {}
    if 'proposal' in idea_dict:
        idea_index = idea_dict['proposal']
        if _getIdeaByIdeaIndex(idea_index):
            return jsonify({"result":"Wrong", "result_msg": "Proposal already exists"})
        _removeFromIdeaIndex(idea_dict['current_proposal'], idea)
        _addIdeaToIndex(idea_dict['proposal'], idea)
        _do_tasks_for_idea_editedproposal(idea_index)
    for k,v in idea_dict.items():
        if k in fields:
            data[k]=v
    for k,v in data.items():
        idea[k]=v
    if ideapic_file_body is not None:
        ruta_dest = '/static/images/concerns/'
        filename =  idea['uuid'] + '.png'
        image_url = save_file(ruta_dest, ideapic_file_body, filename)
        idea["image_url"] = image_url
    return jsonify({"result":"OK", "result_msg":"Idea was modified"})


# <Used by do_cron_tasks_aux>
def remove_idea_aux(idea_index) :
    idea = _getIdeaByIdeaIndex(idea_index)
    for rel in getGraph().match(start_node=idea, bidirectional=True):
        rel.delete()
    idea.delete()
    return jsonify({"result":"OK", "result_msg":"Idea was removed"})


def get_ideas_created_by_participant_aux(participant_email, user_email):
    user = _get_participant_node(user_email)
    participant = _get_participant_node(participant_email)
    ifpublicprofile = participant.get_properties()['ifpublicprofile']
    ideas_indices=[]
    if user_email == participant_email or _getIfContactRelationshipExists(participant, user) is True \
            or ifpublicprofile is True:
        ifallowed = True
        ideas=[x.end_node for x in list(getGraph().match(start_node=participant, rel_type="CREATED"))]
        for idea in ideas:
            idea_index=idea['proposal']
            ideas_indices.append(idea_index)
    else:
        ifallowed = False
    return jsonify({"result": "OK", "ifallowed": ifallowed, "ideas_indices": ideas_indices})


def get_ideas_data_created_by_participant_aux(participant_email, user_email):
    user = _get_participant_node(user_email)
    participant = _get_participant_node(participant_email)
    ifpublicprofile = participant.get_properties()['ifpublicprofile']
    ideas_data = []
    if user_email == participant_email or _getIfContactRelationshipExists(participant, user) is True \
            or ifpublicprofile is True:
        ifallowed = True
        rels = list(getGraph().match(start_node=participant, rel_type="CREATED"))
        for rel in rels:
            idea_data = get_idea_data_aux(rel.end_node)
            ideas_data.append(idea_data)
    else:
        ifallowed = False
    return jsonify({'result': 'OK',"ifallowed": ifallowed,'ideas_data': ideas_data})


# <Used by ideas_for_newsfeed_aux / ideas_for_home_aux / get_ideas_data_created_by_participant_aux
#    /get_idea_data_DEBUG >
# input   idea_node
# Output: << return  idea_data>>
# idea_data = {
    # 'uuid' : unique_identifier_string,
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
def get_idea_data_aux(idea):
    from app import SUPPORT_RATE_MIN
    author_email = getGraph().match_one(end_node=idea, rel_type="CREATED").start_node['email']
    author_photo_url = _get_participant_node(author_email)['image_url']
    author_username = _get_participant_node(author_email)['username']
    idea_proposal = idea['proposal']
    uuid=idea['uuid']
    timestamp = datetime.strptime(idea['timestamp'], '%d.%m.%Y')
    duration = str((datetime.now() - timestamp).days) + ' days'
    #voters_num = len(list(getGraph().match(end_node=idea, rel_type="VOTED_ON")))
    supporters_num = _get_vote_statistics_for_idea(idea_proposal)[0]
    rejectors_num = _get_vote_statistics_for_idea(idea_proposal)[1]
    active_voters_num = supporters_num + rejectors_num
    volunteers_num=_get_vote_statistics_for_idea(idea_proposal)[3]
    support_rate = (supporters_num / active_voters_num) * 100 if active_voters_num is not 0 else 100
    #
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    supporters_data = []
    support_rels = [x for x in vote_rels if x["type"] == "supported"]
    supporters = [x.start_node for x in support_rels]
    for supporter in supporters:
        supporters_data.append({'email': supporter['email'], 'username': supporter['username']})
    rejectors_data = []
    rejection_rels = [x for x in vote_rels if x["type"] == "rejected"]
    rejectors = [x.start_node for x in rejection_rels]
    for rejector in rejectors:
        rejectors_data.append({'email': rejector['email'], 'username': rejector['username']})
    #
    idea_data=idea.get_properties()
    idea_data.update({'author_photo_url': author_photo_url, 'author_username' : author_username,
                      'duration': duration, 'uuid': uuid,
                      'author_email' : author_email, 'supporters_num' : supporters_num,
                      'volunteers_num': volunteers_num,
                      'support_rate': support_rate, 'support_rate_MIN': SUPPORT_RATE_MIN,
                      'supporters' : supporters_data, 'rejectors' : rejectors_data})
    return idea_data


#used by get_idea_data_aux
def _get_vote_statistics_for_idea(idea_index):
    idea=_getIdeaByIdeaIndex(idea_index)
    rejectors_num=0
    supporters_num=0
    passives_num=0
    volunteers_num=0
    for vote_rel in (list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))):
        if vote_rel["type"] == "supported":
            supporters_num+=1
        elif vote_rel["type"] == "rejected":
            rejectors_num+=1
        elif vote_rel["type"] == "ignored":
            passives_num+=1
        if vote_rel["volunteered"] == True:
           volunteers_num+=1
    return (supporters_num, rejectors_num, passives_num, volunteers_num)


def _get_supporters_emails_for_idea_aux(idea_index):
    idea=_getIdeaByIdeaIndex(idea_index)
    supporters_emails = []
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    support_rels = [x for x in vote_rels if x["type"] == "supported"]
    supporters = [x.start_node for x in support_rels]
    for supporter in supporters:
        supporters_emails.append(supporter['email'])
    return supporters_emails


def _get_volunteers_emails_for_idea_aux(idea_index):
    idea=_getIdeaByIdeaIndex(idea_index)
    volunteers_emails = []
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    volunteer_rels = [x for x in vote_rels if x["volunteered"] == True]
    volunteers = [x.start_node for x in volunteer_rels]
    for volunteer in volunteers:
        volunteers_emails.append(volunteer['email'])
    return volunteers_emails




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
    from app import SUPPORT_RATE_MIN
    from notificationManager import _do_tasks_for_idea_failurewarning, _do_tasks_for_idea_successful
    user = _get_participant_node(user_email)
    idea_index=inputdict['idea_proposal']
    idea = _getIdeaByIdeaIndex(idea_index)
    vote_type=inputdict['vote_type']
    vote_ifvolunteered=inputdict['vote_ifvolunteered']
    vote_timestamp=(datetime.now()).strftime("%d.%m.%Y")
    supporters_num= _get_vote_statistics_for_idea(idea_index)[0]
    voters_num = len(list(getGraph().match(end_node=idea, rel_type="VOTED_ON")))
    if voters_num == 0:
        support_rate = 100
    else:
        support_rate = (supporters_num / voters_num)*100
    if support_rate < SUPPORT_RATE_MIN:
        support = False
    else:
        support = True
    if _if_voting_relationship_exists(user, idea):
        if _if_voting_relationship_exists_of_given_type(user, idea, vote_type, vote_ifvolunteered):
            return jsonify({"result": "Wrong: User vote exists of same type"})
        else:
            response = _create_or_modify_voting_relationship_to_given_type(user, idea, vote_type, vote_ifvolunteered, vote_timestamp)
            supporters_num= _get_vote_statistics_for_idea(idea_index)[0]
            volunteers_num=_get_vote_statistics_for_idea(idea_index)[3]
            support_rate = (supporters_num / voters_num)*100
            print (support_rate)
            if support_rate < SUPPORT_RATE_MIN and support == True:
                _do_tasks_for_idea_failurewarning(idea_index)
            if supporters_num >= (idea['supporters_goal_num']) and volunteers_num >= (idea['supporters_goal_num']):
                _do_tasks_for_idea_successful(idea_index)
            return response
    else:
        response = _create_or_modify_voting_relationship_to_given_type(user, idea, vote_type, vote_ifvolunteered, vote_timestamp)
        supporters_num= _get_vote_statistics_for_idea(idea_index)[0]
        volunteers_num=_get_vote_statistics_for_idea(idea_index)[3]
        support_rate = (supporters_num / voters_num)*100 if voters_num is not 0 else 100
        if support_rate < SUPPORT_RATE_MIN and support == True:
            _do_tasks_for_idea_failurewarning(idea_index)
        if supporters_num >= (idea['supporters_goal_num']) and volunteers_num >= (idea['supporters_goal_num']):
            _do_tasks_for_idea_successful(idea_index)
        return response




####################
#  PURE INTERNAL
###################


def _if_voting_relationship_exists(participant, idea):
    voting_rel = getGraph().match_one(start_node=participant, rel_type="VOTED_ON", end_node=idea)
    if voting_rel is not None: return True
    else: return False


#vote_ifvolunteered = True / False / 'all'   ('all' is default)
def _if_voting_relationship_exists_of_given_type(participant, idea, vote_type, vote_ifvolunteered ='all'):
    voting_rel = getGraph().match_one(start_node=participant, rel_type="VOTED_ON", end_node=idea)
    if voting_rel is not None:
        if voting_rel["ifvolunteered"] is 'all':
            if voting_rel["type"] == vote_type: return True
        else:
            if voting_rel["type"] == vote_type and voting_rel["ifvolunteered"] == vote_ifvolunteered:
                return True
    return False


#<used by vote_on_idea_aux>
def _create_or_modify_voting_relationship_to_given_type(participant, idea, vote_type, vote_ifvolunteered, vote_timestamp):
    voting_rel = getGraph().match_one(start_node=participant, rel_type="VOTED_ON", end_node=idea)
    if voting_rel is not None:
        voting_rel["type"] = vote_type
        voting_rel["ifvolunteered"] = vote_ifvolunteered
        voting_rel["timestamp"] = vote_timestamp
        return jsonify({"result": "OK: User vote was modified"})
    else:
        getGraph().create((participant, "VOTED_ON", idea, {"type":vote_type, "timestamp": vote_timestamp, "ifvolunteered": vote_ifvolunteered}))
        return jsonify({"result": "OK: User vote was created"})




