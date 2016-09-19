from py2neo import neo4j
from flask import jsonify,abort
import ast
import json
import logging
from utils import NotFoundError,getGraph


#input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'IT', 'password': 'MD5password',
#              'image_url': 'http://.... ', 'ifpublicprofile': True / False,
#              'host_email': 'asdf@das' / None, 'ifemailverified': True / False}
#return: json {"result": "completed registration"
#                        / "registration pending of email verification"
#                        / "participant already exists"}
def registration_aux(inputdict):
    email = inputdict.get('email')
    try:
        __getParticipantByEmail(email)
        return jsonify(result="participant already exists")
    #except NotFoundError as e:
    except NotFoundError:
        ifemailverified=inputdict.get('ifemailverified')
        host_email=inputdict.get('host_email')
        if ifemailverified is True :
            __newParticipant(inputdict)
            if host_email:
                addFollowingContactToParticipant_aux(email, host_email)
            return jsonify(result="completed registration")
        elif ifemailverified is False :
            __newUnverifiedParticipant(inputdict)
            if host_email:
                addFollowingContactToUnverifiedParticipant_aux(email, host_email)
            return jsonify(result="registration pending of email verification")



#outdated. Not in Use
def addParticipant_aux(participantjson):
    email = participantjson.get('email')
    try:
       __getParticipantByEmail(email)
       return jsonify(result="Participant was already added")
    except NotFoundError as e:
       __newParticipant(participantjson)
       return jsonify(result="Participant was added")


#input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'IT', 'password': 'MD5password',
#              'image_url': 'http://.... ', 'ifpublicprofile': True / False}
def __newParticipant(participantdict):
    email = participantdict.get('email')
    newparticipant, = getGraph().create({"fullname" : participantdict.get('fullname'), "email" : email,
                                  "username" : participantdict.get('username'), "position" : participantdict.get('position'),
                                  "group" : participantdict.get('group'), "password" : participantdict.get('password'),
                                  "ifpublicprofile" : participantdict.get('ifpublicprofile'),
                                  "image_url" : participantdict.get('image_url')
                                  })
    newparticipant.add_labels("participant")
    __addToParticipantsIndex(email, newparticipant)
def __newUnverifiedParticipant(participantdict):
    email = participantdict.get('email')
    newparticipant, = getGraph().create({"fullname" : participantdict.get('fullname'), "email" : email,
                                  "username" : participantdict.get('username'), "position" : participantdict.get('position'),
                                  "group" : participantdict.get('group'), "password" : participantdict.get('password'),
                                  "ifpublicprofile" : participantdict.get('ifpublicprofile'),
                                  "image_url" : participantdict.get('image_url')
                                  })
    newparticipant.add_labels("unverified_participant")
    __addToUnverifiedParticipantsIndex(email, newparticipant)

def __verifyEmail(email):
    participant=__getUnverifiedParticipantByEmail(email)
    __removeFromUnverifiedParticipantsIndex(email, participant)
    __addToParticipantsIndex(email, participant)
    participant.remove_labels("unverified_participant")
    participant.add_labels("participant")
    return jsonify({'result': 'OK'})


def deleteParticipant(email) :
    participantFound = __getParticipantByEmail(email)
    participantFound.delete()

def getAllParticipants():
    allnodes = __getParticipantsIndex().query("email:*")
    participants = []
    for node in allnodes:
         participants.append(node.get_properties())
    return participants

def __getParticipantsIndex():
    return getGraph().get_or_create_index(neo4j.Node, "Participants")
def __getUnverifiedParticipantsIndex():
    return getGraph().get_or_create_index(neo4j.Node, "UnverifiedParticipants")


def __getParticipantByEmail(email) :
    participantFound = __getParticipantsIndex().get("email", email)
    if participantFound :
        return participantFound[0]
    raise NotFoundError("Participant not Found")
def __getUnverifiedParticipantByEmail(email) :
    participantFound = __getUnverifiedParticipantsIndex().get("email", email)
    if participantFound :
         return participantFound[0]
    raise NotFoundError("Unverified Participant not Found")

def getFullNameByEmail_aux(email):
    fullname=__getParticipantByEmail(email)["fullname"]
    return fullname

#currentParticipant, newFollowingContact are graph nodes
def __getIfContactRelationshipExists(currentParticipant, newFollowingContact) :
    contactRelationshipFound = getGraph().match_one(start_node=currentParticipant, end_node=newFollowingContact,
                                                rel_type="FOLLOWS")
    print ("contactRelationshipFound",contactRelationshipFound)
    if contactRelationshipFound is not None:
         return True
    return False

#input: current participant email, new following contact email
#output: json ("Following contact was added"/"Following contact exists already")
def addFollowingContactToParticipant_aux(currentparticipantemail, newfollowingcontactemail) :
    currentparticipant = __getParticipantByEmail(currentparticipantemail)
    newfollowingcontact = __getParticipantByEmail(newfollowingcontactemail)
    if __getIfContactRelationshipExists(currentparticipant, newfollowingcontact) == False:
         getGraph().create((currentparticipant, "FOLLOWS", newfollowingcontact))
         return jsonify(result="Following contact was added")
    return jsonify(result="Following contact exists already")
def addFollowingContactToUnverifiedParticipant_aux(currentparticipantemail, newfollowingcontactemail) :
    currentparticipant = __getUnverifiedParticipantByEmail(currentparticipantemail)
    newfollowingcontact = __getParticipantByEmail(newfollowingcontactemail)
    if __getIfContactRelationshipExists(currentparticipant, newfollowingcontact) == False:
         getGraph().create((currentparticipant, "FOLLOWS", newfollowingcontact))
         return jsonify(result="Following contact was added")
    return jsonify(result="Following contact exists already")

def getContacts(email) :
    currentParticipant = __getParticipantByEmail(email)
    rels = list(getGraph().match(start_node=currentParticipant, rel_type="FOLLOWS"))
    contacts = []
    for rel in rels:
        contacts.append(rel.end_node.get_properties())
        #print getGraph().node(rel.end_node)
    return contacts


def __addToParticipantsIndex(email, newparticipant) :
     getGraph().get_or_create_index(neo4j.Node, "Participants").add("email", email, newparticipant)
def __addToUnverifiedParticipantsIndex(email, newparticipant):
    getGraph().get_or_create_index(neo4j.Node, "UnverifiedParticipants").add("email", email, newparticipant)
def __removeFromUnverifiedParticipantsIndex(email, participant):
    getGraph().get_or_create_index(neo4j.Node, "UnverifiedParticipants").remove("email", email, participant)