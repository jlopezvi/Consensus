from py2neo import neo4j
from flask import jsonify, abort, redirect,url_for, render_template
import ast
import json
import logging
from utils import getGraph, save_file, send_email
from uuid_token import generate_confirmation_token
import datetime
from user_authentification import User
import flask_login


# input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'IT', 'password': 'MD5password',
#              'host_email': 'asdf@das' / None, 'ifpublicprofile': True/ False,
#              'ifregistrationfromemail': True / False}
#        (file) profilepic_file_body
# output: json
#          1. Wrong  -->   {"result":"Wrong","ifemailexists":true,"ifemailexists_msg":ifemailexists_msg[true]}
#          2. OK (registered participant but e-mail not verified yet. Sends new e-mail for verification)  -->
#                       {"result":"OK","ifemailexists":true,"ifemailexists_msg":ifemailexists_msg[true],
#                        "ifemailverified":false,"ifemailverified_msg":ifemailverified_msg[false]}
#          3. OK (4 different normal cases of registration)
#                       {"result":"OK", "ifhost":true/false,"ifhost_msg":ifhost_msg[ifhost],
#                       "ifemailverified":true/false,"ifemailverified_msg":ifemailverified_msg[email_verified]})
def registration_aux(inputdict, profilepic_file_body):
    email = inputdict.get('email')
    ifemailverified_msg= ["E-mail not verified. E-mail verification sent. " \
                          "Close this window and check your e-mail within the next few minutes ", None]
    ifhost_msg=[None, "You will be following your host in Consensus"]
    if _get_participant_node(email, 'all'):   # email exists? (Exceptional cases of registration)
        ifemailexists = True
        ifemailexists_msg = "Participant already exists"
        if _get_participant_node(email):   # participant's email is verified?
            ifemailverified=True
            return jsonify({"result":"Wrong","ifemailexists":ifemailexists,"ifemailexists_msg":ifemailexists_msg})
        else:
            ifemailverified = False
            result_send_emailverification = _registration_send_emailverification(email)
            if result_send_emailverification is "OK":
                return jsonify({"result": "OK: Participant registered previously, resend email verification",
                                "ifemailexists": ifemailexists, "ifemailexists_msg":ifemailexists_msg,
                                "ifemailverified": ifemailverified, "ifemailverified_msg": ifemailverified_msg[ifemailverified]})
            else:
                raise NameError('PROBLEM')
    # (Normal cases of registration)
    # save data for new (verified / unverified) participant in database
    ifemailverified = inputdict.get('ifregistrationfromemail')
    _newParticipant(inputdict, profilepic_file_body)
    if ifemailverified is True:
        user = User(email)
        flask_login.login_user(user)
    else:
        result_send_emailverification2 = _registration_send_emailverification(email)
        if result_send_emailverification2 is "OK":
            pass
        else:
            raise NameError('PROBLEM')
    ifhost = False
    if inputdict.get('host_email') is not None:
        # current_participant (verified/unverified) follows host
        ifhost = _if_added_following_contact_to_user(inputdict.get('host_email'), email)
    return jsonify({"result": "OK", "ifhost": ifhost, "ifhost_msg": ifhost_msg[ifhost],
                    "ifemailverified": ifemailverified, "ifemailverified_msg": ifemailverified_msg[ifemailverified]})


# Used By <registration_aux>
# input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'Human Resources', 'password': 'MD5password',
#              'ifregistrationfromemail': True / False, 'ifpublicprofile': True / False,}
#       profilepic_file_body: None/ (file)
# output: python dict {'result':'OK'}
def _newParticipant(participantdict,profilepic_file_body):
    image_url = '/static/assets/profile/perfil-mediano.png'
    email = participantdict.get('email')
    if profilepic_file_body is not None:
        ruta_dest = '/static/assets/profile/'
        filename=str(email)+'.png'
        image_url = save_file(ruta_dest, profilepic_file_body, filename)
    newparticipant, = getGraph().create({"fullname" : participantdict.get('fullname'), "email" : email,
                                  "username" : participantdict.get('username'), "position" : participantdict.get('position'),
                                  "group" : participantdict.get('group'), "password" : participantdict.get('password'),
                                  "ifpublicprofile" : participantdict.get('ifpublicprofile'),
                                  "profilepic_url" : image_url, "ifsupportingproposalsvisible" : True,
                                  "ifrejectingproposalsvisible": True
                                  })
    if participantdict.get('ifregistrationfromemail') is True:
        newparticipant.add_labels("participant")
        _addToParticipantsIndex(email, newparticipant)
    elif participantdict.get('ifregistrationfromemail') is False:
        newparticipant.add_labels("unverified_participant")
        _addToUnverifiedParticipantsIndex(email, newparticipant)
    return {'result': 'OK'}


def modify_user_data_aux(user_data, profilepic_file_body, user_email):
    participant = _get_participant_node(user_email)
    fields = ['email', 'position', 'group', 'password', 'ifsupportingproposalsvisible',
              'ifrejectingproposalsvisible',
              'username', 'ifpublicprofile', 'fullname']
    data = {}
    if 'new_email' in user_data:
        new_email=user_data['new_email']
        if _get_participant_node(new_email, 'all'):  # email exists?
            return jsonify({'result': 'Wrong: New e-mail already exists'})
        _removeFromParticipantsIndex(user_email, participant)
        _addToParticipantsIndex(new_email, participant)
        user_email = new_email
    for k, v in user_data.items():
        if k in fields:
            data[k] = v
    for k, v in data.items():
        participant[k] = v
    if profilepic_file_body is not None:
        ruta_dest = '/static/assets/profile/'
        filename = str(user_email) + '.png'
        image_url = save_file(ruta_dest, profilepic_file_body, filename)
        participant["profilepic_url"] = image_url
    return jsonify({'result': 'OK'})


def remove_user_aux(user_email) :
    user = _get_participant_node(user_email, 'all')
    created_ideas = [x.end_node for x in list(getGraph().match(start_node=user, rel_type="CREATED"))]
    for created_idea in created_ideas:
        for rel in getGraph().match(start_node=created_idea, bidirectional=True):
            rel.delete()
        created_idea.delete()
    for rel2 in getGraph().match(start_node=user, bidirectional=True):
        rel2.delete()
    user.delete()
    return jsonify({'result': 'OK'})


def get_participant_data_aux(currentuser_email, participant_email):
    from ideaManager import get_ideas_data_created_by_participant_aux
    currentuser = _get_participant_node(currentuser_email)
    participant = _get_participant_node(participant_email)
    ifpublicprofile = participant.get_properties()['ifpublicprofile']
    participant_data= {}
    if participant_email == currentuser_email or _getIfContactRelationshipExists(participant, currentuser) is True \
            or ifpublicprofile is True:
        ifallowed = True
        profilepic_url = participant.get_properties()['profilepic_url']
        username = participant.get_properties()['username']
        fullname = participant.get_properties()['fullname']
        followers_num = len(_get_participant_followers(participant_email))
        followings_num = len(_get_participant_followings(participant_email))
        ideas_num = len(get_ideas_data_created_by_participant_aux(participant_email))
        participant_data.update({'id': participant_email,'profilepic_url': profilepic_url,
                                 'username' : username, 'fullname': fullname,
                                 'ideas_num' : ideas_num,
                                 'followers_num': followers_num,
                                 'followings_num': followings_num})
    else:
        ifallowed = False
    return jsonify({"result":"OK", 'ifallowed': ifallowed, "participant_data": participant_data})


def get_participant_data_by_email_unrestricted_aux(participant_email):
    return jsonify(_get_participant_data_by_email(participant_email))


def if_participant_exists_by_email_aux(participant_email):
    if _get_participant_node(participant_email, 'all'):
        return jsonify({"result": True})
    return jsonify({"result": False})


def get_fullname_for_participant_aux(participant_email, user_email):
    user=_get_participant_node(user_email)
    participant = _get_participant_node(participant_email)
    ifpublicprofile = participant.get_properties()['ifpublicprofile']
    fullname=None
    if participant_email == user_email or _getIfContactRelationshipExists(participant, user) is True \
            or ifpublicprofile is True:
        ifallowed = True
        fullname=participant["fullname"]
    else:
        ifallowed = False
    return jsonify({"result": "OK", "ifallowed": ifallowed, "fullname": fullname})


def get_participant_followings_info_aux(participant_email, user_email):
    user = _get_participant_node(user_email)
    participant = _get_participant_node(participant_email)
    ifpublicprofile = participant['ifpublicprofile']
    followings_info = []
    if (participant_email == user_email) or (_getIfContactRelationshipExists(participant, user) is True) \
            or (ifpublicprofile is True):
        ifallowed = True
        followings = _get_participant_followings(participant_email)
        followings_num = len(followings)
        for following in followings:
            email = following['email']
            username = following['username']
            fullname = following['fullname']
            profilepic_url = following['profilepic_url']
            followings_info.append({'email': email, 'username': username, 'fullname': fullname, 'profilepic_url': profilepic_url})
    else:
        ifallowed = False
        followings = _get_participant_followings(participant_email)
        followings_num = len(followings)
    return jsonify({"result":"OK", "ifallowed": ifallowed, "followings_num": followings_num, "followings_info": followings_info})


def get_participant_followers_info_aux(participant_email, user_email):
    user = _get_participant_node(user_email)
    participant = _get_participant_node(participant_email)
    ifpublicprofile = participant['ifpublicprofile']
    followers_info = []
    if (participant_email == user_email) or (_getIfContactRelationshipExists(participant, user) is True) \
            or (ifpublicprofile is True):
        ifallowed = True
        followers = _get_participant_followers(participant_email)
        followers_num = len(followers)
        for follower in followers:
            email = follower['email']
            username = follower['username']
            fullname = follower['fullname']
            profilepic_url = follower['profilepic_url']
            followers_info.append({'email' : email, 'username': username, 'fullname': fullname, 'profilepic_url': profilepic_url})
    else:
        ifallowed = False
        followers = _get_participant_followers(participant_email)
        followers_num = len(followers)
    return jsonify({"result":"OK", "ifallowed": ifallowed, "followers_num": followers_num, "followers_info": followers_info})


def add_following_contact_to_user_aux(followingcontact_email, user_email):
    result = _if_added_following_contact_to_user(followingcontact_email, user_email)
    if result is True:
        _add_newfollower_notification_from_participant1_to_participant2(user_email, followingcontact_email)
        return jsonify({"result": "OK", "result_msg": "Following contact was added"})
    else:
        return jsonify({"result": "Wrong", "result_msg": "Following contact not possible or exists already"})


def remove_following_contact_to_user_aux(followingcontact_email, user_email):
    result = _if_removed_following_contact_to_user(followingcontact_email, user_email)
    if result is True:
        return jsonify({"result": "OK", "result_msg": "Following contact was removed"})
    else:
        return jsonify({"result": "Wrong", "result_msg": "Following contact does not exist"})

# NOT TESTED
def get_all_participants_aux():
    allnodes = _getParticipantsIndex().query("email:*")
    participants = []
    for node in allnodes:
        participants.append(node.get_properties())
    return participants

def get_all_public_participants_for_user_aux(user):
    participant = _get_participant_node(user)
    allnodes = _getParticipantsIndex().query("email:*")
    participants = []
    for node in allnodes:
        if node.get_properties()['ifpublicprofile'] == True and node.get_properties()['email'] != user:
            participants.append(
                {'email': node.get_properties()['email'], 'fullname': node.get_properties()['fullname'],
                 'position': node.get_properties()['position'], 'group': node.get_properties()['group'],
                 'profilepic_url': node.get_properties()['profilepic_url'],
                 'if_following': _getIfContactRelationshipExists(participant, node)})
    return participants


###############################################

# <USED BY MANY FUNCTIONS>
def _addToParticipantsIndex(email, newparticipant) :
     getGraph().get_or_create_index(neo4j.Node, "Participants").add("email", email, newparticipant)
def _addToUnverifiedParticipantsIndex(email, newparticipant):
    getGraph().get_or_create_index(neo4j.Node, "UnverifiedParticipants").add("email", email, newparticipant)
def _removeFromParticipantsIndex(email, participant):
    getGraph().get_or_create_index(neo4j.Node, "Participants").remove("email", email, participant)
def _removeFromUnverifiedParticipantsIndex(email, participant):
    getGraph().get_or_create_index(neo4j.Node, "UnverifiedParticipants").remove("email", email, participant)
def _getParticipantsIndex():
    return getGraph().get_or_create_index(neo4j.Node, "Participants")
def _getUnverifiedParticipantsIndex():
    return getGraph().get_or_create_index(neo4j.Node, "UnverifiedParticipants")


# <USED BY MANY FUNCTIONS>
#input: email, ifemailverified_category ('all'/True/False)
#output:
#  -> participant_node
#  -> None
#TODO: participantFound[0] is a node or a dictionary?
def _get_participant_node(email, ifemailverified_category=True) :
    if ifemailverified_category in ('all', True):
        participantFound = _getParticipantsIndex().get("email", email)
        if participantFound:
            return participantFound[0]  # node
    if ifemailverified_category in ('all', False):
        unverifiedparticipantFound = _getUnverifiedParticipantsIndex().get("email", email)
        if unverifiedparticipantFound :
            return unverifiedparticipantFound[0] #node
    else:
        return None


# follower, following are participant nodes
def _getIfContactRelationshipExists(follower, following):
    contact_relationship_found = getGraph().match_one(start_node=follower, end_node=following, rel_type="FOLLOWS")
    if contact_relationship_found is not None:
        return True
    return False


# Used By <registration_aux>
# input: email to be verified as an argument
# output: e-mail to the email account with a URL token link for email verification
#         and returns "OK"
def _registration_send_emailverification(email):
    token = generate_confirmation_token(email)
    confirm_url = url_for('.registration_receive_emailverification', token=token, _external=True)
    html = render_template('login/verification_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(email, subject, html)
    return "OK"


# <used by registration_send_invitation>
def _get_fullname_for_participant(participant_email):
    participant = _get_participant_node(participant_email)
    fullname = participant["fullname"]
    return fullname


# input: participant_email
# output: list of nodes of following contacts
def _get_participant_followings(participant_email) :
    participant = _get_participant_node(participant_email)
    rels = list(getGraph().match(start_node=participant, rel_type="FOLLOWS"))
    followings = []
    for rel in rels:
        followings.append(rel.end_node)
    return followings


# input: participant_email
# output: list of nodes of follower contacts
def _get_participant_followers(participant_email) :
    participant = _get_participant_node(participant_email)
    rels = list(getGraph().match(end_node=participant, rel_type="FOLLOWS"))
    followers = []
    for rel in rels:
        followers.append(rel.start_node)
    return followers


# <USED BY: add_following_contact_to_user_aux(), registration_aux()>
# input: user email, new following contact email
# output:
#   ->  True
#   ->  False
#   ->  [False,'Following contact exists already']
def _if_added_following_contact_to_user(followingcontact_email, user_email) :
    user = _get_participant_node(user_email, 'all')  # current's email could be unverified
    followingcontact = _get_participant_node(followingcontact_email)
    if (followingcontact is None) or (followingcontact is user) :
        return False
    if _getIfContactRelationshipExists(user, followingcontact) is True:
        return [False,'Following contact exists already']
    getGraph().create((user, "FOLLOWS", followingcontact))
    return True


# <USED BY: remove_following_contact_to_user_aux()>
# input: user email, following contact email
# output:
#   ->  True
#   ->  False
def _if_removed_following_contact_to_user(followingcontact_email, user_email) :
    user = _get_participant_node(user_email, 'all')  # current's email could be unverified
    followingcontact = _get_participant_node(followingcontact_email)
    if _getIfContactRelationshipExists(user, followingcontact) is True:
        contact_rel = getGraph().match_one(start_node=user, rel_type="FOLLOWS", end_node=followingcontact)
        getGraph().delete(contact_rel)
        return True
    return False



# <Used by /get_participant_data_by_email_unrestricted>
def _get_participant_data_by_email(participant_email):
    from ideaManager import _get_ideas_created_by_participant
    participant = _get_participant_node(participant_email)
    participant_data= {}
    profilepic_url = participant['profilepic_url']
    username = participant['username']
    fullname = participant['fullname']
    followers_num = len(_get_participant_followers(participant_email))
    followings_num = len(_get_participant_followings(participant_email))
    ideas_num = len(_get_ideas_created_by_participant(participant_email)['ideas_indices'])
    participant_data.update({'id': participant_email,'profilepic_url': profilepic_url,
                             'username': username, 'fullname': fullname,
                             'ideas_num': ideas_num,
                             'followers_num': followers_num,
                             'followings_num': followings_num})
    return {"result": "OK", "participant_data": participant_data}




####################

####################
#  NOTIFICATIONS
###################

####################
from utils import send_email


def get_participantnotifications_for_user_aux(user_email):
    user = _get_participant_node(user_email)
    notifications = []
    current_notification = {}
    # notifications from new followers
    follower_rels = list(getGraph().match(end_node=user, rel_type="FOLLOWS"))
    for follower_rel in follower_rels:
        if follower_rel["ifnotification_newfollower"] is True:
            current_notification.update({'notification_type': 'newfollower' ,
                                         'participant_index': follower_rel.start_node['email']})
            notifications.append(current_notification)
    #
    return jsonify({"result": "OK", "data": notifications})


# Used By <remove_notification_to_participant>
def remove_notification_from_participant1_to_participant2_aux(participant1_index, participant2_index, notification_type):
    participant_sender = _get_participant_node(participant1_index)
    participant_receiver = _get_participant_node(participant2_index)
    notification_field_str = 'ifnotification_' + notification_type
    # remove notification from new followers
    follower_rel_found = getGraph().match_one(start_node=participant_sender, end_node= participant_receiver,
                                              rel_type="FOLLOWS")
    if follower_rel_found[notification_field_str] is not None:
        follower_rel_found[notification_field_str] = False
    #
    return jsonify({"result": "OK", "result_msg": "Notification was deleted"})


####################
#  PURE INTERNAL
###################


# <Used by add_following_contact_to_user_aux>
# "notification_type": "newfollower"
def _add_newfollower_notification_from_participant1_to_participant2(participant1_email, participant2_email):
    participant1 = _get_participant_node(participant1_email)
    participant2 = _get_participant_node(participant2_email)
    following_rel = getGraph().match_one(start_node=participant1, rel_type="FOLLOWS", end_node=participant2)
    following_rel["ifnotification_newfollower"] = True
    return


# <Used by add_following_contact_to_user_aux>
# "notification_type": "newfollower"
def _send_newfollower_notification_email_from_participant1_to_participant2(participant1_email, participant2_email):
    participant1 = _get_participant_node(participant1_email)
    subject = "Consensus, New Notifications"
    html = render_template('emails/participant_newfollower.html', msg_proposal=participant1['fullname'])
    send_email(participant2_email, subject, html)
    return