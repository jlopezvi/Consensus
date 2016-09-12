from py2neo import neo4j
from flask import jsonify,abort
import ast
import json
import logging
from utils import NotFoundError,getGraph


def registrationstep1_aux(inputdict):
    email = inputdict.get('email')
    try:
        __getUserByEmail(email)
        return jsonify(result="user already exists")
    #except NotFoundError as e:
    except NotFoundError:
        inputdict.update({'ifpublicprofile':False,'image_url':'http://default.jpg'})
        __newParticipant(inputdict)
        return jsonify(result="completed 1st step of registration")

def registrationstep2_aux(inputjson):
    pass
    #return jsonify(result="completed registration")

#outdated. Not in Use
def addUser_aux(userjson):
    email = userjson.get('email')
    try:
       __getUserByEmail(email)
       return jsonify(result="User was already added")
    except NotFoundError as e:
       __newUser(userjson)
       return jsonify(result="User was added")

#input: python dict {'fullname':'Juan Lopez','email': 'jj@gmail.com', 'username': 'jlopezvi',
#              'position': 'employee', 'group': 'IT', 'password': 'asdssa', 'ifpublicprofile': 'True',
#              'image_url':'http://www.consensus..../userImages/default.jpg'}
def __newParticipant(participantdict):
    email = participantdict.get('email')
    newparticipant, = getGraph().create({"fullname" : participantdict.get('fullname'), "email" : email,
                                  "username" : participantdict.get('username'), "position" : participantdict.get('position'),
                                  "group" : participantdict.get('group'), "password" : participantdict.get('password'),
                                  "ifpublicprofile" : participantdict.get('ifpublicprofile'),
                                  "image_url" : participantdict.get('image_url')
                                  })
    newparticipant.add_labels("participant")
    __addToUsersIndex(email, newparticipant)


def deleteUser(email) :
    userFound = __getUserByEmail(email)
    userFound.delete()

def getAllUsers():
    allnodes = __getUsersIndex().query("email:*")
    users = []
    for node in allnodes:
         users.append(node.get_properties())
    return users

def __getUsersIndex():
    return getGraph().get_or_create_index(neo4j.Node, "Users")

def __getUserByEmail(email) :
    userFound = __getUsersIndex().get("email", email)
    if userFound :
         return userFound[0]
    raise NotFoundError("User not Found")

def getFullNameByEmail_aux(email):
    fullname=__getUserByEmail(email)["fullname"]
    return fullname

#currentUser, newFollowingContact are graph nodes
def __getIfContactRelationshipExists(currentUser, newFollowingContact) :
    contactRelationshipFound = getGraph().match_one(start_node=currentUser, end_node=newFollowingContact,
                                                rel_type="FOLLOWS")
    print ("test10")
    print ("contactRelationshipFound",contactRelationshipFound)
    if contactRelationshipFound is not None:
         return True
    print("test19")
    return False

#input: current(currentUser given by email), newFollowingContact(given by email)
def addFollowingContactToUser_aux(current, newFollowingContact) :
    currentUser = __getUserByEmail(current)
    newFollowingContactUser = __getUserByEmail(newFollowingContact)
    if __getIfContactRelationshipExists(currentUser, newFollowingContactUser) == False:
         getGraph().create((currentUser, "FOLLOWS", newFollowingContactUser))
         return jsonify(result="Following contact was added")
    return jsonify(result="Following Contact exists already")


def getContacts(email) :
    currentUser = __getUserByEmail(email)
    rels = list(getGraph().match(start_node=currentUser, rel_type="FOLLOWS"))
    contacts = []
    for rel in rels:
        contacts.append(rel.end_node.get_properties())
        #print getGraph().node(rel.end_node)
    return contacts


def __addToUsersIndex(email, newUser) :
     getGraph().get_or_create_index(neo4j.Node, "Users").add("email", email, newUser)
 

