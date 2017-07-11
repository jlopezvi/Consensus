from py2neo import neo4j
from participantManager import _get_participant_node, _getIfContactRelationshipExists
from utils import getGraph, save_file
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
                                  "volunteers_goal_num": idea_dict.get('volunteers_goal_num'),
                                  "if_author_public": idea_dict.get('if_author_public')})
    newidea.add_labels("idea")
    _addIdeaToIndex(newidea_index, newidea)
    getGraph().create((user, "CREATED", newidea, {"timestamp":timestamp}))
    # first receivers
    first_receivers = map(_get_participant_node, idea_dict.get('first_receivers_emails'))
    for participant in first_receivers:
        getGraph().create((newidea, "GOES_FIRST_TO", participant))
    #
    return jsonify({"result":"OK", "result_msg":"added idea to database"})


# Used By < modify_idea >
def modify_idea_aux(idea_dict,ideapic_file_body):
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


# <Used by do_cron_tasks_aux>, <redflag_idea_aux>
def remove_idea_aux(idea_index) :
    idea = _getIdeaByIdeaIndex(idea_index)
    for rel in getGraph().match(start_node=idea, bidirectional=True):
        rel.delete()
    idea.delete()
    return jsonify({"result":"OK", "result_msg":"Idea was removed"})

def get_ideas_created_by_participant_aux(participant_email, user_email):
    user = _get_participant_node(user_email)
    participant = _get_participant_node(participant_email)
    ifpublicprofile = participant['ifpublicprofile']
    if user_email == participant_email or _getIfContactRelationshipExists(participant, user) is True \
            or ifpublicprofile is True:
        ifallowed = True
        response = _get_ideas_created_by_participant(participant_email)
        response['ifallowed'] = ifallowed
        return jsonify(response)
    else:
        ifallowed = False
    return jsonify({"result": "OK", "ifallowed": ifallowed})


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
    author_photo_url = _get_participant_node(author_email)['profilepic_url']
    author_username = _get_participant_node(author_email)['username']
    idea_proposal = idea['proposal']
    uuid=idea['uuid']
    timestamp = datetime.strptime(getGraph().match_one(end_node=idea, rel_type="CREATED")["timestamp"], '%d.%m.%Y')
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


# <used by get_idea_data_aux> [0]->supporters, [1]->rejectors, [2]->passives, [3]->volunteers
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
        if vote_rel["ifvolunteered"] == True:
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
    volunteer_rels = [x for x in vote_rels if x["ifvolunteered"] == True]
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


def get_voting_rel_between_user_and_idea_aux(user_email, idea_proposal):
    user = _get_participant_node(user_email)
    idea = _getIdeaByIdeaIndex(idea_proposal)
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
    idea = _getIdeaByIdeaIndex(idea_index)
    vote_type=inputdict['vote_type']
    vote_ifvolunteered=inputdict['vote_ifvolunteered']
    vote_timestamp=(datetime.now()).strftime("%d.%m.%Y")
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
    # TODO: further condition for failure warning, it should not be re-fired before two days from the previous one.
    if support_rate < SUPPORT_RATE_MIN and if_previous_support_rate_OK is True:
        _do_tasks_for_idea_failurewarning(idea_index)
    if supporters_num >= (idea['supporters_goal_num']) and volunteers_num >= (idea['supporters_goal_num']):
        _do_tasks_for_idea_successful(idea_index)
    return response

def redflag_idea_aux(user_email, idea_index, reason):
    user = _get_participant_node(user_email)
    idea = _getIdeaByIdeaIndex(idea_index)
    if (_get_vote_statistics_for_idea(idea_index)[0]) > 0:
        _send_notification_emails_from_idea_to_supporters(idea_index, 'redflag', reason, user['fullname'])
    _send_notification_email_from_idea_to_author(idea_index, 'redflag', reason, user['fullname'])
    return remove_idea_aux(idea_index)

####################
#  PURE INTERNAL
###################


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


# <Used by get_ideas_created_by_participant_aux, _get_participant_data_by_email>
def _get_ideas_created_by_participant(participant_email):
    participant = _get_participant_node(participant_email)
    ideas_indices=[]
    ideas=[x.end_node for x in list(getGraph().match(start_node=participant, rel_type="CREATED"))]
    for idea in ideas:
        idea_index=idea['proposal']
        ideas_indices.append(idea_index)
    return {'result': 'OK', 'ideas_indices': ideas_indices}


def _get_ideas_data_created_by_participant(participant_email):
    participant = _get_participant_node(participant_email)
    ideas_data = []
    rels = list(getGraph().match(start_node=participant, rel_type="CREATED"))
    for rel in rels:
        idea_data = get_idea_data_aux(rel.end_node)
        ideas_data.append(idea_data)
    return {'result': 'OK', 'ideas_data': ideas_data}


def _if_ideaisinfirstphase(idea):
    # if (one day has passed since creation of the idea) then False
    # datetime_now = ((datetime.now()).strftime("%d.%m.%Y"))
    datetime_ideacreation = datetime.strptime(getGraph().match_one(rel_type="CREATED", end_node=idea)["timestamp"], '%d.%m.%Y')
    if ((datetime.now()) - datetime_ideacreation).days >= 1:
        return False
    # if (any of the first receivers has not voted) then True
    idea_first_receivers = [x.end_node for x in list(getGraph().match(start_node=idea, rel_type="GOES_FIRST_TO"))]
    for idea_first_receiver in idea_first_receivers:
        if getGraph().match_one(start_node=idea_first_receiver, rel_type="HAS_VOTED_ON", end_node=idea) is None:
            return True
    # else False
    return True


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
# from ideaManager import _getIdeaByIdeaIndex, _get_supporters_emails_for_idea_aux, _get_volunteers_emails_for_idea_aux
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
    idea = _getIdeaByIdeaIndex(proposal_index)
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
    idea=_getIdeaByIdeaIndex(idea_index)
    idea['if_editedproposal'] = True
    idea['if_editedproposal_timestamp'] = ((datetime.now()).strftime("%d.%m.%Y"))
    _add_notifications_from_idea_to_supporters(idea_index, 'edited')
    _send_notification_emails_from_idea_to_supporters(idea_index, 'edited')
    return


# <used by vote_on_idea_aux>
def _do_tasks_for_idea_failurewarning(idea_index):
    idea=_getIdeaByIdeaIndex(idea_index)
    idea['if_failurewarning'] = True
    idea['if_failurewarning_timestamp'] = ((datetime.now()).strftime("%d.%m.%Y"))
    _add_notification_relationship_from_idea_to_author(idea_index, 'failurewarning')
    _send_notification_email_from_idea_to_author(idea_index, 'failurewarning')
    return


# <used by vote_on_idea_aux>
def _do_tasks_for_idea_successful(idea_index):
    idea=_getIdeaByIdeaIndex(idea_index)
    idea['if_successful'] = True
    idea['if_successful_timestamp'] = ((datetime.now()).strftime("%d.%m.%Y"))
    _add_notifications_from_idea_to_supporters(idea_index, 'successful')
    _add_notification_relationship_from_idea_to_author(idea_index, 'successful_to_author')
    _send_notification_emails_from_idea_to_supporters(idea_index, 'successful')
    _send_notification_email_from_idea_to_author(idea_index, 'successful_to_author')
    return


# <used by _do_tasks_for_idea_editedproposal, _do_tasks_for_idea_failurewarning, _do_tasks_for_idea_successful>
#  notification_type_possibilities = ['editedproposal', 'successful']
def _add_notifications_from_idea_to_supporters(idea_index, notification_type):
    notification_field_str = 'ifnotification_' + notification_type
    idea = _getIdeaByIdeaIndex(idea_index)
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    support_rels = [x for x in vote_rels if x["type"] == "supported"]
    for support_rel in support_rels:
        support_rel[notification_field_str] = True
    return


# <used by _do_tasks_for_idea_editedproposal, _do_tasks_for_idea_failurewarning, _do_tasks_for_idea_successful>
def _send_notification_emails_from_idea_to_supporters(idea_index, notification_type, reason = None, participant_fullname = None):
    idea = _getIdeaByIdeaIndex(idea_index)
    subject = "Consensus, New Notifications"
    if notification_type == 'edited':
        html = render_template('emails/idea_edited.html', msg_proposal=idea['proposal'])
    elif notification_type == 'successful':
        html = render_template('emails/idea_successful.html', msg_proposal=idea['proposal'])
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
def _add_notification_relationship_from_idea_to_author(idea_index, notification_type):
    notification_field_str = 'ifnotification_' + notification_type
    idea = _getIdeaByIdeaIndex(idea_index)
    author_rel = getGraph().match_one(rel_type="CREATED", end_node=idea)
    author_rel[notification_field_str] = True
    return


# <used by _do_tasks_for_idea_failurewarning, _do_tasks_for_idea_successful>
def _send_notification_email_from_idea_to_author(idea_index, notification_type, reason = None, participant_fullname = None):
    idea=_getIdeaByIdeaIndex(idea_index)
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
