from py2neo import neo4j
from participantManager import _get_participant_node, _getIfContactRelationshipExists, _get_participant_followers, \
    _get_participant_followings
from utils import getGraph, save_file, _remove_file
from flask import jsonify, render_template
import json, uuid
from datetime import datetime,date
from math import log10
from imageConverter import *
import os
basedir = os.path.abspath(os.path.dirname(__file__))

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
def add_idea_to_user_aux(user_email, idea_dict):
    user = _get_participant_node(user_email)
    newidea_index = idea_dict.get('proposal')
    code_uuid = str(uuid.uuid4())
    # image goes from base64 to separate JPG file
    if idea_dict.get('image') is None:
        image_url = '/static/images/fondo-c.jpg'
    else:
        image_url = base64ToJGP(idea_dict.get('image'), '/ideas/'+code_uuid)
    #
    if _get_idea_by_ideaindex(newidea_index):
        return jsonify({"result": "Wrong", "result_msg": "proposal already exists"})
    timestamp = (datetime.now()).strftime("%d.%m.%Y %H:%M:%S")
    newidea, = getGraph().create({"concern": idea_dict.get('concern'), "proposal": idea_dict.get('proposal'),
                                  "image_url": image_url, "uuid": code_uuid,
                                  "moreinfo_concern": idea_dict.get('moreinfo_concern'),
                                  "moreinfo_proposal": idea_dict.get('moreinfo_proposal'),
                                  "supporters_goal_num": idea_dict.get('supporters_goal_num'),
                                  "volunteers_goal_num": idea_dict.get('volunteers_goal_num'),
                                  "if_author_public": idea_dict.get('if_author_public')})
    newidea.add_labels("idea")
    _add_idea_to_index(newidea_index, newidea)
    getGraph().create((user, "CREATED", newidea, {"timestamp": timestamp}))
    # first receivers
    first_receivers = map(_get_participant_node, idea_dict.get('first_receivers_emails'))
    for participant in first_receivers:
        getGraph().create((newidea, "GOES_FIRST_TO", participant))
    #
    return jsonify({"result":"OK", "result_msg":"added idea to database"})


# Used By < modify_idea >
def modify_idea_aux(idea_dict):
    idea_index = idea_dict['current_proposal']
    idea = _get_idea_by_ideaindex(idea_index)
    fields = ['concern','proposal','moreinfo_concern','moreinfo_proposal',
              'supporters_goal_num','volunteers_goal_num', 'if_author_public']
    data= {}
    for k,v in idea_dict.items():
        if k in fields:
            data[k]=v
    for k,v in data.items():
        idea[k]=v
    if 'image' in idea_dict:
        # image goes from base64 to separate JPG file
        code_uuid = str(uuid.uuid4())
        if idea_dict.get('image') is None:
            image_url = '/static/images/fondo-c.jpg'
        else:
            image_url = base64ToJGP(idea_dict['image'], '/ideas/' + code_uuid)
        path = basedir + idea['image_url']
        if os.path.isfile(path):
            os.remove(path)
        idea['image_url'] = image_url
    if 'proposal' in idea_dict:
        idea_index = idea_dict['proposal']
        if _get_idea_by_ideaindex(idea_index):
            return jsonify({"result":"Wrong", "result_msg": "Proposal already exists"})
        _remove_from_idea_index(idea_dict['current_proposal'], idea)
        _add_idea_to_index(idea_dict['proposal'], idea)
        _do_tasks_for_idea_editedproposal(idea_index)
    return jsonify({"result":"OK", "result_msg":"Idea was modified"})


# <Used by do_cron_tasks_aux>, <redflag_idea_aux>
def remove_idea_aux(idea_index) :
    idea = _get_idea_by_ideaindex(idea_index)
    return jsonify(_remove_idea(idea))


# <used by remove_idea_aux, remove_user_aux>
def _remove_idea(idea):
    for rel in getGraph().match(start_node=idea, bidirectional=True):
        rel.delete()
    #
    _send_notification_emails_from_idea_to_supporters(idea['proposal'], 'removed')
    _remove_from_idea_index(idea['proposal'], idea)
    if idea['image_url'].startswith('/static/images/ideas/'):
        _remove_file(idea['image_url'])
    idea.delete()
    return {"result":"OK", "result_msg":"Idea was removed"}


def get_ideas_created_by_participant_aux(participant_email, user_email):
    user = _get_participant_node(user_email)
    participant = _get_participant_node(participant_email)
    ifuserisparticipant = (user_email == participant_email)
    ifpublicprofile = participant['ifpublicprofile']
    ideas_indices = []
    if ifuserisparticipant or _getIfContactRelationshipExists(participant, user) or ifpublicprofile:
        ifallowed = True
        ideas_indices = _get_ideas_created_by_participant_for_user(participant_email, user_email)['ideas_indices']
    else:
        ifallowed = False
    return jsonify({"result": "OK", "ifallowed": ifallowed, "ideas_indices": ideas_indices})


def get_idea_data_for_user_aux(idea_index, user_email):
    idea = _get_idea_by_ideaindex(idea_index)
    idea_data = _get_idea_data_for_user(idea, user_email)
    return jsonify({'result': 'OK', 'idea_data': idea_data})


def get_ideas_data_created_by_participant_aux(participant_email, user_email):
    user = _get_participant_node(user_email)
    participant = _get_participant_node(participant_email)
    ifuserisparticipant = (user_email == participant_email)
    ifpublicprofile = participant.get_properties()['ifpublicprofile']
    ideas_data = []
    if ifuserisparticipant or _getIfContactRelationshipExists(participant, user) or ifpublicprofile:
        ifallowed = True
        ideas_data = _get_ideas_data_created_by_participant_for_user(participant_email, user_email)['ideas_data']
    else:
        ifallowed = False
    return jsonify({'result': 'OK',"ifallowed": ifallowed, "ideas_data": ideas_data})


def get_vote_statistics_for_idea_aux(idea_index):
    return _get_vote_statistics_for_idea(idea_index)


def _get_supporters_emails_for_idea_aux(idea_index):
    idea=_get_idea_by_ideaindex(idea_index)
    supporters_emails = []
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    support_rels = [x for x in vote_rels if x["type"] == "supported"]
    supporters = [x.start_node for x in support_rels]
    for supporter in supporters:
        supporters_emails.append(supporter['email'])
    return supporters_emails


def _get_volunteers_emails_for_idea_aux(idea_index):
    idea=_get_idea_by_ideaindex(idea_index)
    volunteers_emails = []
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    volunteer_rels = [x for x in vote_rels if x["ifvolunteered"] == True]
    volunteers = [x.start_node for x in volunteer_rels]
    for volunteer in volunteers:
        volunteers_emails.append(volunteer['email'])
    return volunteers_emails


def get_voting_rel_between_user_and_idea_aux(user_email, idea_proposal):
    user = _get_participant_node(user_email)
    idea = _get_idea_by_ideaindex(idea_proposal)
    if _if_voting_relationship_exists(user,idea):
        voting_rel = getGraph().match_one(start_node=user, rel_type="VOTED_ON", end_node=idea)
        vote_type= voting_rel["type"]
        vote_ifvolunteered = voting_rel["ifvolunteered"]
        return jsonify({"result": "OK", "vote_type":vote_type, "vote_ifvolunteered":vote_ifvolunteered})
    else:
        return jsonify({"result": "Wrong", "result_msg":"Voting relationship does not exist"})


def vote_on_idea_aux(user_email, inputdict):
    from app import SUPPORT_RATE_MIN
    user = _get_participant_node(user_email)
    idea_index=inputdict['idea_proposal']
    idea = _get_idea_by_ideaindex(idea_index)
    vote_type=inputdict['vote_type']
    vote_ifvolunteered=inputdict['vote_ifvolunteered']
    vote_timestamp=(datetime.now()).strftime("%d.%m.%Y %H:%M:%S")
    previous_supporters_num= _get_vote_statistics_for_idea(idea_index)[0]
    previous_rejectors_num = _get_vote_statistics_for_idea(idea_index)[1]
    previous_activevoters_num = previous_supporters_num + previous_rejectors_num
    # previous support rate
    if previous_activevoters_num == 0:
        previous_support_rate = 100
    else:
        previous_support_rate = (previous_supporters_num / previous_activevoters_num)*100
    if previous_support_rate < SUPPORT_RATE_MIN:
        if_previous_support_rate_OK = False
    else:
        if_previous_support_rate_OK = True
    #
    if _if_voting_relationship_exists(user, idea):
        if _if_voting_relationship_exists_of_given_type(user, idea, vote_type, vote_ifvolunteered):
            return jsonify({"result": "Wrong: User vote exists of same type"})
    response = _create_or_modify_voting_relationship_to_given_type(user, idea, vote_type, vote_ifvolunteered, vote_timestamp)
    supporters_num = _get_vote_statistics_for_idea(idea_index)[0]
    rejectors_num =  _get_vote_statistics_for_idea(idea_index)[1]
    activevoters_num = supporters_num + rejectors_num
    volunteers_num = _get_vote_statistics_for_idea(idea_index)[3]
    support_rate = (supporters_num / activevoters_num)*100 if activevoters_num is not 0 else 100
    # failure warning notification
    if 'if_failurewarning_timestamp' in idea:
        # notification should not be re-fired before three days from the previous one.
        failurewarning_timestamp = datetime.strptime(idea['if_failurewarning_timestamp'], '%d.%m.%Y %H:%M:%S')
        if_time_condition_for_failurewarning = ((datetime.now() - failurewarning_timestamp).days >= 3)
    else:
        if_time_condition_for_failurewarning = True
    if support_rate < SUPPORT_RATE_MIN and if_previous_support_rate_OK is True and if_time_condition_for_failurewarning is True:
        _do_tasks_for_idea_failurewarning(idea_index)
    # successful idea notification
    if supporters_num >= (idea['supporters_goal_num']) and volunteers_num >= (idea['supporters_goal_num']):
        _do_tasks_for_idea_successful(idea_index)
    #
    return response


def redflag_idea_aux(user_email, idea_index, reason):
    user = _get_participant_node(user_email)
    idea = _get_idea_by_ideaindex(idea_index)
    if (_get_vote_statistics_for_idea(idea_index)[0]) > 0:
        _send_notification_emails_from_idea_to_supporters(idea_index, 'redflag', reason, user['fullname'])
    _send_notification_email_from_idea_to_author(idea_index, 'redflag', reason, user['fullname'])
    return remove_idea_aux(idea_index)


def get_idea_data_admin_aux(idea_proposal):
    idea = _get_idea_by_ideaindex(idea_proposal)
    return _get_idea_data(idea)


def get_idea_node_data_aux(idea_proposal):
    idea = _get_idea_by_ideaindex(idea_proposal)
    return _get_idea_node_data(idea)


def get_all_ideas_admin_aux():
    allnodes = _get_ideas_index().query("proposal:*")
    ideas = []
    for node in allnodes:
        ideas.append(node.get_properties())
    return ideas




####################
#  PURE INTERNAL
###################


def _ideaIsNewForParticipant(idea,participant) :
    getGraph().create((idea, "IS NEW FOR", participant))


def _add_idea_to_index(proposal, new_idea_node):
    _get_ideas_index().add("proposal", proposal, new_idea_node)
def _add_successfulidea_to_index(proposal, new_idea_node):
    _get_successfulideas_index().add("proposal", proposal, new_idea_node)

def _remove_from_idea_index(proposal, idea_data):
    _get_ideas_index().remove("proposal", proposal, idea_data)
def _remove_from_successfulidea_index(proposal, idea_data):
    _get_successfulideas_index().remove("proposal", proposal, idea_data)

def _get_idea_by_ideaindex(idea_index) :
    ideaFound = _get_ideas_index().get("proposal", idea_index)
    if ideaFound :
        return ideaFound[0]
    return None
def _get_successfulidea_by_ideaindex(idea_index) :
    ideaFound = _get_successfulideas_index().get("proposal", idea_index)
    if ideaFound :
        return ideaFound[0]
    return None

def _get_ideas_index():
    return getGraph().get_or_create_index(neo4j.Node, "Ideas")
def _get_successfulideas_index():
    return getGraph().get_or_create_index(neo4j.Node, "Successful_Ideas")


def _if_voting_relationship_exists(participant, idea):
    voting_rel = getGraph().match_one(start_node=participant, rel_type="VOTED_ON", end_node=idea)
    if voting_rel is not None: return True
    else: return False


# vote_ifvolunteered = True / False / 'all'   ('all' is default)
def _if_voting_relationship_exists_of_given_type(participant, idea, vote_type, vote_ifvolunteered ='all'):
    voting_rel = getGraph().match_one(start_node=participant, rel_type="VOTED_ON", end_node=idea)
    if voting_rel is not None:
        if voting_rel["ifvolunteered"] is 'all':
            if voting_rel["type"] == vote_type: return True
        else:
            if voting_rel["type"] == vote_type and voting_rel["ifvolunteered"] == vote_ifvolunteered:
                return True
    return False


# <used by vote_on_idea_aux>
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


# <Used by get_ideas_created_by_participant_aux, _get_participant_summary_data_unrestricted>
def _get_ideas_created_by_participant_for_user(participant_email, user_email):
    ifuserisparticipant = (participant_email == user_email)
    participant = _get_participant_node(participant_email)
    ideas_indices=[]
    ideas=[x.end_node for x in list(getGraph().match(start_node=participant, rel_type="CREATED"))]
    if ifuserisparticipant:  # no restrictions
        for idea in ideas:
            idea_index = idea['proposal']
            ideas_indices.append(idea_index)
    else:                    # erase anonymous ideas
        for idea in ideas:
            if idea['if_author_public'] is False:
                continue
            idea_index = idea['proposal']
            ideas_indices.append(idea_index)
    return {'result': 'OK', 'ideas_indices': ideas_indices}


def _get_all_ideas_created_by_participant_DEBUG(participant_email):
    participant = _get_participant_node(participant_email)
    ideas_indices=[]
    ideas=[x.end_node for x in list(getGraph().match(start_node=participant, rel_type="CREATED"))]
    for idea in ideas:
        idea_index = idea['proposal']
        ideas_indices.append(idea_index)
    return {'result': 'OK', 'ideas_indices': ideas_indices}


# <Used by get_ideas_data_created_by_participant_aux, _get_participant_data_for_user>
def _get_ideas_data_created_by_participant_for_user(participant_email, user_email):
    ifuserisparticipant = (participant_email == user_email)
    participant = _get_participant_node(participant_email)
    ideas_data = []
    rels = list(getGraph().match(start_node=participant, rel_type="CREATED"))
    if ifuserisparticipant:  # no restrictions
        for rel in rels:
            idea_data = _get_idea_data_for_user(rel.end_node, user_email)
            ideas_data.append(idea_data)
    else:                    # erase anonymous ideas
        for rel in rels:
            if rel.end_node['if_author_public'] is False:
                continue
            idea_data = _get_idea_data_for_user(rel.end_node, user_email)
            ideas_data.append(idea_data)
    return {'result': 'OK', 'ideas_data': ideas_data}



def _if_ideaisinfirstphase(idea):
    # if (one day has passed since creation of the idea) then False
    # datetime_now = ((datetime.now()).strftime("%d.%m.%Y"))
    datetime_ideacreation = datetime.strptime(getGraph().match_one(rel_type="CREATED", end_node=idea)["timestamp"], '%d.%m.%Y %H:%M:%S')
    if ((datetime.now()) - datetime_ideacreation).days >= 1:
        return False
    # if (any of the first receivers has not voted) then True
    idea_first_receivers = [x.end_node for x in list(getGraph().match(start_node=idea, rel_type="GOES_FIRST_TO"))]
    for idea_first_receiver in idea_first_receivers:
        if getGraph().match_one(start_node=idea_first_receiver, rel_type="HAS_VOTED_ON", end_node=idea) is None:
            return True
    # else False
    return False


# <Used by  get_idea_data_admin  >
# input   idea_node
# Output: << return  idea_data>>
# idea_data = {
#             'concern': 'Some text for the concern',
#             'proposal': 'Some text for the proposal',
#             'image_url': 'static/.../asdf.JPG'/None,
#             'uuid': 'unique_identifier_string',
#             'moreinfo_concern': 'blah blah blah more info',
#             'moreinfo_proposal': 'blah blah blah more info',
#             'supporters_goal_num': 200,
#             'volunteers_goal_num': 5,
#             'if_author_public': True / False
#             'author_profilepic_url': 'static/.../pic.jpg'/None, 'author_username': 'daniela', 'author_email': 'a@gmail.com',
#             'duration' : "4 hours/ days/ weeks",
#             'supporters_num' : 5, 'volunteers_num' : 2, 'rejectors_num': 3,
#             'support_rate' : 95, 'support_rate_MIN' : 90,
#             'supporters': [
#                { 'email': 'b@', 'username': 'Juan' }, { 'email': 'c@gmail.com', 'username': 'Pedro' }
#              ],
#             'rejectors':[
#                { 'email': 'd@', 'username': 'Elisa' }
#              ]
#            }
def _get_idea_data(idea):
    from app import SUPPORT_RATE_MIN
    author_email = getGraph().match_one(end_node=idea, rel_type="CREATED").start_node['email']
    author_profilepic_url = _get_participant_node(author_email)['profilepic_url']
    author_username = _get_participant_node(author_email)['username']
    idea_proposal = idea['proposal']
    uuid = idea['uuid']
    duration = _get_idea_duration(idea_proposal)
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
    idea_data.update({'author_profilepic_url': author_profilepic_url, 'author_username' : author_username,
                      'duration': duration, 'uuid': uuid,
                      'author_email' : author_email, 'supporters_num' : supporters_num,
                      'volunteers_num': volunteers_num, 'rejectors_num': rejectors_num,
                      'support_rate': support_rate, 'support_rate_MIN': SUPPORT_RATE_MIN,
                      'supporters' : supporters_data, 'rejectors' : rejectors_data})
    return idea_data


# <Used by ideas_for_newsfeed_aux / ideas_for_home_aux / get_topten_ideas /
# get_idea_data_for_user_aux / _get_ideas_data_created_by_participant_for_user >
# input   idea_node
# Output: << return  idea_data>>
# idea_data = {
#             'concern': 'Some text for the concern',
#             'proposal': 'Some text for the proposal',
#             'image_url': 'static/.../asdf.JPG'/None,
#             'uuid': 'unique_identifier_string',
#             'moreinfo_concern': 'blah blah blah more info',
#             'moreinfo_proposal': 'blah blah blah more info',
#             'supporters_goal_num': 200,
#             'volunteers_goal_num': 5,
#             'if_author_public': True / False
#             'author_profilepic_url': 'static/.../pic.jpg'/None, 'author_username': 'daniela', 'author_email': 'a@gmail.com',
#             'duration' : "4 hours/ days/ weeks",
#             'supporters_num' : 5, 'volunteers_num' : 2, 'rejectors_num': 3,
#             'support_rate' : 95, 'support_rate_MIN' : 90,
#             'identified_supporters': [
#                { 'email': 'user', 'username': 'me' }, { 'email': 'c@gmail.com', 'username': 'Pedro' }
#              ],
#             'identified_rejectors':[
#                { 'email': 'd@', 'username': 'Elisa' }
#              ],
#             'vote_type': None / 'supported' / 'rejected' / 'ignored'
#             'vote_ifvolunteered': None / True / False
#             'vote_duration': '<24h' / '<7days' / '<30days' / 'older'
#             'unidentified_supporters_text': "+ 2 people"/"",
#             'unidentified_rejectors_text': "+ 2 people"/""
#            }
def _get_idea_data_for_user(idea, user_email):
    from app import SUPPORT_RATE_MIN, SUPPORTERS_CHAR_NUM_MAX, REJECTORS_CHAR_NUM_MAX
    user = _get_participant_node(user_email)
    author_email = getGraph().match_one(end_node=idea, rel_type="CREATED").start_node['email']
    author_profilepic_url = _get_participant_node(author_email)['profilepic_url']
    author_username = _get_participant_node(author_email)['username']
    idea_proposal = idea['proposal']
    uuid = idea['uuid']
    duration = _get_idea_duration(idea_proposal)
    # voters_num = len(list(getGraph().match(end_node=idea, rel_type="VOTED_ON")))
    supporters_num = _get_vote_statistics_for_idea(idea_proposal)[0]
    rejectors_num = _get_vote_statistics_for_idea(idea_proposal)[1]
    active_voters_num = supporters_num + rejectors_num
    volunteers_num=_get_vote_statistics_for_idea(idea_proposal)[3]
    support_rate = round((supporters_num / active_voters_num) * 100, 1) if active_voters_num is not 0 else 100
    #
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    followers = _get_participant_followers(user_email)
    followings = _get_participant_followings(user_email)
    #
    identified_supporters_data = []
    supporters_char_counter = 0
    supporters = [x.start_node for x in vote_rels if x["type"] == "supported"]
    # known supporters are either the user or (followers or followings with the right public permissions)
    identified_supporters = [x for x in supporters if x == user or
                        ((x in followers or x in followings) and x['ifsupportingproposalsvisible'] is True)]
    for identified_supporter in identified_supporters:
        if identified_supporter == user:
            supporters_char_counter += 4
            identified_supporters_data.insert(0, {'email': 'user', 'username': 'me'})
        else:
            supporters_char_counter=supporters_char_counter + 2 + len(identified_supporter['username'])
            if supporters_char_counter <= SUPPORTERS_CHAR_NUM_MAX:
                identified_supporters_data.append({'email': identified_supporter['email'], 'username': identified_supporter['username']})
    unidentified_supporters_num = supporters_num - len(identified_supporters_data)
    unidentified_supporters_text_beginning = "+ " if len(identified_supporters_data) >= 1 else ""
    unidentified_supporters_text = unidentified_supporters_text_beginning + str(unidentified_supporters_num) + " people"
    if len(identified_supporters_data) >=1 and unidentified_supporters_num == 0:
        unidentified_supporters_text = ""
    #
    identified_rejectors_data = []
    rejectors_char_counter = 0
    rejectors = [x.start_node for x in vote_rels if x["type"] == "rejected"]
    # known rejectors are either the user or (followers or followings with the right public permissions)
    identified_rejectors = [x for x in rejectors if x == user or
                        ((x in followers or x in followings) and x['ifrejectingproposalsvisible'] is True)]
    for identified_rejector in identified_rejectors:
        if identified_rejector == user:
            rejectors_char_counter = rejectors_char_counter + 4
            identified_rejectors_data.insert(0, {'email': 'user', 'username': 'me'})
        else:
            rejectors_char_counter = rejectors_char_counter + 2 + len(identified_rejector['username'])
            if rejectors_char_counter <= REJECTORS_CHAR_NUM_MAX:
                identified_rejectors_data.append({'email': identified_rejector['email'], 'username': identified_rejector['username']})
    unidentified_rejectors_num = rejectors_num - len(identified_rejectors_data)
    unidentified_rejectors_text_beginning = "+ " if len(identified_rejectors_data) >= 1 else ""
    unidentified_rejectors_text = unidentified_rejectors_text_beginning + str(unidentified_rejectors_num) + " people"
    if len(identified_rejectors_data) >=1 and unidentified_rejectors_num == 0:
        unidentified_rejectors_text = ""
    #
    idea_data=idea.get_properties()
    idea_data.update({'author_profilepic_url': author_profilepic_url, 'author_username': author_username,
                      'duration': duration, 'uuid': uuid,
                      'author_email': author_email, 'supporters_num': supporters_num,
                      'rejectors_num': rejectors_num, 'volunteers_num': volunteers_num,
                      'support_rate': support_rate, 'support_rate_MIN': SUPPORT_RATE_MIN,
                      'identified_supporters': identified_supporters_data, 'identified_rejectors': identified_rejectors_data,
                      'unidentified_supporters_text': unidentified_supporters_text, 'unidentified_rejectors_text': unidentified_rejectors_text})
    # add possible voting relationship, or None
    vote_type = None
    vote_ifvolunteered = None
    vote_duration = None
    voting_rel = getGraph().match_one(start_node=user, rel_type="VOTED_ON", end_node=idea)
    if voting_rel:
        vote_type = voting_rel["type"]
        vote_ifvolunteered = voting_rel["ifvolunteered"]
        vote_duration = _get_idea_vote_duration(datetime.strptime(voting_rel["timestamp"], '%d.%m.%Y %H:%M:%S'))
    idea_data.update({'vote_type': vote_type, 'vote_ifvolunteered': vote_ifvolunteered, 'vote_duration':vote_duration})
    #
    return idea_data


# <Used by get_idea_node_data_aux >
# input   idea_node
# Output: << return  idea_node's data >>  as a python dictionary
def _get_idea_node_data(idea):
    return idea.get_properties()


def _get_idea_duration(idea_index):
    idea=_get_idea_by_ideaindex(idea_index)
    timestamp = datetime.strptime(getGraph().match_one(end_node=idea, rel_type="CREATED")["timestamp"], '%d.%m.%Y %H:%M:%S')
    days = (datetime.now() - timestamp)
    duration = str(days.days) + ' days'
    if days.days < 1:
        hours = int(days.total_seconds() / 3600)
        duration = str(hours) + ' hours'
        if hours == 0:
            duration = '< 1 hour'
    if days.days >= 7:
        week = int(days.days / 7)
        duration = str(week) + ' weeks'
        if week == 1:
            duration = str(week) + ' week'
    return duration


def _get_idea_vote_duration(vote_timestamp):
    duration_raw = (datetime.now() - vote_timestamp)
    duration_days = duration_raw.days
    if duration_days < 1:
        vote_duration = "<24h"
    elif duration_days < 7:
        vote_duration = "<7days"
    elif duration_days < 30:
        vote_duration = "<30days"
    else:
        vote_duration = "older"
    return vote_duration


# <used by _get_idea_data> [0]->supporters, [1]->rejectors, [2]->passives, [3]->volunteers
def _get_vote_statistics_for_idea(idea_index):
    idea=_get_idea_by_ideaindex(idea_index)
    rejectors_num=0
    supporters_num=0
    passives_num=0
    volunteers_num=0
    for vote_rel in (list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))):
        if vote_rel["type"] == "supported":
            supporters_num += 1
        elif vote_rel["type"] == "rejected":
            rejectors_num += 1
        elif vote_rel["type"] == "ignored":
            passives_num += 1
        if vote_rel["ifvolunteered"] is True:
            volunteers_num += 1
    return (supporters_num, rejectors_num, passives_num, volunteers_num)


def _get_idea_score(idea):
    from app import SUPPORT_RATE_MIN
    vote_statistics_for_idea = _get_vote_statistics_for_idea(idea['proposal'])
    supporters_num = vote_statistics_for_idea[0]
    rejectors_num = vote_statistics_for_idea[1]
    if supporters_num == 0:
        return 0
    # volunteers ?
    # supporters points in range [0, infinity]
    supporters_points = log10(supporters_num)
    support_rate = supporters_num / (rejectors_num + supporters_num) * 100
    # support_rate_points in range [0,1]
    support_rate_points = (10 ** ((support_rate - SUPPORT_RATE_MIN) / (100 - SUPPORT_RATE_MIN)) - 1.) / 9.
    # total number
    points = support_rate_points + supporters_points
    return points


####################

####################
#  NOTIFICATIONS
###################

####################
# from utils import getGraph, save_file #, send_email
# from flask import jsonify, render_template
# import json, uuid
# from datetime import datetime,date
# from participantManager import _get_participant_node
# from ideaManager import _get_idea_by_ideaindex, _get_supporters_emails_for_idea_aux, _get_volunteers_emails_for_idea_aux
from utils import send_email


def get_ideanotifications_for_user_aux(user_email):
    user = _get_participant_node(user_email)
    notifications = []
    current_notification = {}
    #1 notifications as author of ideas
    author_rels = list(getGraph().match(start_node=user, rel_type="CREATED"))
    for author_rel in author_rels:
        if author_rel["ifnotification_successful"] is True:
            current_notification.update({'notification_type': 'successful' ,
                                         'idea_index': author_rel.end_node['proposal']})
            notifications.append(current_notification)
        if author_rel["ifnotification_failurewarning"] is True:
            current_notification.update({'notification_type': 'failurewarning' ,
                                         'idea_index': author_rel.end_node['proposal']})
            notifications.append(current_notification)
    #2 notifications as supporter of ideas
    vote_rels = list(getGraph().match(start_node=user, rel_type="VOTED_ON"))
    support_rels = [x for x in vote_rels if x["type"] == "supported"]
    for support_rel in support_rels:
        if support_rel["ifnotification_successful"] is True:
            current_notification.update({'notification_type': 'successful' ,
                                         'idea_index': support_rel.end_node['proposal']})
            notifications.append(current_notification)
        if support_rel["ifnotification_editedproposal"] is True:
            current_notification.update({'notification_type': 'editedproposal' ,
                                         'idea_index': support_rel.end_node['proposal']})
            notifications.append(current_notification)
    #
    return jsonify({"result": "OK", "data": notifications})


# Used By <remove_notification_to_participant>
def remove_notification_from_idea_to_participant_aux(participant_email, proposal_index, notification_type):
    idea = _get_idea_by_ideaindex(proposal_index)
    participant = _get_participant_node(participant_email)
    notification_field_str = 'ifnotification_' + notification_type
    #1 remove notification as author of idea
    author_rel_found = getGraph().match_one(start_node=participant, rel_type="CREATED",
                                                  end_node=idea)
    if author_rel_found[notification_field_str] is not None:
        author_rel_found[notification_field_str] = False
    #2 remove notification as supporter of idea
    vote_rel_found = getGraph().match_one(start_node=participant, rel_type="VOTED_ON",
                                                  end_node=idea)
    if vote_rel_found[notification_field_str] is not None:
        vote_rel_found[notification_field_str] = False
    #
    return jsonify({"result": "OK", "result_msg": "Notification was deleted"})


####################
#  PURE INTERNAL
###################

# <used by modify_idea_aux>
def _do_tasks_for_idea_editedproposal(idea_index):
    idea=_get_idea_by_ideaindex(idea_index)
    idea['if_editedproposal'] = True
    idea['if_editedproposal_timestamp'] = ((datetime.now()).strftime("%d.%m.%Y %H:%M:%S"))
    _add_notifications_from_idea_to_supporters(idea_index, 'edited')
    return


# <used by vote_on_idea_aux>
def _do_tasks_for_idea_failurewarning(idea_index):
    idea=_get_idea_by_ideaindex(idea_index)
    idea['if_failurewarning'] = True
    idea['if_failurewarning_timestamp'] = ((datetime.now()).strftime("%d.%m.%Y %H:%M:%S"))
    _add_notification_from_idea_to_author(idea_index, 'failurewarning')
    _add_notifications_from_idea_to_supporters(idea_index, 'failurewarning')
    _send_notification_email_from_idea_to_author(idea_index, 'failurewarning')
    return


#TODO ampliar la funciones
# _add_notifications_from_idea_to_supporters(idea_index, 'successful')
#    --> _add_notifications_from_idea_to_voters(idea_index, 'successful', ['supporters', 'rejectors'])
# _send_notification_emails_from_idea_to_supporters(idea_index, 'successful')
#    --> _send_notification_emails_from_idea_to_voters(idea_index, 'successful', ['supporters', 'rejectors'])
# <used by vote_on_idea_aux>
def _do_tasks_for_idea_successful(idea_index):
    idea=_get_idea_by_ideaindex(idea_index)
    idea['if_successful'] = True
    idea['if_successful_timestamp'] = ((datetime.now()).strftime("%d.%m.%Y %H:%M:%S"))
    _add_notifications_from_idea_to_supporters(idea_index, 'successful')
    _add_notifications_from_idea_to_rejectors(idea_index, 'successful')
    _add_notification_from_idea_to_author(idea_index, 'successful_to_author')
    _send_notification_emails_from_idea_to_supporters(idea_index, 'successful')
    _send_notification_emails_from_idea_to_rejectors(idea_index, 'successful')
    _send_notification_email_from_idea_to_author(idea_index, 'successful_to_author')
    return


# <used by _do_tasks_for_idea_editedproposal, _do_tasks_for_idea_failurewarning, _do_tasks_for_idea_successful>
#  notification_type_possibilities = ['editedproposal', 'successful', 'failurewarning']
def _add_notifications_from_idea_to_supporters(idea_index, notification_type):
    notification_field_str = 'ifnotification_' + notification_type
    idea = _get_idea_by_ideaindex(idea_index)
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    support_rels = [x for x in vote_rels if x["type"] == "supported"]
    for support_rel in support_rels:
        support_rel[notification_field_str] = True
    return

# <used by _do_tasks_for_idea_successful>
#  notification_type_possibilities = ['successful']
def _add_notifications_from_idea_to_rejectors(idea_index, notification_type):
    notification_field_str = 'ifnotification_' + notification_type
    idea = _get_idea_by_ideaindex(idea_index)
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    reject_rels = [x for x in vote_rels if x["type"] == "rejected"]
    for reject_rel in reject_rels:
        reject_rels[notification_field_str] = True
    return

# <used by _do_tasks_for_idea_successful>
#  notification_type_possibilities = ['successful']
def _send_notification_emails_from_idea_to_rejectors(idea_index, notification_type):
    idea = _get_idea_by_ideaindex(idea_index)
    subject = "Consensus, New Notifications"
    if notification_type == 'successful':
        html = render_template('emails/idea_successful.html', msg_proposal=idea['proposal'])
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    reject_rels = [x for x in vote_rels if x["type"] == "rejected"]
    rejectors = [x.start_node for x in reject_rels]
    for rejector in rejectors:
        send_email(rejector['email'], subject, html)
    return

# TODO add types 'failed', 'removed'
# <used by _do_tasks_for_idea_editedproposal, _do_tasks_for_idea_failurewarning, _do_tasks_for_idea_successful>
def _send_notification_emails_from_idea_to_supporters(idea_index, notification_type, reason = None, participant_fullname = None):
    idea = _get_idea_by_ideaindex(idea_index)
    subject = "Consensus, New Notifications"
    if notification_type == 'edited':
        html = render_template('emails/idea_edited.html', msg_proposal=idea['proposal'])
    elif notification_type == 'successful':
        html = render_template('emails/idea_successful.html', msg_proposal=idea['proposal'])
    elif notification_type == 'removed':
        # TODO
        return
    elif notification_type == 'redflag':
        html = render_template('emails/idea_redflag.html', msg_proposal=idea['proposal'], msg_reason= reason, msg_participant= participant_fullname)
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    support_rels = [x for x in vote_rels if x["type"] == "supported"]
    supporters = [x.start_node for x in support_rels]
    for supporter in supporters:
        send_email(supporter['email'], subject, html)
    return


# <used by _do_tasks_for_idea_failurewarning, _do_tasks_for_idea_successful>
#  notification_type_possibilities = ['successful', failurewarning]
def _add_notification_from_idea_to_author(idea_index, notification_type):
    notification_field_str = 'ifnotification_' + notification_type
    idea = _get_idea_by_ideaindex(idea_index)
    author_rel = getGraph().match_one(rel_type="CREATED", end_node=idea)
    author_rel[notification_field_str] = True
    return

# TODO add type 'failed'
# <used by _do_tasks_for_idea_failurewarning, _do_tasks_for_idea_successful>
def _send_notification_email_from_idea_to_author(idea_index, notification_type, reason = None, participant_fullname = None):
    idea=_get_idea_by_ideaindex(idea_index)
    author = getGraph().match_one(rel_type="CREATED", end_node=idea).start_node
    subject = "Consensus, New Notifications"
    if notification_type == 'failurewarning':
        html = render_template('emails/idea_failurewarning.html', msg_proposal=idea['proposal'])
    elif notification_type == 'redflag':
        html = render_template('emails/idea_redflag.html', msg_proposal=idea['proposal'], msg_reason= reason, msg_participant= participant_fullname)
    elif notification_type == 'successful_to_author':
        volunteers = _get_volunteers_emails_for_idea_aux(idea_index)
        if len(volunteers) > 0 :
            html = render_template('emails/idea_successful.html', msg_proposal=idea['proposal'], volunteers=volunteers)
        else :
            supporters = _get_supporters_emails_for_idea_aux(idea_index)
            html = render_template('emails/idea_successful.html', msg_proposal=idea['proposal'], supporters=supporters)
    send_email(author['email'], subject, html)
    return
