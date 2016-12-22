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
    registration_aux,_verifyEmail
from ideaManager import Idea, addIdeaToUser_aux,deleteOneIdea,getAllIdeas, spreadIdeaToFollowers_aux, \
    _getIdeaByIdeaIndex, vote_on_idea_aux
from webManager import ideas_for_newsfeed_aux
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


@app.route('/search-participant')
def search_p():
    return render_template('/search_participant.html')


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


@app.route('/home')
def home():  
    feed_home = [
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
    print(feed_home)
    return render_template('home.html', persons_home = feed_home) 


#input: user_email(URL); idea (json)
#    {"concern" :"we are not social enough in the office",
#     "proposal": "social coffee pause at 4 p.m.",
#     "image_url" : "static/images/concerns/social_coffee_break.jpg",
#     "datestamp":"01.10.2016",
#     "moreinfo":"I have to say as well this and this and this...",
#     "supporters_goal_num": 500, "volunteers_goal_num": 5}
@app.route('/addIdeaToUser/<string:user_email>', methods=['POST'])
def addIdeaToUser(user_email) :
    idea_dict = request.get_json()
    idea_object = Idea(idea_dict)
    return addIdeaToUser_aux(user_email, idea_object)

#input: nothing
#output: render_template to newsfeed
@app.route('/newsfeed')
@flask_login.login_required
#user_email=flask_login.current_user.id
def newsfeed():
    return render_template('login/newsfeed.html')

#input : NOTHING
#output : json named "feed"
# feed = {
# 'idea_id' : 120,
# 'author_photo_url' : 'assets/profile/perfil-mediano.png', 'author_username' : 'Daniela', 'author_email' : 'a@',
# 'duration' : '2 days',
# 'supporters_goal_num' : 200, 'supporters_num' : 5, 'volunteers_goal_num' : 5, 'volunteers_num' : 2,
# 'image_url' : 'url-to-picture',
# 'concern': 'Some text for the concern',
# 'proposal': 'Some text for the proposal',
# 'support_rate' : 95,
# 'support_rate_MIN' : 90,
# 'supporters': [
# { 'email': 'b@', 'username': 'Maria' }, { 'email': 'c@', 'username': 'Pedro' }
#             ],
# 'rejectors':[
# { 'email': 'd@', 'username': 'Elisa' }
#               ]
# }
@app.route('/ideas_for_newsfeed')
@flask_login.login_required
def ideas_for_newsfeed():
    return ideas_for_newsfeed_aux(flask_login.current_user.id)
    #return ideas_for_newsfeed_aux(email)



#TODO: try with redirect instead of render_template
#input: URL token link from an invitation e-mail
#output: redirects to login with a json called "message"
#  -> json {"result": "The confirmation link is invalid or has expired"}
#  -> json {"result": "email already confirmed"}
#  -> json {"result": "email not registered"}
#TODO: redirects to a place with a message of "email verified" and then, login user and redirection to newsfeed.
#TODO: should I login user when email verified? review registration_aux where I log in user? what's the interplay
#among the two of them?
#  -> json {"result": "emailverification:OK", "email": "asdf@dasdf.com"}
@app.route('/registration_receive_emailverification/<token>')
def registration_receive_emailverification(token):
    if not confirm_token(token, 3600):
        jsondata = {"result": "The confirmation link is invalid or has expired"}
        return render_template('login/login.html', message=jsondata)
    if confirm_token(token, 3600):
        email = confirm_token(token)
        result_dict=_verifyEmail(email)
        if result_dict['result'] == 'OK' :
            #TODO: possibly redundant user_login: see function registration_aux
            ##user login
            #user = User(email)
            #flask_login.login_user(user)
            #flash ('email registered')
            jsondata = {
                "result": "emailverification:OK",
                "email": email
            }
            return render_template('login/login.html', message=jsondata)
        else:
            jsondata = {
                "result": result_dict['result']
            }
            #return redirect(url_for('.hello',message=jsondata))
            return render_template('login/login.html', message=jsondata)


#TODO: try with redirect instead of render_template
#input: URL token link from an invitation e-mail
#output: redirects to login with a json called "message"
#  -> json {"result": "The confirmation link is invalid or has expired"}
#  -> json {"result": "invitation:OK", "current_email": "guestemail@com", "host_email": host_email@com"}
@app.route('/registration_from_invitation/<token>/<guest_email>')
def registration_from_invitation(token, guest_email):
    if not confirm_token(token, 10000):
        jsondata = {"result": "The confirmation link is invalid or has expired"}
        return render_template('login/login.html', message=jsondata)
    if confirm_token(token, 10000):
        host_email = confirm_token(token)
        jsondata = {
            "result": "invitation:OK",
            "current_email": guest_email,
            "host_email": host_email
        }
        return render_template('login/login.html', message=jsondata)


@app.route('/registration_send_invitation/<host_email>/<guest_email>', methods=['GET'])
def registration_send_invitation(host_email, guest_email):
    token = generate_confirmation_token(host_email)
    confirm_url = url_for('.registration_from_invitation', token=token, guest_email=guest_email, _external=True)
    html = render_template('login/invitation_email.html', confirm_url=confirm_url)
    subject = ''.join([getFullNameByEmail(host_email), " invites you to join Consensus"])
    send_email(guest_email, subject, html)
    return jsonify({'result': 'email sent'})

#TODO: format for timestamp!
#input json {"user_email":"asd@asd.com", "idea_proposal":"let's do this", "vote_timestamp":"time", "vote_type":"supports/rejects"}
#output json  {"result" : "Success : User vote was added"}
#             {"result" : "Failure : idea or participant non existings"}
#             {"result" : "Failure : User vote exists already"}
@app.route('/vote_on_idea',methods=['POST'])
def vote_on_idea():
   return vote_on_idea_aux(request.get_json())








############################################
#####   API
############################################


@app.route('/')
def hello(message=None):
    return render_template('login/login.html',message=message)


#PARTICIPANTS

#input: json {"email":"asdf@asdf", "password":"MD5password"}
#output:
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


#input: email to be verified as an argument
#output: e-mail to the email account with a URL token link for email verification
#         and json {"result": "email sent"}
@app.route('/registration_send_emailverification/<email>')
def registration_send_emailverification(email):
    token = generate_confirmation_token(email)
    confirm_url = url_for('.registration_receive_emailverification', token=token, _external=True)
    html = render_template('login/verification_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(email, subject, html)
    return jsonify({'result': 'email sent'})


#input: json {"fullname":"Juan Lopez","email": "jj@gmail.com", "username": "jlopezvi",
#              "position": "employee", "group": "IT", "password": "MD5password",
#              "image_url": "http://.... ", "ifpublicprofile": true / false,
#              "host_email": "asdf@das" / null, "ifemailverified": true / false}
#       file  file.tar.gz
# multipart/form-data : curl -F "metadata=<metadata.json" -F "file=@my-file.tar.gz" http://example.com/add-file
#output:
#     -> NOT USED BY FRONTEND json {"result": "participant already exists""}
#     -> login and json {"result": "email not verified"} (on registration pending of email verification)
#     -> login and json {"result": "OK"} (on registration completed)
@app.route('/registration', methods=['POST'])
def registration():
    #call with json_data converted to python_dictionary_data
    inputdict=request.get_json()
    profilepic_file_body=None
    profilepic_file_body=request.files['fileUpload']
    print('b')
    #if request.args['files']:
    #    profilepic_file_body = request.args['files'][0]
    return registration_aux(inputdict,profilepic_file_body)

#return: Full Name (normal string) corresponding to e-mail
@app.route('/getFullNameByEmail/<email>', methods=['GET'])
def getFullNameByEmail(email):
    return getFullNameByEmail_aux(email)


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



#COMMUNITIES (NOT USED)
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
       


##ERROR HANDLERS
#@app.errorhandler(NotFoundError)
#def handle_NotFoundError(error):
#    response = jsonify(error.to_dict())
#    response.status_code = error.status_code
#    return response





if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if os.environ.get('GRAPHENEDB_URL'):
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(host='127.0.0.1', port=port)
