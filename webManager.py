from participantManager import _get_participant_node, _get_fullname_for_participant
from ideaManager import get_idea_data_aux, remove_idea_aux
from utils import getGraph, send_email #, send_email_new
from flask import jsonify, render_template, url_for
from uuid_token import generate_confirmation_token, confirm_token
from datetime import datetime


def registration_from_invitation_aux(token, guest_email):
    if not confirm_token(token, 10000):
        jsondata = {"type": "registration", "result": "Wrong", "result_msg": "The confirmation link is invalid or has expired"}
        return render_template('login/login.html', message=jsondata)
    if confirm_token(token, 10000):
        host_email = confirm_token(token)
        jsondata = {
            "result": "OK : With data", "result_msg": "Invitation OK",
            "user_email": guest_email,
            "host_email": host_email
        }
        return render_template('login/login.html', message=jsondata)


# MAIL with Flask
def registration_send_invitation_aux(host_email, guest_email):
    token = generate_confirmation_token(host_email)
    confirm_url = url_for('.registration_from_invitation', token=token, guest_email=guest_email, _external=True)
    html = render_template('login/invitation_email.html', confirm_url=confirm_url)
    subject = ''.join([_get_fullname_for_participant(host_email), " invites you to join Consensus"])
    send_email(guest_email, subject, html)
    return jsonify({"result": "OK", "result_msg": "email sent"})


# MAIL with Python
# TODO : choose a mail method
# def registration_send_invitation_aux(host_email, guest_email):
#     send_email_new(host_email, 'invitation', guest_email)


def registration_receive_emailverification_aux(token):
    if not confirm_token(token, 3600):
        jsondata = {"type": "login", "result": "Wrong", "result_msg": "The confirmation link is invalid or has expired"}
        return render_template('login/login.html', message=jsondata)
    if confirm_token(token, 3600):
        email = confirm_token(token)
        result_dict = _verifyEmail(email)
        if result_dict['result'] == 'OK':
            jsondata = {
                "type": "login", "result": "OK : With data", "result_msg": "Email verified",
                "login_email": email
            }
            return render_template('login/login.html', message=jsondata)
        else:
            jsondata = {
                "type": "login", "result": result_dict['result'], "result_msg": result_dict['result_msg']
            }
            # return redirect(url_for('.hello',message=jsondata))
            return render_template('login/login.html', message=jsondata)


def ideas_for_newsfeed_aux(user_email):
    user = _get_participant_node(user_email)
    list_ideas = []
    list_ideas_data = []
    followings = [x.end_node for x in list(getGraph().match(start_node=user, rel_type="FOLLOWS"))]
    if len(followings) is 0:
        return jsonify({"result": "OK", "data": []})
    for following in followings:
        ideas = [x.end_node for x in list(getGraph().match(start_node=following, rel_type="CREATED"))]
        if len(ideas) is 0:
            continue
        for idea in ideas:
            if _if_isnewideaforparticipant(idea, user):
                list_ideas.append(idea)
    for idea in list_ideas:
        newfeed = get_idea_data_aux(idea)
        list_ideas_data.append(newfeed)
    return jsonify({"result": "OK", "data": list_ideas_data})


def ideas_for_home_aux(participant_email, vote_type):
    participant = _get_participant_node(participant_email)
    dic = []
    list_ideas = []
    for vote in (list(getGraph().match(start_node=participant, rel_type="VOTED_ON"))):
        if vote["type"] == vote_type:
            dic.append(vote.end_node)
    for dic_idea in dic:
        current_idea = get_idea_data_aux(dic_idea)
        list_ideas.append(current_idea)
    return jsonify({"result": "OK", "data": list_ideas})


def do_cron_tasks_aux():
    # see the warningfailure_ideas to check whether we have to erase ideas.
    ideas_failurewarning = []
    ideas_failurewarning_removed = []
    rels = list(getGraph().match(rel_type="CREATED"))
    for rel in rels:
        if rel.end_node["failurewarning"] is True:
            ideas_failurewarning.append(rel.end_node)
    if len(ideas_failurewarning) > 0:
        for idea in ideas_failurewarning:
            if_failurewarning_timestamp = datetime.strptime(idea['if_failurewarning_timestamp'], '%d.%m.%Y')
            days = (datetime.now() - if_failurewarning_timestamp).days
            if (days > 7):
                ideas_failurewarning_removed.append(idea['proposal'])
                remove_idea_aux(idea['proposal'])
    return jsonify({"result":"OK", "ideas_removed" : ideas_failurewarning_removed})


####################
#  PURE INTERNAL
###################


# <Used by ideas_for_newsfeed_aux>
def _if_isnewideaforparticipant(idea, participant):
    votingRelationshipFound = getGraph().match_one(start_node=participant, rel_type="VOTED_ON", end_node=idea)
    if votingRelationshipFound is None: return True
    else: return False


# <Used by registration_receive_emailverification_aux() >
# input: email
# output: python dictionary
#  -> {'result': 'Wrong', 'result_msg': 'Email already verified'}
#  -> {'result': 'Wrong', 'result_msg': 'Email not registered'}
#  -> {'result': 'OK', 'result_msg': 'Email verified'}
def _verifyEmail(email):
    from participantManager import _removeFromUnverifiedParticipantsIndex, _addToParticipantsIndex
    unverifiedparticipant = _get_participant_node(email, False)
    if unverifiedparticipant is None:
        if _get_participant_node(email, True):
            return {'result': 'Wrong', 'result_msg': 'Email already verified'}
        else:
            return {'result': 'Wrong', 'result_msg': 'Email not registered'}
    else:
        _removeFromUnverifiedParticipantsIndex(email, unverifiedparticipant)
        _addToParticipantsIndex(email, unverifiedparticipant)
        unverifiedparticipant.remove_labels("unverified_participant")
        unverifiedparticipant.add_labels("participant")
        # TODO datestamp for registration
        # registered_on=datetime.datetime.now()
        return {'result': 'OK', 'result_msg': 'Email verified'}

