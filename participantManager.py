from py2neo import neo4j
from flask import jsonify,abort, redirect,url_for
import ast
import json
import logging
from utils import getGraph
import datetime
from user_authentification import User
import flask_login


#input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'IT', 'password': 'MD5password',
#              'image_url': 'http://.... ', 'ifpublicprofile': True / False,
#              'host_email': 'asdf@das' / None, 'ifemailverified': True / False}
#output:
#     -> NOT USED BY FRONTEND  json {"result": "participant already exists""}
#     -> login and json {"result": "email not verified"} (on registration pending of email verification)
#     -> login and json {"result": "OK"} (on registration completed)
def registration_aux(inputdict,profilepic_file_body=None):
    email = inputdict['email']
    if _getParticipantByEmail(email,'all') :
        return jsonify(result="participant already exists")
    else : #registration
        _newParticipant(inputdict)
        if inputdict['host_email']:
            #TODO: verify valid host_email (exists and it is not equal to email)
            addFollowingContactToParticipant_aux(email, inputdict['host_email'])
        #user login
        user = User(email)
        flask_login.login_user(user)
        #routes depending on whether the email has been verified or not
        if inputdict['ifemailverified'] is True:
            return jsonify(result="OK")
            #return redirect(url_for('newsfeed'))
        else :
            return jsonify(result="email not verified")
            #return redirect(url_for('registration_send_emailverification', email=email))

            #return jsonify(result="registration pending of email verification")
        # else :
        #     _newUnverifiedParticipant(inputdict)
        #     if host_email:
        #         addFollowingContactToUnverifiedParticipant_aux(email, host_email)
        #     user = User(email)
        #     flask_login.login_user(user)
        #     return redirect(url_for('newsfeed2'))
        #     #return jsonify(result="registration pending of email verification")



#input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'Human Resources', 'password': 'MD5password',
#              'image_url': 'http://.... ', 'ifpublicprofile': True / False,
#              'ifemailverified': True / False}
#output: python dict {'result':'OK'}
def _newParticipant(participantdict):
    email = participantdict['email']
    newparticipant, = getGraph().create({"fullname" : participantdict['fullname'], "email" : email,
                                  "username" : participantdict['username'], "position" : participantdict['position'],
                                  "group" : participantdict['group'], "password" : participantdict['password'],
                                  "ifpublicprofile" : participantdict['ifpublicprofile'],
                                  "image_url" : participantdict['image_url']
                                  })
    if participantdict['ifemailverified']==True:
        newparticipant.add_labels("participant")
        _addToParticipantsIndex(email, newparticipant)
    elif participantdict['ifemailverified']== False:
        newparticipant.add_labels("unverified_participant")
        _addToUnverifiedParticipantsIndex(email, newparticipant)
    return {'result' : 'OK'}

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
#output: json
#   ->  {"result" : "Following contact was added"}
#   ->  {"result" : "Following contact exists already")
def addFollowingContactToParticipant_aux(currentparticipantemail, newfollowingcontactemail) :
    currentparticipant = _getParticipantByEmail(currentparticipantemail,'all')  #current's email could be unverified
    newfollowingcontact = _getParticipantByEmail(newfollowingcontactemail)
    if _getIfContactRelationshipExists(currentparticipant, newfollowingcontact) == False:
         getGraph().create((currentparticipant, "FOLLOWS", newfollowingcontact))
         return jsonify(result="Following contact was added")
    return jsonify(result="Following contact exists already")
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