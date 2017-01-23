from py2neo import neo4j
from participantManager import _getParticipantByEmail, getFollowerContacts
from ideaManager import get_idea_structure
from utils import getGraph
from flask import jsonify, render_template

#Global variable support_rate_MIN = 90%
support_rate_MIN = 90


def ideas_for_newsfeed_aux(participant_email):
    participant = _getParticipantByEmail(participant_email)
    dic = []
    feed = []
    followings_rels = list(getGraph().match(start_node=participant, rel_type="FOLLOWS"))
    if len(followings_rels) is 0:
        return None
    for following_rel in followings_rels:
        following = following_rel.end_node
        ideas_rels = list(getGraph().match(start_node=following, rel_type="CREATED"))
        if len(ideas_rels) is 0:
            continue
        for idea_rel in ideas_rels:
            idea = idea_rel.end_node
            if ifIsNewIdeaForParticipant(idea, participant):
                dic.append(idea)
    for dic_idea in dic:
        newfeed = get_idea_structure(dic_idea)
        feed.append(newfeed)
    return jsonify(result=feed)

# Used by ideas_for_newsfeed_aux
def ifIsNewIdeaForParticipant(idea, participant):
    votingRelationshipFound = getGraph().match_one(start_node=participant, rel_type="VOTED_ON", end_node=idea)
    if votingRelationshipFound is None:
        return True


def ideas_for_home_aux(participant_email, vote_type):
    participant = _getParticipantByEmail(participant_email)
    dic = []
    feed = []
    for vote in (list(getGraph().match(start_node=participant, rel_type="VOTED_ON"))):
        if vote["type"] == vote_type:
            dic.append(vote.end_node)
    for dic_idea in dic:
        current_idea = get_idea_structure(dic_idea)
        feed.append(current_idea)
    return jsonify(result=feed)




#
# def ideas_for_newsfeed_aux(user_email):
#     # load 1 concern
#     # feed = concern
#     new_idea_node=getNewIdeaForParticipant(user_email)
#     if new_idea_node is None:
#         return "redirect to Home"
#
#
#     # feed = {
#     # 'idea_id' : 12343,
#     # 'author_photo_url' : 'assets/profile/perfil-mediano.png', 'author_username' : 'Daniela', 'author_email' : 'a@',
#     # 'duration' : '2 days',
#     # 'supporters_goal_num' : 200, 'supporters_num' : 5, 'volunteers_goal_num' : 5, 'volunteers_num' : 2,
#     # 'image_url' : 'url-to-picture',
#     # 'concern': 'Some text for the concern',
#     # 'proposal': 'Some text for the proposal',
#     # 'support_rate' : 95,
#     # 'support_rate_MIN' : 90,
#     # 'supporters': [
#     # { 'email': 'b@', 'username': 'Maria' }, { 'email': 'c@', 'username': 'Pedro' }
#     #             ],
#     # 'rejectors':[
#     # { 'email': 'd@', 'username': 'Elisa' }
#     #               ]
#     # }
#
#
#     author_email = getGraph().match_one(end_node=new_idea_node, rel_type="CREATED").start_node.get_properties()['email']
#     author_photo_url = _getParticipantByEmail(author_email).get_properties()['image_url']
#     author_username = _getParticipantByEmail(author_email).get_properties()['username']
#     #TODO: add numerical index to ideas
#     idea_id=0
#     duration = "2 days"
#     #duration = time today - _getParticipantByEmail(user_email).get_properties()['timestamp']
#     voters_num = len(list(getGraph().match(end_node=new_idea_node, rel_type="VOTED_ON")))
#     supporters_num = _get_vote_statistics_for_idea(new_idea_node)[0]
#     #rejectors_num = _get_vote_statistics_for_idea(new_idea_node)[1]
#     volunteers_num = _get_vote_statistics_for_idea(new_idea_node)[2]
#     if voters_num == 0 :
#         support_rate = 100
#     else:
#         support_rate = (supporters_num / voters_num)*100
#     supporters = []
#     rejectors = []
#     for vote_rel in (list(getGraph().match(end_node=new_idea_node, rel_type="VOTED_ON"))):
#         email = vote_rel.start_node.get_properties()['email']
#         username = vote_rel.start_node.get_properties()['username']
#         if vote_rel["type"] == "supporter":
#             supporters.append({'email': email, 'username': username})
#         else:
#             rejectors.append({'email': email, 'username': username})
#     feed=new_idea_node.get_properties()
#     feed.update({'idea_id' : idea_id,
#                  'author_photo_url': author_photo_url, 'author_username' : author_username,
#                  'duration': duration,
#                  'author_email' : author_email, 'supporters_num' : supporters_num,
#                  'volunteers_num': volunteers_num,
#                  'support_rate': support_rate, 'support_rate_MIN': support_rate_MIN,
#                  'supporters' : supporters, 'rejectors' : rejectors})
#
#     return jsonify(feed)
#     # return render_template('login/newsfeed2.html', persons=feed)
#
# #used by ideas_for_newsfeed_aux
# def _get_vote_statistics_for_idea(node_idea):
#    rejectors_num=0
#    supporters_num=0
#    volunteers_num=0
#    for vote_rel in (list(getGraph().match(end_node=node_idea, rel_type="VOTED_ON"))):
#        if vote_rel["type"] == "supporter":
#            supporters_num+=1
#        else:
#            rejectors_num+=1
#        if vote_rel["volunteered"] == "yes":
#            volunteers_num+=1
#    return (supporters_num,rejectors_num,volunteers_num)
#
# # def getNewIdeaForParticipant(participant_email):
# #     participant=_getParticipantByEmail(participant_email)
# #     rels = list(getGraph().match(end_node=participant, rel_type="IS NEW FOR"))
# #     if len(rels) is 0:
# #         return None
# #     return rels[0].start_node
#
# def getNewIdeaForParticipant(participant_email):
#      participant=_getParticipantByEmail(participant_email)
#      followings_rels = list(getGraph().match(start_node=participant, rel_type="FOLLOWS"))
#      if len(followings_rels) is 0:
#          return None
#      for following_rel in followings_rels :
#          #TODO: ADD "HAS_VOTED_ON"
#          following=following_rel.end_node
#          ideas_rels=list(getGraph().match(start_node=following, rel_type="CREATED"))
#          if len(ideas_rels) is 0:
#              continue
#          for idea_rel in ideas_rels :
#              idea=idea_rel.end_node
#              idea_id=idea['proposal']
#              if ifIsNewIdeaForParticipant(idea_id,participant_email):
#                  return idea
#
# def ifIsNewIdeaForParticipant(idea_id,participant_email):
#     return True