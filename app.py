import os

from flask import Flask,jsonify,json
from crossdomain import crossdomain
from flask import request,render_template,redirect
import ast
import json
from communityManager import saveCommunity,deleteCommunity,addCommunityToContact,getCommunities
from userManagement import __getUserByEmail,deleteUser,getAllUsers,addUser_aux, \
    addFollowingContactToUser_aux,getContacts,getFullNameByEmail_aux
from concernManager import addConcernToUser_aux,deleteOneConcern,getAllConcerns
from utils import NotFoundError
import logging

#logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/newsfeed')
def newsfeed():
    feed = [
        {
            'id': 'id',
            'picture': 'assets/profile/images.jpg',
            'name': 'Daniela',
            'duration': '2 Days',
            'supporters_goal': '5/200',
            'volunters_goal': '2/5',
            'image': 'url-to-picture',
            'problem':  'Some text for the problem',
            'proposal': 'Some text for the proposal',
            'liked':
            [
                {
                    'id': 'id',
                    'name': 'Maria'
                },
                {
                    'id': 'id',
                    'name': 'Pedro'
                },
                {
                    'id': 'id',
                    'name': 'Juan'
                },
                {
                    'id': 'id',
                    'name': 'Jesus'
                }
            ],
            'disliked': 
            [
                {
                    'id': 'id',
                    'name': 'Jose'
                }
            ]
        }
    ]
    return render_template('newsfeed.html', persons = feed)

#TEST
@app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.get_json()
    print (content['mytext'])
    #return jsonify({"uuid":uuid})
    #return "uuid"
    #return content['mytext']
    return content

@app.route('/signUp')
@app.route('/signUp/<host_email>')
def signUp(host_email=None):
    if host_email != None:
        __getUserByEmail(host_email)
    return render_template('signUp.html',host_email=host_email)



#API

#return: Full Name (normal string) corresponding to e-mail
@app.route('/getFullNameByEmail/<email>', methods=['GET'])
def getFullNameByEmail(email):
    return getFullNameByEmail_aux(email)

@app.route('/addUser', methods=['POST'])
#@crossdomain(origin='*', headers=['Content-Type'])
def addUser():
    return addUser_aux(request.get_json())

#input: json with fields "current" (current user email), "newFollowingContact" (email)
@app.route('/addFollowingContactToUser', methods=['POST'])
def addFollowingContactToUser():
    current=request.get_json()['current']
    newFollowingContact=request.get_json()['newFollowingContact']
    return addFollowingContactToUser_aux(current, newFollowingContact)
#@app.route('/addFollowingContactToUser/<string:current>/<string:newFollowingContact>', methods=['POST', 'OPTIONS'])
#def addFollowingContactToUser(current, newFollowingContact) :
#    addFollowingContactToUser_aux(current, newFollowingContact)
#    return "addFollowingContact was invoked"


@app.route('/deleteUser/<string:email>', methods=['DELETE', 'OPTIONS'])
def removeUser(email) :
    deleteUser(email)
    return "User with email %s was successfully removed" % email

@app.route('/getUsers', methods=['GET','OPTIONS'])
def getUsers():
    return json.dumps(getAllUsers())

@app.route('/getAllContactsForUser/<string:email>', methods=['GET', 'OPTIONS'])
def getAllContacts(email) :
    return json.dumps(getContacts(email))



#COMMUNITIES
@app.route('/addCommunity', methods=['POST'])
def addComunity():
    return saveCommunity(request.get_json())

@app.route('/addCommunityToUser/<string:name>/<string:email>', methods=['POST', 'OPTIONS'])
def addCommunityToUser(name, email) :
    addCommunityToContact(name, email)
    return "Community %s was added to user with email %s" % (name, email)

@app.route('/delete/community/<string:name>', methods=['DELETE', 'OPTIONS'])
def removeCommunity(name):
    deleteCommunity(name)
    return "Community %s was successfully removed" % name

@app.route('/getCommunitiesOfUser/<string:email>', methods=['GET','OPTIONS'])
def getAllCommunitiesForUser(email):
    return json.dumps(getCommunities(email))




#CONCERNS

#input: current (currentUser's email); concern (json with fields "title", "description", "image_url")
#output: newConcern is added and linked to currentUser
@app.route('/addConcernToUser/<string:current>', methods=['POST', 'OPTIONS'])
def addConcernToUser(current) :
    concern = request.get_json()
    addConcernToUser_aux(current, concern)
    return "addConcern was invoked"

@app.route('/deleteConcern/<string:idConcern>', methods=['DELETE', 'OPTIONS'])
def deleteConcern(idConcern) :
    print (idConcern)
    deleteOneConcern(idConcern)
    return "deleteConcern was invoked"

@app.route('/getConcerns/<string:current>', methods=['GET', 'OPTIONS'])
def getConcerns(current):
    print (current)
    return json.dumps(getAllConcerns(current))
       



if __name__ == '__main__':
#    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=port)


#ERROR HANDLERS
@app.errorhandler(NotFoundError)
def handle_NotFoundError(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response