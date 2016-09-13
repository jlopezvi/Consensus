import os

from flask import Flask,jsonify,json
from crossdomain import crossdomain
from flask import request,render_template,redirect
import ast
import json
from communityManager import saveCommunity,deleteCommunity,addCommunityToContact,getCommunities
from userManagement import __getParticipantByEmail,deleteParticipant,getAllParticipants,addParticipant_aux, \
    addFollowingContactToParticipant_aux,getContacts,getFullNameByEmail_aux,registration_aux
from concernManager import addConcernToUser_aux,deleteOneConcern,getAllConcerns
from utils import NotFoundError
import logging

#logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('login/login.html')


@app.route('/home')
def home():  
    feed_home = [
        {
            'id': 'id',
            'picture': 'assets/profile/images.jpg',
            'name': 'Daniela',
            'duration': '2 Days',
            'supporters_goal': 200,
            'supporters_current': 5,
            'volunters_goal': 5,
            'volunters_current': 2,
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
    return render_template('home.html', persons_home = feed_home) 


@app.route('/newsfeed')
def newsfeed():
    feed = [
        {
            'id': 'id',
            'picture': 'assets/profile/images.jpg',
            'name': 'Daniela',
            'duration': '2 Days',
            'supporters_goal': 200,
            'supporters_current': 5,
            'volunters_goal': 5,
            'volunters_current': 2,
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
    return render_template('login/newsfeed.html', persons = feed)

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
        __getParticipantByEmail(host_email)
    return render_template('signUp.html',host_email=host_email)



#API

#input: json {"fullname":"Juan Lopez","email": "jj@gmail.com", "username": "jlopezvi",
#              "position": "employee", "group": "IT", "password": "MD5password",
#              "image_url": "http://.... ", "ifpublicprofile": true / false,
#              "host_email": "asdf@das" / null, "ifemailverified": true / false}
#return: json {"result": "completed registration"
#                        / "registration pending of email verification"
#                        / "user already exists"}
@app.route('/registration', methods=['POST'])
def registration():
    #call with json_data converted to python_dictionary_data
    return registration_aux(request.get_json())

#return: Full Name (normal string) corresponding to e-mail
@app.route('/getFullNameByEmail/<email>', methods=['GET'])
def getFullNameByEmail(email):
    return getFullNameByEmail_aux(email)

@app.route('/addParticipant', methods=['POST'])
#@crossdomain(origin='*', headers=['Content-Type'])
def addParticipant():
    return addParticipant_aux(request.get_json())

#input: json with fields "current" (current user email), "newFollowingContact" (email)
@app.route('/addFollowingContactToParticipant', methods=['POST'])
def addFollowingContactToParticipant():
    current=request.get_json()['current']
    newFollowingContact=request.get_json()['newFollowingContact']
    return addFollowingContactToParticipant_aux(current, newFollowingContact)
#@app.route('/addFollowingContactToParticipant/<string:current>/<string:newFollowingContact>', methods=['POST', 'OPTIONS'])
#def addFollowingContactToParticipant(current, newFollowingContact) :
#    addFollowingContactToParticipant_aux(current, newFollowingContact)
#    return "addFollowingContact was invoked"


@app.route('/deleteParticipant/<string:email>', methods=['DELETE', 'OPTIONS'])
def removeParticipant(email) :
    deleteParticipant(email)
    return "Participant with email %s was successfully removed" % email

@app.route('/getParticipants', methods=['GET','OPTIONS'])
def getParticipants():
    return json.dumps(getAllParticipants())

@app.route('/getAllContactsForParticipant/<string:email>', methods=['GET', 'OPTIONS'])
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
    #app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=port)


#ERROR HANDLERS
@app.errorhandler(NotFoundError)
def handle_NotFoundError(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response