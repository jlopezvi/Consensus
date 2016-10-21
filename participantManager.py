from py2neo import neo4j
from flask import jsonify,abort
import ast
import json
import logging
from utils import getGraph
import datetime


#input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'IT', 'password': 'MD5password',
#              'image_url': 'http://.... ', 'ifpublicprofile': True / False,
#              'host_email': 'asdf@das' / None, 'ifemailverified': True / False}
#return: json {"result": "completed registration"
#                        / "registration pending of email verification"
#                        / "participant already exists"}
def registration_aux(inputdict):
    email = inputdict.get('email')
    if _getParticipantByEmail(email) :
        return jsonify(result="participant already exists")
    else : #registration
        ifemailverified=inputdict.get('ifemailverified')
        host_email=inputdict.get('host_email')
        if ifemailverified is True :
            _newParticipant(inputdict)
            if host_email and (host_email is not email):
                addFollowingContactToParticipant_aux(email, host_email)
            return jsonify(result="completed registration")
        else :
            _newUnverifiedParticipant(inputdict)
            if host_email:
                addFollowingContactToUnverifiedParticipant_aux(email, host_email)
            return jsonify(result="registration pending of email verification")



#input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'IT', 'password': 'MD5password',
#              'image_url': 'http://.... ', 'ifpublicprofile': True / False}
def _newParticipant(participantdict):
    email = participantdict.get('email')
    newparticipant, = getGraph().create({"fullname" : participantdict.get('fullname'), "email" : email,
                                  "username" : participantdict.get('username'), "position" : participantdict.get('position'),
                                  "group" : participantdict.get('group'), "password" : participantdict.get('password'),
                                  "ifpublicprofile" : participantdict.get('ifpublicprofile'),
                                  "image_url" : participantdict.get('image_url')
                                  })
    newparticipant.add_labels("participant")
    _addToParticipantsIndex(email, newparticipant)
def _newUnverifiedParticipant(participantdict):
    email = participantdict.get('email')
    newparticipant, = getGraph().create({"fullname" : participantdict.get('fullname'), "email" : email,
                                  "username" : participantdict.get('username'), "position" : participantdict.get('position'),
                                  "group" : participantdict.get('group'), "password" : participantdict.get('password'),
                                  "ifpublicprofile" : participantdict.get('ifpublicprofile'),
                                  "image_url" : participantdict.get('image_url')
                                  })
    newparticipant.add_labels("unverified_participant")
    _addToUnverifiedParticipantsIndex(email, newparticipant)

def _verifyEmail(email):
    unverifiedparticipant = _getUnverifiedParticipantByEmail(email)
    if unverifiedparticipant is None:
       if _getParticipantByEmail(email):
           return {'result': 'email already confirmed'}
       else:
           return {'result': 'email not registered'}
    else:
        unverifiedparticipant = _getUnverifiedParticipantByEmail(email)
        _removeFromUnverifiedParticipantsIndex(email, unverifiedparticipant)
        _addToParticipantsIndex(email, unverifiedparticipant)
        unverifiedparticipant.remove_labels("unverified_participant")
        unverifiedparticipant.add_labels("participant")
        #TODO datestamp for registration
        #registered_on=datetime.datetime.now()
        return {'result': 'OK'}



def deleteParticipant(email) :
    participantFound = _getParticipantByEmail(email)
    participantFound.delete()

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


def _getParticipantByEmail(email) :
    participantFound = _getParticipantsIndex().get("email", email)
    if participantFound :
        return participantFound[0]
    return None
def _getUnverifiedParticipantByEmail(email) :
    participantFound = _getUnverifiedParticipantsIndex().get("email", email)
    if participantFound :
         return participantFound[0]
    return None

def getFullNameByEmail_aux(email):
    fullname=_getParticipantByEmail(email)["fullname"]
    return fullname

#currentParticipant, newFollowingContact are graph nodes
def _getIfContactRelationshipExists(currentParticipant, newFollowingContact) :
    contactRelationshipFound = getGraph().match_one(start_node=currentParticipant, end_node=newFollowingContact,
                                                rel_type="FOLLOWS")
    print ("contactRelationshipFound",contactRelationshipFound)
    if contactRelationshipFound is not None:
         return True
    return False

#input: current participant email, new following contact email
#output: json ("Following contact was added"/"Following contact exists already")
def addFollowingContactToParticipant_aux(currentparticipantemail, newfollowingcontactemail) :
    currentparticipant = _getParticipantByEmail(currentparticipantemail)
    newfollowingcontact = _getParticipantByEmail(newfollowingcontactemail)
    if _getIfContactRelationshipExists(currentparticipant, newfollowingcontact) == False:
         getGraph().create((currentparticipant, "FOLLOWS", newfollowingcontact))
         return jsonify(result="Following contact was added")
    return jsonify(result="Following contact exists already")
def addFollowingContactToUnverifiedParticipant_aux(currentparticipantemail, newfollowingcontactemail) :
    currentparticipant = _getUnverifiedParticipantByEmail(currentparticipantemail)
    newfollowingcontact = _getParticipantByEmail(newfollowingcontactemail)
    if _getIfContactRelationshipExists(currentparticipant, newfollowingcontact) == False:
         getGraph().create((currentparticipant, "FOLLOWS", newfollowingcontact))
         return jsonify(result="Following contact was added")
    return jsonify(result="Following contact exists already")

def getFollowingContacts(participant_email) :
    participant = _getParticipantByEmail(participant_email)
    rels = list(getGraph().match(start_node=participant, rel_type="FOLLOWS"))
    following_contacts = []
    for rel in rels:
        following_contacts.append(rel.end_node)
    return following_contacts

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
def _removeFromUnverifiedParticipantsIndex(email, participant):
    getGraph().get_or_create_index(neo4j.Node, "UnverifiedParticipants").remove("email", email, participant)