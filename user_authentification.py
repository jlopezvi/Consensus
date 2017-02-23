import flask_login
#import datetime

class User(flask_login.UserMixin):

    #def __init__(self, email, password, ifemailverified=None) :
    def __init__(self, email) :
        #TODO: distinguish unverified and verified participants
        from participantManager import _get_participant_node
        if _get_participant_node(email, 'all') is None:
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


