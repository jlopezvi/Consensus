import os

from flask import Flask,jsonify,json, flash
from crossdomain import crossdomain
from flask import request,render_template,redirect,url_for
import ast
import json
from communityManager import saveCommunity,deleteCommunity,addCommunityToContact,getCommunities
from participantManager import _get_participant_node, remove_user_aux, get_all_participants_admin_aux, \
    get_participant_followers_info_aux,get_participant_followings_info_aux, get_fullname_for_participant_unrestricted_aux,\
    get_fullname_for_participant_aux, registration_aux, get_participant_data_aux, modify_user_data_aux,  \
    get_participant_data_by_email_unrestricted_aux, get_all_public_participants_for_user_aux, if_participant_exists_by_email_aux, \
    add_following_contact_to_user_aux, remove_following_contact_to_user_aux, get_user_data_aux, modify_user_password_aux
from participantManager import get_participantnotifications_for_user_aux, remove_notification_from_participant1_to_participant2_aux
from ideaManager import get_ideas_data_created_by_participant_aux, get_ideas_created_by_participant_aux,\
    add_idea_to_user_aux, vote_on_idea_aux, modify_idea_aux, remove_idea_aux, _get_supporters_emails_for_idea_aux, \
    _get_volunteers_emails_for_idea_aux, get_vote_statistics_for_idea_aux, get_voting_rel_between_user_and_idea_aux, \
    redflag_idea_aux, get_all_ideas_admin_aux, get_idea_data_admin_aux, get_idea_node_data_aux
from ideaManager import get_ideanotifications_for_user_aux, remove_notification_from_idea_to_participant_aux, \
    _do_tasks_for_idea_editedproposal
from webManager import ideas_for_newsfeed_aux, ideas_for_home_aux, registration_receive_emailverification_aux, \
    registration_from_invitation_aux, registration_send_invitation_aux, do_cron_tasks_aux, get_topten_ideas_aux

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
DEBUG=False
try:
    os.environ['APP_SETTINGS']
    app.config.from_object(os.environ['APP_SETTINGS'])
    DEBUG = app.config['DEBUG']
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

@app.route('/test')
def test():
    return url_for('static', filename='images/ideas/a.jpg')


@app.route('/do_tasks_for_idea_editedproposal_TEST/<idea_index>', methods=['POST'])
def do_tasks_for_idea_editedproposal_TEST(idea_index):
    return _do_tasks_for_idea_editedproposal(idea_index)


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
    user_email = flask_login.current_user.id
    message = {"user": user_email}
    return render_template('login/newsfeed.html', message = message)


@app.route('/home')
@flask_login.login_required
#user_email=flask_login.current_user.id
def home():
    user_email = flask_login.current_user.id
    message = {"user": user_email}
    return render_template('home.html', message = message)


@app.route('/participants')
@app.route('/participants/<participant_email>')
@flask_login.login_required
def participants(participant_email=None):
    user_email = flask_login.current_user.id
    message = {"user": user_email, "participant": participant_email}
    return render_template('participants.html', message = message)


@app.route('/topten')
@flask_login.login_required
def topten():
    user_email = flask_login.current_user.id
    message = {"user": user_email}
    return render_template('topten.html', message = message)


##############
# PARTICIPANT MANAGER
##############


# input: json {"email":"asdf@asdf", "password":"MD5password"}
# output:
#   json {"result":"Wrong: Bad e-mail"} / json {"result": "Wrong: Bad password"}
#           / login and json {"result": "OK"}
@app.route('/login', methods=['POST'])
def login():
    login = request.get_json(force=True)
    user_to_check=_get_participant_node(login['email'])
    if user_to_check is None :
        return jsonify({"result":"Wrong: Bad e-mail"})
    if login['password'] == user_to_check['password']:
        user = User(login['email'])
        flask_login.login_user(user)
        return jsonify({"result": "OK"})
    else:
        return jsonify({"result": "Wrong: Bad password"})


# input: user_index logged in
# output:  json  {"result": "OK"}
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return jsonify({"result": "OK"})


# input:  application/json
#                      {"fullname":"Juan Lopez","email":"jj@gmail.com", "username": "jlopezvi",
#                       "position":"employee", "group":"IT", "password":"MD5password",
#                       "host_email":"asdf@das"/null, "ifpublicprofile":true/false,
#                       "ifregistrationfromemail":true/false, "profilepic": "base64_string"/null}
# output: json
#          1. Wrong (participant registered already!)
#                       {"result":"Wrong","ifemailexists":true,"ifemailexists_msg":"message"}
#          2. OK (participant registered already but e-mail not verified yet. Sends new e-mail for verification)  -->
#                       {"result": "OK: Participant registered previously, resend email verification",
#                        "ifemailexists":true, "ifemailexists_msg":"message",
#                        "ifemailverified":false,"ifemailverified_msg":"message"}
#          3. OK (4 different normal cases of registration)
#                       {"result":"OK", "ifhost":true/false,"ifhost_msg":"message",
#                       "ifemailverified":true/false,"ifemailverified_msg":"message"})
#             *Note: when "ifemailverified" is "true", the user is logged in
#             *Note: when "ifemailverified" is "false", a verification e-mail is sent
#             *Note: when "ifhost" is "true", the user starts following the host.
@app.route('/registration', methods=['POST'])
def registration():
    inputdict = request.get_json()
    return registration_aux(inputdict)


# input:      user_email (user logged in)
#             application/json   ALL FIELDS ARE OPTIONAL !
#                      {"fullname": "Juan Lopez", "new_email": "new_email@gmail.com",
#                       "username": "jlopezvi",
#                       "position":"employee", "group": "IT", "password": "MD5password",
#                       "ifpublicprofile": true/false,, "ifsupportingproposalsvisible" : true/false,
#                       "ifrejectingproposalsvisible" : true/false, "profilepic": "base64_string"/null
#                       }
# Output: json
#           1. {'result': 'Wrong: New e-mail already exists'}
#           2. {'result': 'OK'}
@app.route('/modify_user_data', methods=['PUT'])
@app.route('/modify_user_data/<user_email_DEBUG>', methods=['PUT'])
def modify_user_data(user_email_DEBUG=None):
   if DEBUG and user_email_DEBUG is not None:
       user_email = user_email_DEBUG
   else:
       user_email = flask_login.current_user.id
   inputdict = request.get_json()
   return modify_user_data_aux(inputdict, user_email)


# input:      user_email (user logged in)
#             application/json
#                      {"old_password": "asdf", "new_password": "ndls" }
# Output: json
#           1. {'result': 'Wrong: Wrong current password'}
#           2. {'result': 'OK'}
@app.route('/modify_user_password', methods=['PUT'])
@app.route('/modify_user_password/<user_email_DEBUG>', methods=['PUT'])
def modify_user_password(user_email_DEBUG=None):
   if DEBUG and user_email_DEBUG is not None:
       user_email = user_email_DEBUG
   else:
       user_email = flask_login.current_user.id
   inputdict = request.get_json()
   return modify_user_password_aux(inputdict, user_email)


# input:   user_email  (user logged in)
# Output:  application/json
#    {"result": "OK", "data": data}
#      data  =  {"fullname":"Juan Lopez", "email": "email@gmail.com",
#                "username": "jlopezvi",
#                "position": "employee", "group": "IT", "password": "MD5password",
#                "ifpublicprofile": true/false, "ifsupportingproposalsvisible" : true/false,
#                "ifrejectingproposalsvisible" : true/false, "profilepic_url": "static/.../pic.jpg"
#                }
@app.route('/get_user_data', methods=['GET'])
@app.route('/get_user_data/<user_email_DEBUG>', methods=['GET'])
def get_user_data(user_email_DEBUG=None):
   if DEBUG and user_email_DEBUG is not None:
       user_email = user_email_DEBUG
   else:
       user_email = flask_login.current_user.id
   return get_user_data_aux(user_email)


# input:   user_email  (user logged in)
# output: json {"result": "OK"}
@app.route('/remove_user', methods=['DELETE'])
@app.route('/remove_user/<user_email_DEBUG>', methods=['DELETE'])
def remove_user(user_email_DEBUG=None) :
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return remove_user_aux(user_email)


# input: participant_email: new@gmail.com,  user_email (user logged in)
# output: JSON      [2 possibilities, according to privacy restrictions]
#       1.  {"result":"OK", "ifallowed":true, "participant_data": participant_data }
#        participant_data:
#        {
#            'id': 'email',
#            'profilepic_url': 'static/.../pic.jpg',
#            'username': 'John',
#            'fullname': 'Juan J. Lopez Villarejo',
#            'ideas_num': 5,
#            'followers_num': 5,
#            'followings_num': 2
#        }
#       2.  {"result":"OK", "ifallowed":false, "participant_data": {} }
@app.route('/get_participant_data/<participant_email>')
@app.route('/get_participant_data/<participant_email>/<user_email_DEBUG>')
def get_participant_data(participant_email, user_email_DEBUG=None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return get_participant_data_aux(user_email, participant_email)


# input: participant_email: new@gmail.com
# output: json  {"result":"OK", "participant_data": participant_data }
#        participant_data:
#        {
#            'id': 'email',
#            'profilepic_url': 'static/.../pic.jpg',
#            'username': 'John',
#            'fullname': 'Juan J. Lopez Villarejo',
#            'position': 'assistant'
#            'group': 'Marketing'
#            'ideas_num': 5,
#            'followers_num': 5,
#            'followings_num': 2
#        }
@app.route('/get_participant_data_by_email_unrestricted/<participant_email>')
def get_participant_data_by_email_unrestricted(participant_email):
    return get_participant_data_by_email_unrestricted_aux(participant_email)


# input: email
# output: json {"result" : true / false }
@app.route('/if_participant_exists_by_email/<participant_email>')
def if_participant_exists_by_email(participant_email):
    return if_participant_exists_by_email_aux(participant_email)


# input: participant_email, user_email  (user logged in)
# output: json {"result": "OK", "ifallowed": ifallowed, "fullname": fullname}
@app.route('/get_fullname_for_participant/<participant_email>', methods=['GET'])
@app.route('/get_fullname_for_participant/<participant_email>/<user_email_DEBUG>', methods=['GET'])
def get_fullname_for_participant(participant_email, user_email_DEBUG=None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return get_fullname_for_participant_aux(participant_email, user_email)


# input: participant_email
# output: json {"result": "OK", "fullname": fullname}
@app.route('/get_fullname_for_participant_unrestricted/<participant_email>', methods=['GET'])
def get_fullname_for_participant_unrestricted(participant_email):
    return get_fullname_for_participant_unrestricted_aux(participant_email)


# Input: participant's email, user's email (user logged in)
# Output: json  [2 possibilities, according to privacy restrictions]
#       1.{"result":"OK", "ifallowed": True,
# 		   "followers_num": 1,
#  		   "followers_info": [
# 		    {
# 		      "email": "ale@gmail.com",
# 		      "fullname": "alejandro perez",
# 		      "username": "ale",
#             "profilepic_url": "static/.../pic.jpg"
# 		    }
# 		   ]
# 		  }
#       2.{"result":"OK", "ifallowed": False, "followers_num": 1, "followers_info": []}
@app.route('/get_participant_followers_info/<participant_email>', methods=['GET'])
@app.route('/get_participant_followers_info/<participant_email>/<user_email_DEBUG>', methods=['GET'])
def get_participant_followers_info(participant_email, user_email_DEBUG=None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return get_participant_followers_info_aux(participant_email, user_email)


# Input: participant's email, user's email (user logged in)
# Output: json  [2 possibilities, according to privacy restrictions]
#       1.{"result":"OK", "ifallowed": True,
# 		   "followings_num": 1,
#  		   "followings_info": [
# 		    {
# 		      "email": "ale@gmail.com",
# 		      "fullname": "alejandro perez",
# 		      "username": "ale",
#             "profilepic_url": "static/.../pic.jpg"
#  		    }
# 		   ]
# 		  }
#       2.{"result":"OK", "ifallowed": False, "followings_num": 1, "followings_info": []}
@app.route('/get_participant_followings_info/<participant_email>', methods=['GET'])
@app.route('/get_participant_followings_info/<participant_email>/<user_email_DEBUG>', methods=['GET'])
def get_participant_followings_info(participant_email, user_email_DEBUG=None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return get_participant_followings_info_aux(participant_email, user_email)


# input: followingcontact email, user email (user logged in)
# output: json  {"result": "OK"/"Wrong"}
@app.route('/add_following_contact_to_user/<followingcontact_email>', methods=['GET'])
@app.route('/add_following_contact_to_user/<followingcontact_email>/<user_email_DEBUG>', methods=['GET'])
def add_following_contact_to_user(followingcontact_email, user_email_DEBUG=None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return add_following_contact_to_user_aux(followingcontact_email, user_email)


# input: followingcontact email, user email (user logged in)
# output: json  {"result": "OK"/"Wrong"}
@app.route('/remove_following_contact_to_user/<followingcontact_email>', methods=['GET'])
@app.route('/remove_following_contact_to_user/<followingcontact_email>/<user_email_DEBUG>', methods=['GET'])
def remove_following_contact_to_user(followingcontact_email, user_email_DEBUG=None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return remove_following_contact_to_user_aux(followingcontact_email, user_email)


@app.route('/get_all_participants_admin', methods=['GET','OPTIONS'])
def get_all_participants_admin():
    return json.dumps(get_all_participants_admin_aux())


# Output  json {"email": "new@gmail.com", "position": "Employee", "group": "IT",
#               "fullname": "jlopezvi", "profilepic_url": "static/.../pic.jpg", "if_following":True/False}
@app.route('/get_all_public_participants_for_user', methods=['GET'])
def get_all_public_participants_for_user():
    user = flask_login.current_user.id
    return json.dumps(get_all_public_participants_for_user_aux(user))


##### PARTICIPANT NOTIFICATIONS

# TODO: test
# input:  [user logged in]
# output: json {"result": "OK", "data": notifications}) with
#       notifications = [
#                     {'notification_type': 'newfollower',
#                      'participant_index': participant_email },
#                     {   }
#                     ]
@app.route('/get_participantnotifications_for_user',methods=['GET'])
@app.route('/get_participantnotifications_for_user/<user_email_DEBUG>',methods=['GET'])
def get_participantnotifications_for_user(user_email_DEBUG):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return get_participantnotifications_for_user_aux(user_email)


# TODO: test
# input: json {"participant1_email":"asdf@asdf", "participant2_email":"asdf2@asdf",
#             "notification_type": "newfollower"}
# output:
#   json {"result": "OK", "result_msg": "Notification was deleted"} /
@app.route('/remove_notification_from_participant1_to_participant2',methods=['POST'])
def remove_notification_from_participant1_to_participant2():
    participant1_email = request.get_json()['participant1_email']
    participant2_email = request.get_json()['participant2_email']
    notification_type = request.get_json()['notification_type']
    return remove_notification_from_participant1_to_participant2_aux(participant1_email, participant2_email, notification_type)


###############
# IDEA MANAGER
###############


#   input:  user_email (user logged in)
#           application/json :
#                          {"concern":"we are not social enough in the office",
#                           "proposal":"social coffee pause at 4 p.m.",
#       	                "moreinfo_concern":"I have to say as well this and this and this about the concern...",
#                           "moreinfo_proposal":"I have to say as well this and this and this about the proposal...",
#                           "supporters_goal_num":500, "volunteers_goal_num":5,
#                           "image":"base64_string"/null,
#                           "if_author_public":true/false, "first_receivers_emails":["asdf@asd.com", "bdsd@sds.com"] }
#    output: json {"result":"OK", "result_msg":"added idea to database"}
#                 {"result":"Wrong", "result_msg":"proposal already exists"}
@app.route('/add_idea_to_user', methods=['POST'])
@app.route('/add_idea_to_user/<string:user_email_DEBUG>', methods=['POST'])
def add_idea_to_user(user_email_DEBUG=None) :
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    idea_dict = request.get_json()
    return add_idea_to_user_aux(user_email,idea_dict)


#   input:  application/json :  ALL FIELDS ARE OPTIONAL SAVE FOR  'current_proposal'!
#                          {"concern":"we are not social enough in the office",
#                           "current_proposal": "this is the proposal to be modified",
#                           "proposal": "this is the new proposal (if is required)",
#       	                "moreinfo_concern":"I have to say as well this and this and this about the concern...",
#                           "moreinfo_proposal":"I have to say as well this and this and this about the proposal...",
#                           "supporters_goal_num":500, "volunteers_goal_num":5,
#                           "image":"base64_string"/null,
#                           "if_author_public":true/false }
#   Output json :  1./ {"result":"OK", "result_msg":"Idea was modified"}
#    	           2./ {"result":"Wrong", "result_msg": "Proposal already exists"}
@app.route('/modify_idea', methods=['PUT'])
def modify_idea():
    idea_dict = request.get_json()
    return modify_idea_aux(idea_dict)


#   input:  json   {"proposal": "text of the proposal"}
#   Output json :  {"result":"OK", "result_msg":"Idea was removed"}
@app.route('/remove_idea', methods=['DELETE'])
def remove_idea():
    idea_index=request.get_json()['proposal']
    return remove_idea_aux(idea_index)


# Input: participant's email, user's email (user logged in)
# Output: json with fields "result","ifallowed":true/ false, "ideas_indices".
# "ideas_indices" contains a list [] with the indices for all the ideas created by the user
#  There are two possibilities according to privacy restrictions
# 1. {"result": "OK",
#     "ifallowed": true,
#     "ideas_indices": [proposal_of_idea_1, proposal_of_idea_2,...]
#     }
# 2. {
#    "result": "OK"
#    "ifallowed": false,
#    "ideas_indices": []
#    }
@app.route('/get_ideas_created_by_participant/<participant_email>', methods=['GET'])
@app.route('/get_ideas_created_by_participant/<participant_email>/<user_email>', methods=['GET'])
def get_ideas_created_by_participant(participant_email,user_email_DEBUG=None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return get_ideas_created_by_participant_aux(participant_email,user_email)


# Input: participant's email, user's email (user logged in)
# Output: json with fields "result","ifallowed":true/ false, "ideas_data".
# "ideas_data" contains list [] with json data {} for all the ideas created by the user
#  There are two possibilities according to privacy restrictions
# 1. {"result": "OK",
#     "ifallowed": true,
#     "ideas_data":
#          [
#            {
#             'concern': 'Some text for the concern',
#             'proposal': 'Some text for the proposal',
#             'image_url': 'static/.../asdf.JPG'/null,
#             'uuid': 'unique_identifier_string',
#             'moreinfo_concern': 'blah blah blah more info',
#             'moreinfo_proposal': 'blah blah blah more info',
#             'supporters_goal_num': 200,
#             'volunteers_goal_num': 5,
#             'if_author_public': true / false
#             'author_profilepic_url': 'static/.../pic.jpg'/null, 'author_username': 'daniela', 'author_email': 'a@gmail.com',
#             'duration' : "4 hours/ days/ weeks",
#             'supporters_num' : 5, 'volunteers_num' : 2, 'rejectors_num': 3,
#             'support_rate' : 95, 'support_rate_MIN' : 90,
#             'known_supporters': [
#                { 'email': 'user', 'username': 'me' }, { 'email': 'c@gmail.com', 'username': 'Pedro' }
#              ],
#             'known_rejectors':[
#                { 'email': 'd@', 'username': 'Elisa' }
#              ],
#             'vote_type': null / 'supported' / 'rejected' / 'ignored'
#             'vote_ifvolunteered': null / true / false
#            },
#            {
#              ...
#            }
#          ]
#    }
# 2. {
#    "result": "OK",
#    "ifallowed": false,
#    "ideas_data": []
#    }
@app.route('/get_ideas_data_created_by_participant/<participant_email>', methods=['GET'])
@app.route('/get_ideas_data_created_by_participant/<participant_email>/<user_email>', methods=['GET'])
def get_ideas_data_created_by_participant(participant_email,user_email_DEBUG=None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return get_ideas_data_created_by_participant_aux(participant_email,user_email)


# input   idea_proposal
# output  json {"result": "OK", "volunteers_emails": [email1, email2,...]}
@app.route('/get_volunteers_emails_for_idea/<idea_proposal>', methods=['GET'])
def get_volunteers_emails_for_idea(idea_proposal):
    volunteers_emails = _get_volunteers_emails_for_idea_aux(idea_proposal)
    return jsonify({"result": "OK", "volunteers_emails": volunteers_emails})


# input   idea_proposal
# output  json {"result": "OK", "supporters_emails": [email1, email2,...]}
@app.route('/get_supporters_emails_for_idea/<idea_proposal>', methods=['GET'])
def get_supporters_emails_for_idea(idea_proposal):
    supporters_emails = _get_supporters_emails_for_idea_aux(idea_proposal)
    return jsonify({"result": "OK", "supporters_emails": supporters_emails})


# input   idea_proposal
# output  {"result": "OK", "vote_statistics" : [supporters_num, rejectors_num, passives_num, volunteers_num]}
@app.route('/get_vote_statistics_for_idea/<idea_proposal>', methods=['GET'])
def get_vote_statistics_for_idea(idea_proposal):
    vote_statistics = get_vote_statistics_for_idea_aux(idea_proposal)
    return jsonify({"result": "OK", "vote_statistics" : vote_statistics})


# input:  user's email (flask_login.current_user.id), idea_proposal
# output: json  {"result": "OK", "vote_type":"supported/rejected/ignored", "vote_ifvolunteered":true/false}
#               {"result": "Wrong", "result_msg": "Voting relationship does not exist"}
@app.route('/get_voting_rel_between_user_and_idea/<idea_proposal>',methods=['GET'])
@app.route('/get_voting_rel_between_user_and_idea/<idea_proposal>/<user_email_DEBUG>',methods=['GET'])
def vote_status_idea(idea_proposal, user_email_DEBUG = None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return get_voting_rel_between_user_and_idea_aux(user_email, idea_proposal)


# TODO: format for vote_timestamp
# input   user's email (flask_login.current_user.id)
#         json {"idea_proposal":"let's do this",
#               "vote_type":"supported/rejected/ignored", "vote_ifvolunteered": true/false}
# output json  {"result": "Wrong: User vote exists of same type"}
#              {"result": "OK: User vote was modified"}
#              {"result": "OK: User vote was created"}
@app.route('/vote_on_idea',methods=['POST'])
@app.route('/vote_on_idea/<user_email_DEBUG>',methods=['POST'])
def vote_on_idea(user_email_DEBUG = None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return vote_on_idea_aux(user_email, request.get_json())


# input:   user's email (flask_login.current_user.id),
#          json {"idea_index":"let's do this",
#               "reason":"this and this"}
# output: jsonify({"result":"OK", "result_msg":"Idea was removed"})
@app.route('/redflag_idea',methods=['POST'])
@app.route('/redflag_idea/<user_email_DEBUG>',methods=['POST'])
def redflag_idea(user_email_DEBUG = None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    reason = request.get_json()['reason']
    idea_index = request.get_json()['idea_index']
    return redflag_idea_aux(user_email, idea_index, reason)


@app.route('/get_all_ideas_admin', methods=['GET','OPTIONS'])
def get_all_ideas_admin():
    return json.dumps(get_all_ideas_admin_aux())


# input   idea_proposal
# output   idea data as a json
@app.route('/get_idea_data_admin/<idea_proposal>', methods=['GET'])
def get_idea_data_admin(idea_proposal):
    return jsonify(get_idea_data_admin_aux(idea_proposal))


# input   idea_proposal
# output   idea_node's data as a json
@app.route('/get_idea_node_data/<idea_proposal>', methods=['GET'])
def get_idea_node_data(idea_proposal):
    return jsonify(get_idea_node_data_aux(idea_proposal))


##### IDEA NOTIFICATIONS

# TODO: test
# input:  [user logged in]
# output: json {"result": "OK", "data": notifications}) with
#       notifications = [
#                     {'notification_type': 'failurewarning'/'successful'/'sucessful_to_author'/'edited',
#                      'idea_index': idea_proposal },
#                     {   }
#                     ]
@app.route('/get_ideanotifications_for_user',methods=['GET'])
@app.route('/get_ideanotifications_for_user/<user_email_DEBUG>',methods=['GET'])
def get_ideanotifications_for_user(user_email_DEBUG):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return get_ideanotifications_for_user_aux(user_email)


# TODO: test
# input: json {"participant_email":"asdf@asdf", "proposal":"this is a proposal",
#             "notification_type": "failurewarning"/"successful"/"sucessful_to_author"/"edited"}
# output:
#   json {"result": "OK", "result_msg": "Notification was deleted"} /
@app.route('/remove_notification_from_idea_to_participant',methods=['POST'])
def remove_notification_from_idea_to_participant():
    participant_email = request.get_json()['participant_email']
    idea_index = request.get_json()['proposal']
    notification_type = request.get_json()['notification_type']
    return remove_notification_from_idea_to_participant_aux(participant_email, idea_index, notification_type)



##############
# WEB MANAGER
##############


# TODO: try with redirect instead of render_template
# input: URL token link from an invitation e-mail and that (guest) e-mail
# output: redirects to login with a json called "message"
#  -> json {"type": "registration", "result": "Wrong", "result_msg": "The confirmation link is invalid or has expired"}
#  -> json {"type": "registration", "result": "OK : With data", "result_msg": "Invitation OK",
#            "user_email": "guestemail@com", "host_email": host_email@com"}
@app.route('/registration_from_invitation/<token>/<guest_email>')
def registration_from_invitation(token, guest_email):
    return registration_from_invitation_aux(token, guest_email)


# input: host_email and guest_email
# output: sends registration e-mail and json
#         {"result": "OK", "result_msg" : "email sent"}
@app.route('/registration_send_invitation/<host_email>/<guest_email>', methods=['GET'])
def registration_send_invitation(host_email, guest_email):
    return registration_send_invitation_aux(host_email, guest_email)


# TODO: try with redirect instead of render_template
# input: URL token link from an invitation e-mail
# output: redirects to login with a json called "message"
#  -> json {"type": "login", "result": "Wrong", "result_msg": "The confirmation link is invalid or has expired"}
#  -> json {"type": "login", "result": "Wrong", "result_msg": "Email already verified"}
#  -> json {"type": "login", "result": "Wrong", "result_msg": "Email not registered"}
#  -> json {"type": "login", "result": "OK : With data", "result_msg": "Email verified", "login_email": "asdf@dasdf.com"}
@app.route('/registration_receive_emailverification/<token>')
def registration_receive_emailverification(token):
    return registration_receive_emailverification_aux(token)


# TODO: add weights for ideas
# Get Ideas For Newsfeed
# Input: user_email   (user logged in)
# Output: json with fields 'result' and 'data'. 'data' contains array with all ideas that the user has not << VOTED_ON >>
# {"result": "OK",
#  "data": [
#            {
#             'concern': 'Some text for the concern',
#             'proposal': 'Some text for the proposal',
#             'image_url': 'static/.../asdf.JPG'/null,
#             'uuid': 'unique_identifier_string',
#             'moreinfo_concern': 'blah blah blah more info',
#             'moreinfo_proposal': 'blah blah blah more info',
#             'supporters_goal_num': 200,
#             'volunteers_goal_num': 5,
#             'if_author_public': true / false
#             'author_profilepic_url': 'static/.../pic.jpg'/null, 'author_username': 'daniela', 'author_email': 'a@gmail.com',
#             'duration' : "4 hours/ days/ weeks",
#             'supporters_num' : 5, 'volunteers_num' : 2, 'rejectors_num': 3,
#             'support_rate' : 95, 'support_rate_MIN' : 90,
#             'known_supporters': [
#                { 'email': 'user', 'username': 'me' }, { 'email': 'c@gmail.com', 'username': 'Pedro' }
#              ],
#             'known_rejectors':[
#                { 'email': 'd@', 'username': 'Elisa' }
#              ],
#             'vote_type': null / 'supported' / 'rejected' / 'ignored'
#             'vote_ifvolunteered': null / true / false
#            },
#            {
#              ...
#            }
#          ]
# }
@app.route('/ideas_for_newsfeed',methods=['GET'])
@app.route('/ideas_for_newsfeed/<user_email_DEBUG>',methods=['GET'])
def ideas_for_newsfeed(user_email_DEBUG = None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return ideas_for_newsfeed_aux(user_email)


# Ideas For Home: See the Supported + Volunteered ideas/ See the ignored ideas / See the rejected ideas
# Input: user_email (user logged in) and JSON {"vote_type": "rejected/supported/ignored"}
# Output: json with fields 'result' and 'data'. 'data' Array with all ideas that the user has voted according to << vote_type >>
# {"result": "OK",
#  "data": [
#            {
#             'concern': 'Some text for the concern',
#             'proposal': 'Some text for the proposal',
#             'image_url': 'static/.../asdf.JPG'/null,
#             'uuid': 'unique_identifier_string',
#             'moreinfo_concern': 'blah blah blah more info',
#             'moreinfo_proposal': 'blah blah blah more info',
#             'supporters_goal_num': 200,
#             'volunteers_goal_num': 5,
#             'if_author_public': true / false
#             'author_profilepic_url': 'static/.../pic.jpg'/null, 'author_username': 'daniela', 'author_email': 'a@gmail.com',
#             'duration' : "4 hours/ days/ weeks",
#             'supporters_num' : 5, 'volunteers_num' : 2, 'rejectors_num': 3,
#             'support_rate' : 95, 'support_rate_MIN' : 90,
#             'known_supporters': [
#                { 'email': 'user', 'username': 'me' }, { 'email': 'c@gmail.com', 'username': 'Pedro' }
#              ],
#             'known_rejectors':[
#                { 'email': 'd@', 'username': 'Elisa' }
#              ],
#             'vote_type': null / 'supported' / 'rejected' / 'ignored'
#             'vote_ifvolunteered': null / true / false
#            },
#            {
#              ...
#            }
#          ]
# }
@app.route('/ideas_for_home',methods=['POST'])
@app.route('/ideas_for_home/<user_email_DEBUG>',methods=['POST'])
def ideas_for_home(user_email_DEBUG = None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    #
    vote_type = request.get_json()['vote_type']
    return ideas_for_home_aux(user_email, vote_type)


# Input:  None
# Output: json with fields 'result' and 'data'. 'data' Array with at most 10 ideas ranked from 1st to 10st in order
# {"result": "OK",
#  "data": [
#            {
#             'concern': 'Some text for the concern',
#             'proposal': 'Some text for the proposal',
#             'image_url': 'static/.../asdf.JPG'/null,
#             'uuid': 'unique_identifier_string',
#             'moreinfo_concern': 'blah blah blah more info',
#             'moreinfo_proposal': 'blah blah blah more info',
#             'supporters_goal_num': 200,
#             'volunteers_goal_num': 5,
#             'if_author_public': true / false
#             'author_profilepic_url': 'static/.../pic.jpg'/null, 'author_username': 'daniela', 'author_email': 'a@gmail.com',
#             'duration' : "4 hours/ days/ weeks",
#             'supporters_num' : 5, 'volunteers_num' : 2, 'rejectors_num': 3,
#             'support_rate' : 95, 'support_rate_MIN' : 90,
#             'known_supporters': [
#                { 'email': 'user', 'username': 'me' }, { 'email': 'c@gmail.com', 'username': 'Pedro' }
#              ],
#             'known_rejectors':[
#                { 'email': 'd@', 'username': 'Elisa' }
#              ],
#             'vote_type': null / 'supported' / 'rejected' / 'ignored'
#             'vote_ifvolunteered': null / true / false
#            },
#            {
#              ...
#            }
#          ]
# }
@app.route('/get_topten_ideas',methods=['GET'])
@app.route('/get_topten_ideas/<user_email_DEBUG>',methods=['GET'])
def get_topten_ideas(user_email_DEBUG = None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    return get_topten_ideas_aux(user_email)


# input : None
# output: JSON    {"result":"OK", "ideas_removed" : [ "proposal1", "proposal2"]}
@app.route('/do_cron_tasks')
def do_cron_tasks():
    return do_cron_tasks_aux()






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
