import bcrypt

import logging

_log = logging.getLogger(__name__)

class User(object):
    _type="User"
    username = None
    email = None
    password_hash = None
    token = None
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.hashpw(password, bcrypt.gensalt(14))
        self.token = "dummy"

    def check_password(self, password):
        if bcrypt.hashpw(password, self.password_hash) == self.password_hash:
            return True
        else:
            return False

    def reset_password(self, old_password, new_password):
        if self.check_password(old_password):
            self.password_hash = bcrypt.hashpw(new_password, bcrypt.gensalt(14))
            return True
        else:
            return False