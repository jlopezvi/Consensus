from py2neo import neo4j
from participantManager import _get_participant_node, _getIfContactRelationshipExists
from utils import getGraph, save_file, send_email
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
        do_tasks_for_idea_edited(idea_index)
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
    author_email = getGraph().match_one(end_node=idea, rel_type="CREATED").start_node.get_properties()['email']
    author_photo_url = _get_participant_node(author_email)['image_url']
    author_username = _get_participant_node(author_email)['username']
    uuid=idea['uuid']
    timestamp = datetime.strptime(idea['timestamp'], '%d.%m.%Y')
    duration = str((datetime.now() - timestamp).days) + ' days'
    #voters_num = len(list(getGraph().match(end_node=idea, rel_type="VOTED_ON")))
    supporters_num = _get_vote_statistics_for_idea(idea)[0]
    rejectors_num = _get_vote_statistics_for_idea(idea)[1]
    active_voters_num = supporters_num + rejectors_num
    volunteers_num=_get_vote_statistics_for_idea(idea)[2]
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
def _get_vote_statistics_for_idea(node_idea):
   rejectors_num=0
   supporters_num=0
   volunteers_num=0
   for vote_rel in (list(getGraph().match(end_node=node_idea, rel_type="VOTED_ON"))):
       if vote_rel["type"] == "supported":
           supporters_num+=1
       elif vote_rel["type"] == "rejected":
           rejectors_num+=1
       if vote_rel["volunteered"] == True:
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
    from app import SUPPORT_RATE_MIN
    user = _get_participant_node(user_email)
    idea_index=inputdict['idea_proposal']
    idea = _getIdeaByIdeaIndex(idea_index)
    vote_type=inputdict['vote_type']
    vote_ifvolunteered=inputdict['vote_ifvolunteered']
    vote_timestamp=(datetime.now()).strftime("%d.%m.%Y")
    supporters_num= _get_vote_statistics_for_idea(idea)[0]
    voters_num = len(list(getGraph().match(end_node=idea, rel_type="VOTED_ON")))
    if voters_num == 0:
        support_rate = 100
    else:
        support_rate = (supporters_num / voters_num)*100
    if support_rate < SUPPORT_RATE_MIN:
        support = False
    else:
        support = True
    if if_voting_relationship_exists(user,idea):
        if if_voting_relationship_exists_of_given_type(user, idea, vote_type, vote_ifvolunteered):
            return jsonify({'result':'Wrong: User vote exists'})
        else:
            response = create_or_modify_voting_relationship_to_given_type(user, idea, vote_type, vote_ifvolunteered, vote_timestamp)
            supporters_num= _get_vote_statistics_for_idea(idea)[0]
            volunteers_num=_get_vote_statistics_for_idea(idea)[2]
            support_rate = (supporters_num / voters_num)*100
            print (support_rate)
            if support_rate < SUPPORT_RATE_MIN and support == True:
                do_tasks_for_idea_failurewarning(idea_index)
            if supporters_num >= (idea['supporters_goal_num']) and volunteers_num >= (idea['supporters_goal_num']):
                do_tasks_for_idea_successful(idea_index)
            return response
    else:
        response = create_or_modify_voting_relationship_to_given_type(user, idea, vote_type, vote_ifvolunteered, vote_timestamp)
        supporters_num= _get_vote_statistics_for_idea(idea)[0]
        volunteers_num=_get_vote_statistics_for_idea(idea)[2]
        support_rate = (supporters_num / voters_num)*100 if voters_num is not 0 else 100
        if support_rate < SUPPORT_RATE_MIN and support == True:
            do_tasks_for_idea_failurewarning(idea_index)
        if supporters_num >= (idea['supporters_goal_num']) and volunteers_num >= (idea['supporters_goal_num']):
            do_tasks_for_idea_successful(idea_index)
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


def create_notification_relationships_to_supporters(idea, notification_type):
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    support_rels = [x for x in vote_rels if x["type"] == "supported"]
    supporters = [x.start_node for x in support_rels]
    for supporter in supporters:
        NotificationRelationshipFound = getGraph().match_one(start_node=idea, rel_type="HAS_NOTIFICATION_FOR",
                                                             end_node=supporter)
        if NotificationRelationshipFound is None:
            getGraph().create((idea, "HAS_NOTIFICATION_FOR", supporter, {"type": notification_type}))
        else:
            NotificationRelationshipFound["type"] = notification_type
    return


def send_notification_emails_to_supporters(idea, notification_type):
    subject = "Consensus, New Notifications"
    if notification_type == 'edited':
        html = render_template('idea_edited.html', msg_proposal=idea['proposal'])
    else:
        html = render_template('idea_successful.html', msg_proposal=idea['proposal'])
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    support_rels = [x for x in vote_rels if x["type"] == "supported"]
    supporters = [x.start_node for x in support_rels]
    for supporter in supporters:
        send_email(supporter['email'], subject, html)
    return


def create_notification_relationship_to_author(idea, notification_type):
    author = getGraph().match_one(rel_type="CREATED", end_node=idea).start_node
    NotificationRelationshipFound = getGraph().match_one(start_node=idea, rel_type="HAS_NOTIFICATION_FOR", end_node=author)
    if NotificationRelationshipFound is None:
        getGraph().create((idea, "HAS_NOTIFICATION_FOR", author, {"type":notification_type}))
    else:
        NotificationRelationshipFound["type"] = notification_type
    return


def send_notification_email_to_author(idea, notification_type):
    author = getGraph().match_one(rel_type="CREATED", end_node=idea).start_node
    subject = "Consensus, New Notifications"
    if notification_type == 'failurewarning':
        html = render_template('idea_failurewarning.html', msg_proposal=idea['proposal'])
    else:
        html = render_template('idea_successful.html', msg_proposal=idea['proposal'])
    send_email(author['email'], subject, html)
    return


def do_tasks_for_idea_edited(idea_index):
    idea=_getIdeaByIdeaIndex(idea_index)
    idea['if_proposal_edited'] = True
    idea['if_proposal_edited_timestamp'] = ((datetime.now()).strftime("%d.%m.%Y"))
    create_notification_relationships_to_supporters(idea, 'edited')
    send_notification_emails_to_supporters(idea, 'edited')
    return


def do_tasks_for_idea_failurewarning(idea_index):
    idea=_getIdeaByIdeaIndex(idea_index)
    idea['failurewarning'] = True
    idea['if_failurewarning_timestamp'] = ((datetime.now()).strftime("%d.%m.%Y"))
    create_notification_relationship_to_author(idea, 'failurewarning')
    send_notification_email_to_author(idea,'failurewarning')
    return


def do_tasks_for_idea_successful(idea_index):
    idea=_getIdeaByIdeaIndex(idea_index)
    idea['if_successful'] = True
    idea['if_successful_timestamp'] = ((datetime.now()).strftime("%d.%m.%Y"))
    create_notification_relationships_to_supporters(idea, 'successful')
    create_notification_relationship_to_author(idea, 'successful_to_author')
    send_notification_emails_to_supporters(idea, 'successful')
    send_notification_email_to_author(idea,'successful_to_author')
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
