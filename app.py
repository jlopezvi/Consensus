import os

from flask import Flask,jsonify,json
from crossdomain import crossdomain
from flask import request,render_template,redirect,url_for
import ast
import json
from communityManager import saveCommunity,deleteCommunity,addCommunityToContact,getCommunities
from participantManager import _getParticipantByEmail,deleteParticipant,getAllParticipants, \
    addFollowingContactToParticipant_aux,getFollowerContacts,getFollowingContacts,getFullNameByEmail_aux,\
    registration_aux,_verifyEmail
from ideaManager import Idea, addIdeaToUser_aux,deleteOneIdea,getAllIdeas, spreadIdeaToFollowers_aux, \
    _getIdeaByIdeaIndex
from webManager import newsfeed2_aux
import logging
import flask_login
from user_authentification import User

#logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

#flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = 'super secret string'  # Change this!
@login_manager.user_loader
def user_loader(email):
    return User(email)

#@login_manager.unauthorized_handler
#def unauthorized_handler():
 #   return 'Unauthorized'

#input: json {"email":"asdf@asdf", "password":"MD5password"}
#output:
#   json {"result":"Bad e-mail"} / json {"result": "Bad password"}
#   / login cookie and redirection to '/newsfeed'
@app.route('/login2', methods=['POST','GET'])
def login2():
    if request.method == 'GET':
        return '''
               <form action='login2' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='password' id='password' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = request.form['email']
    user_to_check=_getParticipantByEmail(email)
    if user_to_check is None :
        return jsonify(result ="Bad e-mail")

    if request.form['password'] == user_to_check['password']:
        user = User(email)
        flask_login.login_user(user)
        return redirect(url_for('newsfeed2'))
    else:
        return jsonify(result="Bad password")

#input: json {"email":"asdf@asdf", "password":"MD5password"}
#output:
#   json {"result":"Bad e-mail"} / json {"result": "Bad password"}
#   / login cookie and redirection to '/newsfeed'
@app.route('/login', methods=['POST'])
def login():
    login = request.get_json(force=True)
    return jsonify(login)
    '''
    user_to_check=_getParticipantByEmail(login['email'])
    if user_to_check is None :
        return jsonify(result ="Bad e-mail")

    if login['password'] == user_to_check['password']:
        user = User(login['email'])
        flask_login.login_user(user)
        return redirect(url_for('newsfeed2'))
    else:
        return jsonify(result="Bad password")
    '''

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@app.route('/')
def hello():
    return render_template('login/login.html')


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
#     "supporters_goal": 500, "volunteers_goal": 5}
@app.route('/addIdeaToUser/<string:user_email>', methods=['POST'])
def addIdeaToUser(user_email) :
    idea_dict = request.get_json()
    idea_object = Idea(idea_dict)
    return addIdeaToUser_aux(user_email, idea_object)


@app.route('/newsfeed2')
@flask_login.login_required
def newsfeed2():
    print('Logged in as: ' + flask_login.current_user.id)
    return newsfeed2_aux(flask_login.current_user.id)


@app.route('/newsfeed')
#@flask_login.login_required
def newsfeed():
    #print('Logged in as: ' + flask_login.current_user.id)
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
        _getParticipantByEmail(host_email)
    return render_template('signUp.html',host_email=host_email)



#API

#input: email to be verified as an argument
#output: e-mail to the email account with a URL link for email verification
@app.route('/registration_send_emailverification/<email>')
def registration_send_emailverification(email):
    pass

#input: URL from an invitation e-mail with email to be verified
#output: redirects to login page with message in json {"verified_email":"asd@asdf"}
@app.route('/registration_receive_emailverification/<email>')
def registration_receive_emailverification(email):
    _verifyEmail(email)
    jsondata = jsonify({'verified_email': email})
    return redirect(url_for('.hello', message=jsondata))

#input: URL from an invitation e-mail with guest_email and host_email
#output: redirects to login page with message in json {"current_email":"asd@asdf","host_email":"bd@asdf"}
@app.route('/registration_from_invitation/<current_email>/<host_email>', methods=['GET'])
def registration_from_invitation(current_email,host_email):
    jsondata = jsonify({
        'current_email': current_email,
        'host_email': host_email
    })
    return redirect(url_for('.hello', message=jsondata))

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
    print(request.get_json())
    return registration_aux(request.get_json())

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
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=port)