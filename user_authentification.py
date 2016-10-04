import flask_login
from participantManager import _getParticipantByEmail


class User(flask_login.UserMixin):

    def __init__(self, email) :
        if _getParticipantByEmail(email) :
            self.id = email
        if _getParticipantByEmail(email) is None :
            self = None

    #def get_by(self, email):
    #    try:
    #        __getParticipantByEmail(email)
    #        self.id = email
    #        return self
    #    except NotFoundError:
    #        return


