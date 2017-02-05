#TODO: change system of looking for new ideas. Erase tagging "IS_NEW_FOR". DIRECT SEARCH
import os

from flask import Flask,jsonify,json, flash
from crossdomain import crossdomain
from flask import request,render_template,redirect,url_for
import ast
import json
from communityManager import saveCommunity,deleteCommunity,addCommunityToContact,getCommunities
from participantManager import _getParticipantByEmail,deleteParticipant,getAllParticipants, \
    addFollowingContactToParticipant_aux,getFollowerContacts,getFollowingContacts,getFullNameByEmail_aux,\
    registration_aux, _verifyEmail
from ideaManager import get_ideas_created_by_participant_aux, add_idea_to_user_aux,deleteOneIdea,getAllIdeas, \
    _getIdeaByIdeaIndex, vote_on_idea_aux
from webManager import ideas_for_newsfeed_aux, ideas_for_home_aux, registration_receive_emailverification_aux, \
    registration_from_invitation_aux, registration_send_invitation_aux
import logging
import flask_login
from user_authentification import User
from uuid_token import generate_confirmation_token, confirm_token
from flask_mail import Mail
from utils import send_email

#TODO: logging, sending emails when errors take place.
#logging.basicConfig(level=logging.DEBUG)

################
#### config ####
################
app = Flask(__name__)
# app.debug = True
app.config.from_object('config.BaseConfig')
try:
    os.environ['APP_SETTINGS']
    app.config.from_object(os.environ['APP_SETTINGS'])
except KeyError:
    pass

MAIL_DEFAULT_SENDER=app.config['MAIL_DEFAULT_SENDER']
SUPPORT_RATE_MIN=app.config['SUPPORT_RATE_MIN']


####################
#### extensions ####
####################

#flask-mail
mail = Mail(app)

#flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
#app.secret_key = 'super secret string'  # Change this!
@login_manager.user_loader
def user_loader(email):
    return User(email)

#@login_manager.unauthorized_handler
#def unauthorized_handler():
 #   return 'Unauthorized'


################################
####    API, WORKING NOW    ####
################################

#REPLACE /search-participant with this function /participants
# @app.route('/participants')
# def participants():
#     return render_template('/participants.html')
@app.route('/search-participant')
def search_p():
    return render_template('/search_participant.html')

#TO BE ERASED and REPLACED by two single JSON calls
@app.route('/participants')
def participants():
    participants_p = [
        {
            'id': 'id',
            'picture': 'assets/profile/perfil-mediano.png',
            'username': 'John',
            'name': 'Juan J.',
            'lastname': 'Lopez Villarejo',
            'active_publications': 5,
            'followers': 5,
            'following': 2
        }
    ]
    feed = [
        {
            'id': 'id',
            'picture': 'assets/profile/perfil-mediano.png',
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
    return render_template('login/participants.html', participants = participants_p, feed = feed)


############################################
#  API
############################################


@app.route('/')
def hello(message=None):
    return render_template('login/login.html',message=message)


@app.route('/newsfeed')
@flask_login.login_required
#user_email=flask_login.current_user.id
def newsfeed():
    return render_template('login/newsfeed.html')


@app.route('/home')
@flask_login.login_required
#user_email=flask_login.current_user.id
def home():
    return render_template('login/home.html')

##############
# PARTICIPANT MANAGER
##############


# input: json {"email":"asdf@asdf", "password":"MD5password"}
# output:
#   json {"result":"Bad e-mail"} / json {"result": "Bad password"}
#   / login cookie and redirection to '/newsfeed'
@app.route('/login', methods=['POST'])
def login():
    login = request.get_json(force=True)
    user_to_check=_getParticipantByEmail(login['email'])
    if user_to_check is None :
        return jsonify(result ="Bad e-mail")

    if login['password'] == user_to_check['password']:
        user = User(login['email'])
        flask_login.login_user(user)
        return jsonify(result="Login validated")
    else:
        return jsonify(result="Bad password")

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

#input: email
#output: json {"result" : "Participant found" / "Participant not found" }
@app.route('/get_participant_by_email/<email>')
def getParticipantByEmail(email):
    if _getParticipantByEmail(email,'all'):
        return jsonify(result="Participant found")
    return jsonify(result="Participant not found")


# input:  multipart/form-data
#        (file) profilepic_file_body
#   (data dictionary): {"fullname":"Juan Lopez","email": "jj@gmail.com", "username": "jlopezvi",
#                       "position": "employee", "group": "IT", "password": "MD5password",
#                       "host_email": "asdf@das" / "None", "ifpublicprofile": "True"/ "False",
#                       "ifregistrationfromemail": "True" / "False"}
# output: json
#          1. Wrong  -->   {"result":"Wrong","ifemailexists":true,"ifemailexists_msg":"message"}
#          2. OK (registered participant but e-mail not verified yet. Sends new e-mail for verification)  -->
#                       {"result":"OK","ifemailexists":true,"ifemailexists_msg":"message",
#                        "ifemailverified":false,"ifemailverified_msg":"message"}
#          3. OK (4 different normal cases of registration)
#                       {"result":"OK", "ifhost":true/false,"ifhost_msg":"message",
#                       "ifemailverified":true/false,"ifemailverified_msg":"message"})
@app.route('/registration', methods=['POST'])
def registration():
    profilepic_file_body = None
    # TODO: inputdict should be a real python dictionary with True, False and None. Can we use request.form.to_dict ?
    inputdict=request.form
    if 'fileUpload' in request.files:
        profilepic_file_body = request.files['fileUpload']
    return registration_aux(inputdict,profilepic_file_body)


#return: Full Name (normal string) corresponding to e-mail
@app.route('/getFullNameByEmail/<email>', methods=['GET'])
def getFullNameByEmail(email):
    return getFullNameByEmail_aux(email)

#TODO: connect with the _aux function.
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


#Not used
@app.route('/deleteParticipant/<string:email>', methods=['DELETE', 'OPTIONS'])
def removeParticipant(email) :
    deleteParticipant(email)
    return "Participant with email %s was successfully removed" % email

#Not used
@app.route('/getParticipants', methods=['GET','OPTIONS'])
def getParticipants():
    return json.dumps(getAllParticipants())

#Not used
@app.route('/getAllContactsForParticipant/<string:email>', methods=['GET', 'OPTIONS'])
def getAllContacts(email) :
    return json.dumps(getContacts(email))



###############
# IDEA MANAGER
###############


# Input: participant's email
# Output: json with fields "result", "data". "data" contains array with all ideas created by the user
# {"result": "OK",
#  "data": [
#    {
#      "author_email": "new@hotmail.com",
#      "author_photo_url": "",
#      "author_username": "newmail",
#      "concern": "this is mi new concern for test",
#      "datestamp": "01.10.2016",
#      "duration": "118 days",
#      "idea_id": "(13)",
#      "image_url": "/home/alexis/Documentos/Consensus-master/static/images/concerns/new@hotmail.com2017-01-24_092326.767044.png",
#      "moreinfo": "this and this",
#      "proposal": "this proposal is for test",
#      "rejectors": [],
#      "support_rate": 100,
#      "support_rate_MIN": 90,
#      "supporters": [],
#      "supporters_goal_num": "500",
#      "supporters_num": 0,
#      "volunteers_goal_num": "5",
#      "volunteers_num": 0
#    },
#    {
#      "author_email": "new@hotmail.com",
#      "author_photo_url": "",
#      "author_username": "newmail",
#      "concern": "Concern",
#      "datestamp": "01.10.2016",
#      "duration": "118 days",
#      "idea_id": "(9)",
#      "image_url": "http:myproposal.jpg",
#      "moreinfo": "this and this...",
#      "proposal": "IdeaM",
#      "rejectors": [],
#      "support_rate": 100,
#      "support_rate_MIN": 90,
#      "supporters": [],
#      "supporters_goal_num": "400",
#      "supporters_num": 0,
#      "volunteers_goal_num": "11",
#      "volunteers_num": 0
#    }
 # ]
#}
@app.route('/get_ideas_created_by_participant/<email>',methods=['GET'])
def get_ideas_created_by_participant(email):
    return get_ideas_created_by_participant_aux(email)


#   input:  user_email(URL); multipart/form-data
#           (file) ideapic_file_body
#       (data dictionary):  {"concern" :"we are not social enough in the office",
#                           "proposal": "social coffee pause at 4 p.m.",
#                           "datestamp":"01.10.2016",
#                           "moreinfo":"I have to say as well this and this and this...",
#                           "supporters_goal_num": 500, "volunteers_goal_num": 5}
#    output: json {"result":"OK", "result_msg":"added idea to database"}
#                 {"result":"Wrong", "result_msg":"proposal already exists"}
@app.route('/add_idea_to_user/<string:user_email>', methods=['POST'])
def add_idea_to_user(user_email) :
    ideapic_file_body = None
    idea_dict = request.form
    if 'fileUpload' in request.files:
        ideapic_file_body = request.files['fileUpload']
    return add_idea_to_user_aux(user_email,idea_dict,ideapic_file_body)


# input json {"user_email":"asd@asd.com", "idea_proposal":"let's do this", "vote_timestamp":"time", "vote_type":"supporter/rejector"}
# output json  {"result" : "Success : User vote was added"}
#             {"result" : "Failure : Idea or participant non existings"}
#             {"result" : "Failure : User vote exists already"}
@app.route('/vote_on_idea',methods=['POST'])
def vote_on_idea():
   return vote_on_idea_aux(request.get_json())


#IDEAS (NOT USED)
@app.route('/deleteConcern/<string:idConcern>', methods=['DELETE', 'OPTIONS'])
def deleteConcern(idConcern) :
    print (idConcern)
    deleteOneConcern(idConcern)
    return "deleteConcern was invoked"

@app.route('/getConcerns/<string:current>', methods=['GET', 'OPTIONS'])
def getConcerns(current):
    print (current)
    return json.dumps(getAllConcerns(current))


##############
# WEB MANAGER
##############


# TODO: try with redirect instead of render_template
# input: URL token link from an invitation e-mail
# output: redirects to login with a json called "message"
#  -> json {"result": "The confirmation link is invalid or has expired"}
#  -> json {"result": "invitation:OK", "current_email": "guestemail@com", "host_email": host_email@com"}
@app.route('/registration_from_invitation/<token>/<guest_email>')
def registration_from_invitation(token, guest_email):
    return registration_from_invitation_aux(token, guest_email)


# input: host_email and guest_email
# output: sends registration e-mail
@app.route('/registration_send_invitation/<host_email>/<guest_email>', methods=['GET'])
def registration_send_invitation(host_email, guest_email):
    return registration_send_invitation_aux(host_email, guest_email)


# TODO: try with redirect instead of render_template
# input: URL token link from an invitation e-mail
# output: redirects to login with a json called "message"
#  -> json {"result": "The confirmation link is invalid or has expired"}
#  -> json {"result": "email already confirmed"}
#  -> json {"result": "email not registered"}
# TODO: redirects to a place with a message of "email verified" and then, login user and redirection to newsfeed.
# TODO: should I login user when email verified? review registration_aux where I log in user? what's the interplay
# among the two of them?
#  -> json {"result": "emailverification:OK", "email": "asdf@dasdf.com"}
@app.route('/registration_receive_emailverification/<token>')
def registration_receive_emailverification(token):
    return registration_receive_emailverification_aux(token)


# TODO: add weights for ideas
# Get Ideas For Newsfeed
# Input: << flask_login.current_user.id >>
# Output: json with fields 'result' and 'data'. 'data' contains array with all ideas that the user has not << VOTED_ON >>
# {'result':'OK',
#  'data': [
#    {
#      "author_email": "new1@hotmail.com",
#      "author_photo_url": "",
#      "author_username": "new1",
#      "concern": "this is mi new concern for test",
#      "datestamp": "01.10.2016",
#      "duration": "118 days",
#      "idea_id": "(13)",
#      "image_url": "/home/alexis/Documentos/Consensus-master/static/images/concerns/new1hotmail.com2017-01-24_092326.767044.png",
#      "moreinfo": "this and this",
#      "proposal": "this proposal is for test",
#      "rejectors": [],
#      "support_rate": 100,
#      "support_rate_MIN": 90,
#      "supporters": [
#             { "email": "new2@hotmail.com", "username": "new2_mail" }
#                   ],
#      "supporters_goal_num": "500",
#      "supporters_num": 0,
#      "volunteers_goal_num": "5",
#      "volunteers_num": 0
#    },
#    {
#      "author_email": "new2@hotmail.com",
#      "author_photo_url": "",
#      "author_username": "new2",
#      "concern": "Concern",
#      "datestamp": "01.10.2016",
#      "duration": "118 days",
#      "idea_id": "(9)",
#      "image_url": "http:myproposal.jpg",
#      "moreinfo": "this and this...",
#      "proposal": "IdeaM",
#      "rejectors": [
#           { "email": "new1@hotmail.com", "username": "new1_mail" }
#                   ],
#      "support_rate": 100,
#      "support_rate_MIN": 90,
#      "supporters": [],
#      "supporters_goal_num": "400",
#      "supporters_num": 0,
#      "volunteers_goal_num": "11",
#      "volunteers_num": 0
#    }
 # ]
 #}
@app.route('/ideas_for_newsfeed')
@flask_login.login_required
def ideas_for_newsfeed():
    return ideas_for_newsfeed_aux(flask_login.current_user.id)


# TEMPORARY: función para testear con ARC el << newsfeed >>
@app.route('/ideas_for_newsfeed_test',methods=['POST'])
def ideas_for_newsfeed_test():
    email=request.get_json()['email']
    return ideas_for_newsfeed_aux(email)



# Ideas For Home: See the Supported + Volunteered ideas/ See the ignored ideas / See the rejected ideas
# Input: JSON {"email":"new@gmail.com", "vote_type": "rejected/supported/ignored"
# Output: json with fields 'result' and 'data'. 'data' Array with all ideas that the user has voted according to << vote_type >>
# {'result':'OK',
#  'data': [
#    {
#      "author_email": "adavidsole@gmail.com",
#      "author_username": "alexdsole",
#      "concern": "Concern",
#      "datestamp": "01.10.2016",
#      "duration": "118 days",
#      "idea_id": "(6)",
#      "image_url": "http:myproposal.jpg",
#      "moreinfo": "this and this...",
#      "proposal": "New Proposal ",
#      "rejectors": [
#            { "email": "new1@hotmail.com", "username": "new1_mail" }
#                   ],
#      "support_rate": 0,
#      "support_rate_MIN": 90,
#      "supporters": [],
#      "supporters_goal_num": "400",
#      "supporters_num": 0,
#      "volunteers_goal_num": "11",
#      "volunteers_num": 0
#    },
#    {
#      "author_email": "newemail@hotmail.com",
#      "author_photo_url": "",
#      "author_username": "newemail",
#      "concern": "Concern",
#      "datestamp": "01.10.2016",
#      "duration": "118 days",
#      "idea_id": "(5)",
#      "image_url": "http:myproposal.jpg",
#      "moreinfo": "this and this...",
#      "proposal": "This is my Proposal",
#      "rejectors": [
#           { "email": "new1@hotmail.com", "username": "new1_mail" }
#                   ],
#      "support_rate": 50,
#      "support_rate_MIN": 90,
#      "supporters": [
#           { "email": "new2@gmail.com", "username": "new2_mail"  }
#                    ],
#      "supporters_goal_num": "400",
#      "supporters_num": 1,
#      "volunteers_goal_num": "11",
#      "volunteers_num": 1
#    }
#  ]
#}
@app.route('/ideas_for_home',methods=['POST'])
def ideas_for_home():
    email=request.get_json()['email']
    vote_type=request.get_json()['vote_type']
    return ideas_for_home_aux(email,vote_type)



########################
# COMMUNITIES (NOT USED)
#######################

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



################
# ERROR HANDLERS
################
#@app.errorhandler(NotFoundError)
#def handle_NotFoundError(error):
#    response = jsonify(error.to_dict())
#    response.status_code = error.status_code
#    return response



################
# MAIN PROGRAM
################

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if os.environ.get('GRAPHENEDB_URL'):
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(host='127.0.0.1', port=port)
