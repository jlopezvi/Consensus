from py2neo import neo4j
from participantManager import _getParticipantByEmail, getFollowerContacts
from utils import getGraph
from flask import jsonify, render_template

#Global variable support_rate_MIN = 90%
support_rate_MIN = 90

def ideas_for_newsfeed_aux(user_email):
    # load 1 concern
    # feed = concern
    new_idea_node=getNewIdeaForParticipant(user_email)
    if new_idea_node is None:
        return "redirect to Home"


    # feed = {
    # 'idea_id' : 12343,
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


    author_email = user_email
    author_photo_url = _getParticipantByEmail(user_email).get_properties()['image_url']
    author_username = _getParticipantByEmail(user_email).get_properties()['username']
    #TODO: add numerical index to ideas
    idea_id=0
    #duration = time today - _getParticipantByEmail(user_email).get_properties()['timestamp']
    supporters_num = len(list(getGraph().match(end_node=new_idea_node, rel_type="SUPPORTS")))
    volunteers_num = len(list(getGraph().match(end_node=new_idea_node, rel_type="VOLUNTEERS")))
    voters_num = len(list(getGraph().match(end_node=new_idea_node, rel_type="HAS_VOTED_ON")))
    if voters_num == 0 :
        support_rate = 100
    else:
        support_rate = (supporters_num / voters_num)*100
    supporters_rels = list(getGraph().match(end_node=new_idea_node, rel_type="SUPPORTS"))
    supporters = []
    for supporter_rel in supporters_rels:
        email = supporter_rel.start_node.get_properties()['email']
        username = supporter_rel.start_node.get_properties()['username']
        supporters.append({'email' : email, 'username':username })
    rejectors_rels = list(getGraph().match(end_node=new_idea_node, rel_type="REJECTS"))
    rejectors = []
    for rejector_rel in rejectors_rels:
        email = rejector_rel.start_node.get_properties()['email']
        username = rejector_rel.start_node.get_properties()['username']
        rejectors.append({'email' : email, 'username':username })

    feed=new_idea_node.get_properties()
    feed.update({'idea_id' : idea_id,
                 'author_photo_url': author_photo_url, 'author_username' : author_username,
                 'author_email' : author_email, 'supporters_num' : supporters_num,
                 'volunteers_num': volunteers_num,
                 'support_rate': support_rate, 'support_rate_MIN': support_rate_MIN,
                 'supporters' : supporters, 'rejectors' : rejectors})

    return jsonify(feed)
    # return render_template('login/newsfeed.html', persons=feed)


def getNewIdeaForParticipant(participant_email):
    participant=_getParticipantByEmail(participant_email)
    rels = list(getGraph().match(end_node=participant, rel_type="IS NEW FOR"))
    if len(rels) is 0:
        return None
    return rels[0].start_node