import os

from flask import Flask,jsonify,json, flash
from crossdomain import crossdomain
from flask import request,render_template,redirect,url_for
import ast
import json
from communityManager import saveCommunity,deleteCommunity,addCommunityToContact,getCommunities
from participantManager import _get_participant_node, remove_user_aux, get_all_participants_aux, \
    get_participant_followers_info_aux,get_participant_followings_info_aux,\
    get_fullname_for_participant_aux, registration_aux, get_participant_data_aux, modify_user_data_aux, \
    get_participant_data_by_email_unrestricted_aux, get_all_public_participants_aux, if_participant_exists_by_email_aux, \
    add_following_contact_to_user_aux, remove_following_contact_to_user_aux
from participantManager import get_participantnotifications_for_user_aux, remove_notification_from_participant1_to_participant2_aux
from ideaManager import get_ideas_data_created_by_participant_aux, get_ideas_created_by_participant_aux,\
     get_idea_data_aux, add_idea_to_user_aux, deleteOneIdea,getAllIdeas, \
    _getIdeaByIdeaIndex, vote_on_idea_aux, modify_idea_aux, remove_idea_aux, \
    _get_supporters_emails_for_idea_aux, _get_volunteers_emails_for_idea_aux, \
    _get_vote_statistics_for_idea
from ideaManager import get_ideanotifications_for_user_aux, remove_notification_from_idea_to_participant_aux, \
    _do_tasks_for_idea_editedproposal
from webManager import ideas_for_newsfeed_aux, ideas_for_home_aux, registration_receive_emailverification_aux, \
    registration_from_invitation_aux, registration_send_invitation_aux, do_cron_tasks_aux, _verifyEmail

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


# input:  application/x-www-form-urlencoded
#        (file) profilepic_file_body
#   (data dictionary): fullname=Juan Lopez&email=jj@gmail.com&username=jlopezvi
#                       &position=employee&group=IT&password=MD5password
#                       &host_email=asdf@das/None&ifpublicprofile=True/False
#                       &ifregistrationfromemail=True/False
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
    profilepic_file_body = None
    inputdict = request.form.to_dict()
    # translation of data to a python dictionary, with True, False, and None
    if inputdict['ifpublicprofile'] == 'True': inputdict['ifpublicprofile'] = True
    if inputdict['ifpublicprofile'] == 'False': inputdict['ifpublicprofile'] = False
    if inputdict['ifregistrationfromemail'] == 'True': inputdict['ifregistrationfromemail'] = True
    if inputdict['ifregistrationfromemail'] == 'False': inputdict['ifregistrationfromemail'] = False
    if inputdict['host_email'] == 'None': inputdict['host_email'] = None
    # if profilepic :
    if 'fileUpload' in request.files:
        profilepic_file_body = request.files['fileUpload']
    return registration_aux(inputdict,profilepic_file_body)


#TODO  multipart/form-data   or   application/x-www-form-urlencoded ?
# input:   user_email  (user logged in)
#          multipart/form-data   or   application/x-www-form-urlencoded ?
#        (file) profilepic_file_body
#     (data dictionary): {"fullname":"Juan Lopez", "new_email": "new_email@gmail.com",
#                       "username": "jlopezvi",
#                       "position": "employee", "group": "IT", "password": "MD5password",
#                       "ifpublicprofile": "True"/ "False", "ifsupportingproposalsvisible" : "True"/"False",
# 			            "ifrejectingproposalsvisible" : "True"/"False"
#           		    }
# Output: json
#           1. {'result': 'Wrong: New e-mail already exists'}
# 	        2. {'result': 'OK'}
@app.route('/modify_user_data', methods=['PUT'])
@app.route('/modify_user_data/<user_email_DEBUG>', methods=['PUT'])
def modify_user_data(user_email_DEBUG=None):
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id

    profilepic_file_body = None
    if 'fileUpload' in request.files:
        profilepic_file_body = request.files['fileUpload']

    inputdict = request.form.to_dict()
    # translation of data to a python dictionnary, with True, False, and None
    if 'ifpublicprofile' in inputdict:
        if inputdict['ifpublicprofile'] == 'True': inputdict['ifpublicprofile'] = True
        if inputdict['ifpublicprofile'] == 'False': inputdict['ifpublicprofile'] = False
    if 'ifsupportingproposalsvisible' in inputdict:
        if inputdict['ifsupportingproposalsvisible'] == 'True': inputdict['ifsupportingproposalsvisible'] = True
        if inputdict['ifsupportingproposalsvisible'] == 'False': inputdict['ifsupportingproposalsvisible'] = False
    if 'ifrejectingproposalsvisible' in inputdict:
        if inputdict['ifrejectingproposalsvisible'] == 'True': inputdict['ifrejectingproposalsvisible'] = True
        if inputdict['ifrejectingproposalsvisible'] == 'False': inputdict['ifrejectingproposalsvisible'] = False
    if 'host_email' in inputdict:
        if inputdict['host_email'] == 'None': inputdict['host_email'] = None
    #
    return modify_user_data_aux(inputdict, profilepic_file_body, user_email)


# input:   user_email  (user logged in)
# output: json {"result": "OK"/"Wrong"}
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
#       1.  return jsonify({"result":"OK", "ifallowed":true, "participant_data": participant_data })
#        participant_data:
#        {
#            'id': 'email',
#            'profilepic_url': 'assets/profile/perfil-mediano.png',
#            'username': 'John',
#            'fullname': 'Juan J. Lopez Villarejo',
#            'ideas_num': 5,
#            'followers_num': 5,
#            'followings_num': 2
#        }
#       2.  return jsonify({"result":"OK", "ifallowed":false, "participant_data": {} })
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
#            'profilepic_url': 'assets/profile/perfil-mediano.png',
#            'username': 'John',
#            'fullname': 'Juan J. Lopez Villarejo',
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


# Input: participant's email, user's email (user logged in)
# Output: json  [2 possibilities, according to privacy restrictions]
#       1.{"result":"OK", "ifallowed": True,
# 		   "followers_num": 1,
#  		   "followers_info": [
# 		    {
# 		      "email": "ale@gmail.com",
# 		      "fullname": "alejandro perez",
# 		      "username": "ale",
#             "profilepic_url": "http://path"
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
#             "profilepic_url": "http://path"
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


# TODO: DEBUG
@app.route('/get_all_participants_DEBUG', methods=['GET','OPTIONS'])
def get_all_participants_DEBUG():
    return json.dumps(get_all_participants_aux())

# Output  json {"email": "new@gmail.com", "position": "Employee", "group": "IT",
#               "fullname": "jlopezvi", "profilepic_url":'example.jpg', "if_following":True/False}
@app.route('/get_all_public_participants', methods=['GET'])
def get_all_public_participants():
    user = flask_login.current_user.id
    return json.dumps(get_all_public_participants_aux(user))


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
#           application/x-www-form-urlencoded :
#           (file) ideapic_file_body
#       (data dictionary):  concern=we are not social enough in the office&
#                           proposal=social coffee pause at 4 p.m.&
#       	                moreinfo_concern=I have to say as well this and this and this about the concern...&
#                           moreinfo_proposal=I have to say as well this and this and this about the proposal...&
#                           supporters_goal_num=500&volunteers_goal_num=5
#                           &if_author_public=True/False&first_receivers_emails=asdf@asd.com bdsd@sds.com dssa@gmail.com
#    output: json {"result":"OK", "result_msg":"added idea to database"}
#                 {"result":"Wrong", "result_msg":"proposal already exists"}
@app.route('/add_idea_to_user', methods=['POST'])
@app.route('/add_idea_to_user/<string:user_email_DEBUG>', methods=['POST'])
def add_idea_to_user(user_email_DEBUG=None) :
    if DEBUG and user_email_DEBUG is not None:
        user_email = user_email_DEBUG
    else:
        user_email = flask_login.current_user.id
    ideapic_file_body = None
    idea_dict = request.form.to_dict()
    # translation of data to a python dictionary, with integers
    if 'supporters_goal_num' in idea_dict: idea_dict['supporters_goal_num'] = int(idea_dict.get('supporters_goal_num'))
    if 'volunteers_goal_num' in idea_dict: idea_dict['volunteers_goal_num'] = int(idea_dict.get('volunteers_goal_num'))
    if idea_dict['if_author_public'] == 'True': idea_dict['if_author_public'] = True
    if idea_dict['if_author_public'] == 'False': idea_dict['if_author_public'] = False
    idea_dict['first_receivers_emails'] = idea_dict['first_receivers_emails'].split()
    #
    if 'fileUpload' in request.files:
        ideapic_file_body = request.files['fileUpload']
    return add_idea_to_user_aux(user_email,idea_dict,ideapic_file_body)


#   input:  application/x-www-form-urlencoded :
#           (file) ideapic_file_body
#       (data dictionary):  {"concern" :"we are not social enough in the office",
#                            "current_proposal": "this is the proposal to be modified",
#                            "proposal": "this is the new proposal (if is required)",
#                            "moreinfo_concern":"I have to say as well this and this and this...",
#                            "moreinfo_proposal":"I have to say as well this and this and this...",
#                            "supporters_goal_num": 500, "volunteers_goal_num": 5}
#   Output json :  1./ {"result":"OK", "result_msg":"Idea was modified"}
#    	           2./ {"result":"Wrong", "result_msg": "Proposal already exists"}
@app.route('/modify_idea', methods=['PUT'])
def modify_idea():
    ideapic_file_body = None
    idea_dict = request.form.to_dict()
    # translation of data to a python dictionary, with integers
    if 'supporters_goal_num' in idea_dict: idea_dict['supporters_goal_num'] = int(idea_dict.get('supporters_goal_num'))
    if 'volunteers_goal_num' in idea_dict: idea_dict['volunteers_goal_num'] = int(idea_dict.get('volunteers_goal_num'))
    #
    if 'fileUpload' in request.files:
        ideapic_file_body = request.files['fileUpload']
    return modify_idea_aux(idea_dict, ideapic_file_body)


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
#     "ideas_data": [
#      {
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
#      },
#      { ... }
#      ]
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


#input   idea_proposal
#output   idea data as a json
@app.route('/get_idea_data_DEBUG/<idea_proposal>', methods=['GET'])
def get_idea_data_DEBUG(idea_proposal):
    idea = _getIdeaByIdeaIndex(idea_proposal)
    return get_idea_data_aux(idea)


#input   idea_proposal
#output  {"result": "OK", "vote_statistics" : [supporters_num, rejectors_num, passives_num, volunteers_num]}
@app.route('/get_vote_statistics_for_idea/<idea_proposal>', methods=['GET'])
def get_vote_statistics_for_idea(idea_proposal):
    vote_statistics = _get_vote_statistics_for_idea(idea_proposal)
    return jsonify({"result": "OK", "vote_statistics" : vote_statistics})


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

# TODO
@app.route('/getConcerns/<string:current>', methods=['GET', 'OPTIONS'])
def getConcerns(current):
    print (current)
    return json.dumps(getAllConcerns(current))


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
#    {
#      "author_email": "new1@hotmail.com",
#      "author_photo_url": "",
#      "author_username": "new1",
#      "concern": "this is mi new concern for test",
#      "timestamp": "01.10.2016",
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
#      "timestamp": "01.10.2016",
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
#  ]
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
#    {
#      "author_email": "adavidsole@gmail.com",
#      "author_username": "alexdsole",
#      "concern": "Concern",
#      "timestamp": "01.10.2016",
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
#      "timestamp": "01.10.2016",
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
