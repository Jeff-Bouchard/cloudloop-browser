import bcrypt
from json import JSONEncoder, JSONDecoder
import logging
import datetime
import jwt

PYJWT_SECRET_KEY=b'|\xc7\xf6E9&\xf9vf`N(\xe3x.\xd4R\xc1|<_\xddJ\xa7'

_log = logging.getLogger(__name__)

class User(object):
    _type = "User"
    username = None
    email = None
    password_hash = None

    def __init__(self, username, email='', password=''):
        self._type = "User"
        self.username = username
        self.email = email
        if password != '':
            _log.info(f'New password for user object being hashed. {username}')
            encoded_password = password.encode('utf-8')
            self.password_hash = bcrypt.hashpw(encoded_password, bcrypt.gensalt(14))
        else:
            self.password_hash = b'SCRUBBED'


    def reset_password(self, old_password, new_password):
        if self.check_password(old_password):
            self.password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(14))
            return True
        else:
            return False


    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                PYJWT_SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, PYJWT_SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'