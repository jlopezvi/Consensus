from utils import getGraph, save_file #, send_email
from flask import jsonify, render_template
import json, uuid
from datetime import datetime,date
from participantManager import _get_participant_node
from ideaManager import _getIdeaByIdeaIndex, _get_supporters_emails_for_idea_aux, _get_volunteers_emails_for_idea_aux


def get_notifications_for_user_aux(email):
    participant = _get_participant_node(email)
    notifications = []
    current_notification = {}
    for NotificationRelationshipFound in (list(getGraph().match(end_node= participant ,rel_type="HAS_NOTIFICATION_FOR"))):
        current_notification.update({'notification_type' : NotificationRelationshipFound["type"],
                                     'proposal' : NotificationRelationshipFound.start_node['proposal']})
        notifications.append(current_notification)
    return jsonify({"result": "OK", "data": notifications})


# Used By <remove_notification_to_participant>
def remove_notification_from_idea_to_participant_aux(participant_email, proposal_index):
    idea = _getIdeaByIdeaIndex(proposal_index)
    participant = _get_participant_node(participant_email)
    notification_rel_found = getGraph().match_one(start_node=idea, rel_type="HAS_NOTIFICATION_FOR",
                                                  end_node=participant)
    if notification_rel_found is not None:
        getGraph().delete(notification_rel_found)
        return jsonify({"result": "OK", "result_msg": "Notification was deleted"})
    return jsonify({"result": "Wrong", "result_msg": "Notification does not exist"})


####################
#  PURE INTERNAL
###################

# <used by modify_idea_aux>
def _do_tasks_for_idea_editedproposal(idea_index):
    idea=_getIdeaByIdeaIndex(idea_index)
    idea['if_proposal_edited'] = True
    idea['if_proposal_edited_timestamp'] = ((datetime.now()).strftime("%d.%m.%Y"))
    _add_notification_relationships_from_idea_to_supporters(idea_index, 'edited')
    _send_notification_emails_from_idea_to_supporters(idea_index, 'edited')
    return


# <used by vote_on_idea_aux>
def _do_tasks_for_idea_failurewarning(idea_index):
    idea=_getIdeaByIdeaIndex(idea_index)
    idea['failurewarning'] = True
    idea['if_failurewarning_timestamp'] = ((datetime.now()).strftime("%d.%m.%Y"))
    _add_notification_relationship_from_idea_to_author(idea_index, 'failurewarning')
    _send_notification_email_from_idea_to_author(idea_index, 'failurewarning')
    return


# <used by vote_on_idea_aux>
def _do_tasks_for_idea_successful(idea_index):
    idea=_getIdeaByIdeaIndex(idea_index)
    idea['if_successful'] = True
    idea['if_successful_timestamp'] = ((datetime.now()).strftime("%d.%m.%Y"))
    _add_notification_relationships_from_idea_to_supporters(idea_index, 'successful')
    _add_notification_relationship_from_idea_to_author(idea_index, 'successful_to_author')
    _send_notification_emails_from_idea_to_supporters(idea_index, 'successful')
    _send_notification_email_from_idea_to_author(idea_index, 'successful_to_author')
    return


# <used by _do_tasks_for_idea_editedproposal, _do_tasks_for_idea_failurewarning, _do_tasks_for_idea_successful>
def _add_notification_relationships_from_idea_to_supporters(idea_index, notification_type):
    idea=_getIdeaByIdeaIndex(idea_index)
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    support_rels = [x for x in vote_rels if x["type"] == "supported"]
    supporters = [x.start_node for x in support_rels]
    for supporter in supporters:
        notification_rel_found = getGraph().match_one(start_node=idea, rel_type="HAS_NOTIFICATION_FOR",
                                                      end_node=supporter)
    if notification_rel_found is None:
        getGraph().create((idea, "HAS_NOTIFICATION_FOR", supporter, {"type": notification_type}))
    else:
        notification_rel_found["type"] = notification_type
    return


# <used by _do_tasks_for_idea_editedproposal, _do_tasks_for_idea_failurewarning, _do_tasks_for_idea_successful>
def _send_notification_emails_from_idea_to_supporters(idea_index, notification_type):
    idea=_getIdeaByIdeaIndex(idea_index)
    subject = "Consensus, New Notifications"
    if notification_type == 'edited':
        html = render_template('emails/idea_edited.html', msg_proposal=idea['proposal'])
    elif notification_type == 'successful':
        html = render_template('emails/idea_successful.html', msg_proposal=idea['proposal'])
    vote_rels = list(getGraph().match(end_node=idea, rel_type="VOTED_ON"))
    support_rels = [x for x in vote_rels if x["type"] == "supported"]
    supporters = [x.start_node for x in support_rels]
    for supporter in supporters:
        send_email(supporter['email'], subject, html)
    return


# <used by _do_tasks_for_idea_editedproposal, _do_tasks_for_idea_failurewarning, _do_tasks_for_idea_successful>
def _add_notification_relationship_from_idea_to_author(idea_index, notification_type):
    idea=_getIdeaByIdeaIndex(idea_index)
    author = getGraph().match_one(rel_type="CREATED", end_node=idea).start_node
    notification_rel_found = getGraph().match_one(start_node=idea, rel_type="HAS_NOTIFICATION_FOR", end_node=author)
    if notification_rel_found is None:
        getGraph().create((idea, "HAS_NOTIFICATION_FOR", author, {"type":notification_type}))
    else:
        notification_rel_found["type"] = notification_type
    return


# <used by _do_tasks_for_idea_editedproposal, _do_tasks_for_idea_failurewarning, _do_tasks_for_idea_successful>
def _send_notification_email_from_idea_to_author(idea_index, notification_type):
    idea=_getIdeaByIdeaIndex(idea_index)
    author = getGraph().match_one(rel_type="CREATED", end_node=idea).start_node
    subject = "Consensus, New Notifications"
    if notification_type == 'failurewarning':
        html = render_template('emails/idea_failurewarning.html', msg_proposal=idea['proposal'])
    elif notification_type == 'successful_to_author':
        volunteers = _get_volunteers_emails_for_idea_aux(idea_index)
        if len(volunteers) > 0 :
            html = render_template('emails/idea_successful.html', msg_proposal=idea['proposal'], volunteers=volunteers)
        else :
            supporters = _get_supporters_emails_for_idea_aux(idea_index)
            html = render_template('emails/idea_successful.html', msg_proposal=idea['proposal'], supporters=supporters)
    send_email(author['email'], subject, html)
    return
