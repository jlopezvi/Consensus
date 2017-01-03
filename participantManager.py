from py2neo import neo4j
from flask import jsonify,abort, redirect,url_for, render_template
import ast
import json
import logging
from utils import getGraph, send_email
from uuid_token import generate_confirmation_token
import datetime
from user_authentification import User
import flask_login
from werkzeug.utils import secure_filename
import os
basedir = os.path.abspath(os.path.dirname(__file__))


# input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'IT', 'password': 'MD5password',
#              'host_email': 'asdf@das' / None, 'ifregistrationfromemail': True / False}
# output: json
#          1. Wrong  -->   {"result":"Wrong","ifemailexists":true,"ifemailexists_msg":ifemailexists_msg[true]}
#          2. OK (registered participant but e-mail not verified yet. Sends new e-mail for verification)  -->
#                       {"result":"OK","ifemailexists":true,"ifemailexists_msg":ifemailexists_msg[true],
#                        "ifemailverified":false,"ifemailverified_msg":ifemailverified_msg[false]}
#          3. OK (4 different normal cases of registration)
#                       {"result":"OK", "ifhost":true/false,"ifhost_msg":ifhost_msg[ifhost],
#                       "ifemailverified":true/false,"ifemailverified_msg":ifemailverified_msg[ifemailverified]})
def registration_basicdata_aux(inputdict):
    email = inputdict['email']
    ifemailexists_msg=[None,"Participant already exists"]
    ifemailverified_msg= ["E-mail not verified. E-mail verification sent. " \
                          "Close this window and check your e-mail within the next few minutes ", None]
    ifhost_msg=[None, "You will be following your host in Consensus"]
    if _getParticipantByEmail(email,'all'):   # email exists?
        ifemailexists = True
        if _getParticipantByEmail(email):   # participant's email is verified?
            return jsonify({"result":"Wrong","ifemailexists":ifemailexists,"ifemailexists_msg":ifemailexists_msg[ifemailexists]})
        else:
            ifemailverified=False
            result_send_emailverification = _registration_send_emailverification(email)
            if result_send_emailverification is "OK" :
                return jsonify({"result":"OK","ifemailexists":ifemailexists,"ifemailexists_msg":ifemailexists_msg[ifemailexists],
                                "ifemailverified":ifemailverified,"ifemailverified_msg":ifemailverified_msg[ifemailverified]})
    # save data for new (verified / unverified) participant in database
    _newParticipant(inputdict)
    ifhost = False
    if inputdict['host_email']:
        # current_participant (verified/unverified) follows host
        ifhost = addFollowingContactToParticipant_aux(email, inputdict['host_email'])
    ifemailverified=inputdict['ifregistrationfromemail']
    if ifemailverified is True :
        user = User(email)
        flask_login.login_user(user)
    else:
        _registration_send_emailverification(email)
    return jsonify({"result":"OK", "ifhost":ifhost,"ifhost_msg":ifhost_msg[ifhost],
                   "ifemailverified":ifemailverified,"ifemailverified_msg":ifemailverified_msg[ifemailverified]})


#input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'Human Resources', 'password': 'MD5password',
#              'ifregistrationfromemail': True / False}
#output: python dict {'result':'OK'}
def _newParticipant(participantdict):
    email = participantdict['email']
    #add some default values for profile (changed with completeregistration)
    default_profilepic_url = 'static/assets/profile/perfil-mediano.png'
    default_ifpublicprofile = False
    newparticipant, = getGraph().create({"fullname": participantdict['fullname'], "email": email,
                                         "username": participantdict['username'], "position": participantdict['position'],
                                         "group": participantdict['group'], "password": participantdict['password'],
                                         "profilepic_url":default_profilepic_url, "ifpublicprofile":default_ifpublicprofile
                                         })
    if participantdict['ifregistrationfromemail'] is True:
        newparticipant.add_labels("participant")
        _addToParticipantsIndex(email, newparticipant)
    elif participantdict['ifregistrationfromemail'] is False:
        newparticipant.add_labels("unverified_participant")
        _addToUnverifiedParticipantsIndex(email, newparticipant)
    return "OK"

# input: python dict {'email': 'jj@gmail.com', 'ifpublicprofile': True/False,
#               'ifprofilepic':True/False}
# output: json {"result": "Wrong"}
#              {"result": "OK"}
#              {"result": "OK: profilepic", "profilepic_url": "static/assets/profile/email@adress.png"}
def registration_completeregistration_aux(inputdict):
    email=inputdict['email']
    participant=_getParticipantByEmail(email,'all')
    if participant is None:
        return jsonify({"result": "Wrong"})
    else:
        participant.set_properties({"ifpublicprofile": inputdict['ifpublicprofile']})
        if inputdict['ifprofilepic'] is True:
            response = _registration_uploadprofilepic(email)
            if response is "OK":
                return jsonify({"result": "OK: profilepic"})
        elif inputdict['ifprofilepic'] is False:
            return jsonify({"result": "OK"})

def _registration_uploadprofilepic(email, profilepic_file_body):
    currentparticipant = _getParticipantByEmail(email,'all')
    if (profilepic_file_body is None) or (currentparticipant is None):
        return "Wrong"
    else:
        path = basedir + '/static/assets/profile/'
        # TODO: change name for profilepic. Currently the email.
        filename=str(email)+'.png'
        profilepic_file_body.save(os.path.join(path, secure_filename(filename)))
        currentparticipant["profilepic_url"] = path + secure_filename(filename)
        return "OK"


# input: email to be verified as an argument
# output: e-mail to the email account with a URL token link for email verification
#         and json {"result": "email sent"}
def _registration_send_emailverification(email):
    token = generate_confirmation_token(email)
    confirm_url = url_for('.registration_receive_emailverification', token=token, _external=True)
    html = render_template('login/verification_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(email, subject, html)
    return "OK"


# def _newUnverifiedParticipant(participantdict):
#     email = participantdict.get('email')
#     newparticipant, = getGraph().create({"fullname" : participantdict.get('fullname'), "email" : email,
#                                   "username" : participantdict.get('username'), "position" : participantdict.get('position'),
#                                   "group" : participantdict.get('group'), "password" : participantdict.get('password'),
#                                   "ifpublicprofile" : participantdict.get('ifpublicprofile'),
#                                   "image_url" : participantdict.get('image_url')
#                                   })
#     newparticipant.add_labels("unverified_participant")
#     _addToUnverifiedParticipantsIndex(email, newparticipant)

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
def addFollowingContactToParticipant_aux(currentparticipantemail, newfollowingcontactemail) :
    currentparticipant = _getParticipantByEmail(currentparticipantemail,'all')  #current's email could be unverified
    newfollowingcontact = _getParticipantByEmail(newfollowingcontactemail)
    if (currentparticipant is None) or (newfollowingcontact is None) or (currentparticipantemail is newfollowingcontactemail) :
        return False
    if _getIfContactRelationshipExists(currentparticipant, newfollowingcontact) == True:
        return [False,'Following contact exists already']
    getGraph().create((currentparticipant, "FOLLOWS", newfollowingcontact))
    return True

# def addFollowingContactToUnverifiedParticipant_aux(currentparticipantemail, newfollowingcontactemail) :
#     currentparticipant = _getUnverifiedParticipantByEmail(currentparticipantemail)
#     newfollowingcontact = _getParticipantByEmail(newfollowingcontactemail)
#     if _getIfContactRelationshipExists(currentparticipant, newfollowingcontact) == False:
#          getGraph().create((currentparticipant, "FOLLOWS", newfollowingcontact))
#          return jsonify(result="Following contact was added")
#     return jsonify(result="Following contact exists already")

#input: participant_email
#output: list of nodes of following contacts
def getFollowingContacts(participant_email) :
    participant = _getParticipantByEmail(participant_email)
    rels = list(getGraph().match(start_node=participant, rel_type="FOLLOWS"))
    following_contacts = []
    for rel in rels:
        following_contacts.append(rel.end_node)
    return following_contacts

#input: participant_email
#output: list of nodes of follower contacts
def getFollowerContacts(participant_email) :
    participant = _getParticipantByEmail(participant_email)
    rels = list(getGraph().match(end_node=participant, rel_type="FOLLOWS"))
    follower_contacts = []
    for rel in rels:
        follower_contacts.append(rel.start_node)
    return follower_contacts

def _addToParticipantsIndex(email, newparticipant) :
     getGraph().get_or_create_index(neo4j.Node, "Participants").add("email", email, newparticipant)
def _addToUnverifiedParticipantsIndex(email, newparticipant):
    getGraph().get_or_create_index(neo4j.Node, "UnverifiedParticipants").add("email", email, newparticipant)
def _removeFromParticipantsIndex(email, participant):
    getGraph().get_or_create_index(neo4j.Node, "Participants").remove("email", email, participant)
def _removeFromUnverifiedParticipantsIndex(email, participant):
    getGraph().get_or_create_index(neo4j.Node, "UnverifiedParticipants").remove("email", email, participant)