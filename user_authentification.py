import flask_login
#import datetime
from participantManager import _getParticipantByEmail


class User(flask_login.UserMixin):

    #def __init__(self, email, password, ifemailverified=None) :
    def __init__(self, email) :
        if _getParticipantByEmail(email) is None:
            self = None
        else:
            self.id = email
            #self.email = email
            ##the password should be encrypted MD5password already at the frontend
            #self.password = password
            #self.registered_on = datetime.datetime.now()
            #self.ifemailverified = ifemailverified



    #def get_by(self, email):
    #    try:
    #        __getParticipantByEmail(email)
    #        self.id = email
    #        return self
    #    except NotFoundError:
    #        return


