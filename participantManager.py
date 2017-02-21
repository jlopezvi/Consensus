from py2neo import neo4j
from flask import jsonify,abort, redirect,url_for, render_template
import ast
import json
import logging
from utils import getGraph, send_email, save_file
from uuid_token import generate_confirmation_token
import datetime
from user_authentification import User
import flask_login


# TODO: change 'True', 'False', 'None' to True, False, None when calling this function to have a real Python dictionary
# input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'IT', 'password': 'MD5password',
#              'host_email': 'asdf@das' / 'None', 'ifpublicprofile': 'True'/ 'False',
#              'ifregistrationfromemail': 'True' / 'False'}
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
    if _getParticipantByEmail(email,'all'):   # email exists? (Exceptional cases of registration)
        ifemailexists = True
        ifemailexists_msg = "Participant already exists"
        if _getParticipantByEmail(email):   # participant's email is verified?
            ifemailverified=True
            return jsonify({"result":"Wrong","ifemailexists":ifemailexists,"ifemailexists_msg":ifemailexists_msg})
        else:
            ifemailverified=False
            result_send_emailverification = _registration_send_emailverification(email)
            if result_send_emailverification is "OK" :
                return jsonify({"result": "OK", "ifemailexists": ifemailexists, "ifemailexists_msg":ifemailexists_msg,
                                "ifemailverified": ifemailverified, "ifemailverified_msg": ifemailverified_msg[ifemailverified]})
    # (Normal cases of registration)
    # save data for new (verified / unverified) participant in database
    ifemailverified = inputdict.get('ifregistrationfromemail')
    _newParticipant(inputdict, profilepic_file_body)
    if ifemailverified =='True':
        email_verified = True
        user = User(email)
        flask_login.login_user(user)
    else:
        email_verified = False
        _registration_send_emailverification(email)
    ifhost = False
    if inputdict.get('host_email') != 'None':
        # current_participant (verified/unverified) follows host
        ifhost = add_following_contact_to_participant_aux(email, inputdict.get('host_email'))
    return jsonify({"result":"OK", "ifhost":ifhost, "ifhost_msg":ifhost_msg[ifhost],
                    "ifemailverified":email_verified, "ifemailverified_msg":ifemailverified_msg[email_verified]})


#Used By <registration_aux>
#input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'Human Resources', 'password': 'MD5password',
#              'ifregistrationfromemail': 'True' / 'False', 'ifpublicprofile': 'True' / 'False',}
#       profilepic_file_body: None/ (file)
#output: python dict {'result':'OK'}
def _newParticipant(participantdict,profilepic_file_body):
    image_url = 'static/assets/profile/perfil-mediano.png'
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
    if participantdict.get('ifregistrationfromemail')=='True':
        newparticipant.add_labels("participant")
        _addToParticipantsIndex(email, newparticipant)
    elif participantdict.get('ifregistrationfromemail')== 'False':
        newparticipant.add_labels("unverified_participant")
        _addToUnverifiedParticipantsIndex(email, newparticipant)
    return {'result' : 'OK'}

#Used By <registration_aux>
# input: email to be verified as an argument
# output: e-mail to the email account with a URL token link for email verification
#         and json {"result": "OK", "result_msg":"email sent"}
def _registration_send_emailverification(email):
    token = generate_confirmation_token(email)
    confirm_url = url_for('.registration_receive_emailverification', token=token, _external=True)
    html = render_template('login/verification_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(email, subject, html)
    return jsonify({"result": "OK", "result_msg":"email sent"})


#input: email
#output: python dictionary
#  -> {'result': 'email already confirmed'}
#  -> {'result': 'email not registered'}
#  -> {'result': 'OK'}
def _verifyEmail(email):
    unverifiedparticipant = _getParticipantByEmail(email,False)
    if unverifiedparticipant is None:
       if _getParticipantByEmail(email,True):
           return {'result': 'email already confirmed'}
       else:
           return {'result': 'email not registered'}
    else:
        _removeFromUnverifiedParticipantsIndex(email, unverifiedparticipant)
        _addToParticipantsIndex(email, unverifiedparticipant)
        unverifiedparticipant.remove_labels("unverified_participant")
        unverifiedparticipant.add_labels("participant")
        #TODO datestamp for registration
        #registered_on=datetime.datetime.now()
        return {'result': 'OK'}


#NOT USED
def deleteParticipant(email) :
    participantFound = _getParticipantByEmail(email,'all')
    participantFound.delete()

#NOT USED
def getAllParticipants():
    allnodes = _getParticipantsIndex().query("email:*")
    participants = []
    for node in allnodes:
         participants.append(node.get_properties())
    return participants

def _getParticipantsIndex():
    return getGraph().get_or_create_index(neo4j.Node, "Participants")
def _getUnverifiedParticipantsIndex():
    return getGraph().get_or_create_index(neo4j.Node, "UnverifiedParticipants")

#input: email, ifemailverified_category ('all'/True/False)
#output:
#  -> participant_node
#  -> None
#TODO: participantFound[0] is a node or a dictionary?
def _getParticipantByEmail(email, ifemailverified_category=True) :
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

# def _getUnverifiedParticipantByEmail(email) :
#     participantFound = _getUnverifiedParticipantsIndex().get("email", email)
#     if participantFound :
#          return participantFound[0]
#     return None

def getFullNameByEmail_aux(email):
    if _getParticipantByEmail(email):
        fullname=_getParticipantByEmail(email)["fullname"]
        return fullname
    return None

#currentParticipant, newFollowingContact are graph nodes
def _getIfContactRelationshipExists(currentParticipant, newFollowingContact) :
    contactRelationshipFound = getGraph().match_one(start_node=currentParticipant, end_node=newFollowingContact,
                                                rel_type="FOLLOWS")
    print ("contactRelationshipFound",contactRelationshipFound)
    if contactRelationshipFound is not None:
         return True
    return False


#input: current participant email, new following contact email
#output:
#   ->  True
#   ->  False
#   ->  [False,'Following contact exists already']
def add_following_contact_to_participant_aux(currentparticipantemail,newfollowingcontactemail) :
    currentparticipant = _getParticipantByEmail(currentparticipantemail,'all')  #current's email could be unverified
    newfollowingcontact = _getParticipantByEmail(newfollowingcontactemail)
    if (currentparticipant is None) or (newfollowingcontact is None) or (currentparticipantemail is newfollowingcontactemail) :
        return False
    if _getIfContactRelationshipExists(currentparticipant, newfollowingcontact) is True:
        return [False,'Following contact exists already']
    getGraph().create((currentparticipant, "FOLLOWS", newfollowingcontact))
    return True


#input: participant_email
#output: list of nodes of following contacts
def get_participant_followings(participant_email) :
    participant = _getParticipantByEmail(participant_email)
    rels = list(getGraph().match(start_node=participant, rel_type="FOLLOWS"))
    followings = []
    for rel in rels:
        followings.append(rel.end_node)
    return followings

#input: participant_email
#output: list of nodes of follower contacts
def get_participant_followers(participant_email) :
    participant = _getParticipantByEmail(participant_email)
    rels = list(getGraph().match(end_node=participant, rel_type="FOLLOWS"))
    followers = []
    for rel in rels:
        followers.append(rel.start_node)
    return followers


def get_participant_followings_info_aux(email):
    participant=_getParticipantByEmail(email)
    followings= []
    participants_followings = get_participant_followings(email)
    for p in participants_followings:
        email = p.get_properties()['email']
        username = p.get_properties()['username']
        fullname = p.get_properties()['fullname']
        followings.append({'email' : email, 'username':username, 'fullname' : fullname })
    return jsonify({"followings_num": len(participants_followings), "followings": followings})


def get_participant_followers_info_aux(email):
    participant=_getParticipantByEmail(email)
    followers= []
    participants_followers = get_participant_followers(email)
    for p in participants_followers:
        email = p.get_properties()['email']
        username = p.get_properties()['username']
        fullname = p.get_properties()['fullname']
        followers.append({'email' : email, 'username':username, 'fullname' : fullname })
    return jsonify({"followers_num" : len(participants_followers), "followers": followers})




def _addToParticipantsIndex(email, newparticipant) :
     getGraph().get_or_create_index(neo4j.Node, "Participants").add("email", email, newparticipant)
def _addToUnverifiedParticipantsIndex(email, newparticipant):
    getGraph().get_or_create_index(neo4j.Node, "UnverifiedParticipants").add("email", email, newparticipant)
def _removeFromParticipantsIndex(email, participant):
    getGraph().get_or_create_index(neo4j.Node, "Participants").remove("email", email, participant)
def _removeFromUnverifiedParticipantsIndex(email, participant):
    getGraph().get_or_create_index(neo4j.Node, "UnverifiedParticipants").remove("email", email, participant)