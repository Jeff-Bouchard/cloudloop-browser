from rejson import Client, Path
from user import User
from serde import CloudLoopDecoder, CloudLoopEncoder
import bcrypt
import logging

class UserAlreadyExistsException(Exception):
    pass


class UserActionNotPermittedException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class UserNotInvitedSession(Exception):
    pass

_log = logging.getLogger(__name__)

class UserStore(object):
    """
    UserStore is a secondary Redis DB which stores user data.
    """
    def __init__(self, flush=False, redis_host='cloudloop-rejson'):
        self._data = {}
        self._rejson = Client(host=redis_host,
                              port=6379,
                              decode_responses=True,
                              db=2,
                              encoder=CloudLoopEncoder(),
                              decoder=CloudLoopDecoder())

        if flush:
            self._rejson.flushall()

    def __getitem__(self, username):
        return self.get_user(username)

    def create_user(self, username, password, email=''):
        if not self._rejson.exists(username):
            user = User(username=username, password=password, email=email)
            print(f"Storing user {user.username}")
            self._rejson.jsonset(username, Path.rootPath(), user)
            return True
        else:
            raise UserAlreadyExistsException(f'Username {username} already exists.')

    def check_for_session(self, username, session_name):
        exists = self._rejson.jsonarrindex(username, '.sessions', session_name)
        if exists >= 0:
            return True
        else:
            return False

    def join_session(self, username, session_name):
        """
        Idempotent add session to user object.
        """
        if not self.check_for_session(username, session_name):
            _log.info(f'Adding {username} to {session_name}')
            self._rejson.jsonarrappend(username, '.sessions', session_name)
            _log.info(f'User {username} added to session {session_name}.')
            return True
        else:
            msg=(f'User {username} already in session {session_name}.')
            _log.warning(msg)
            raise UserActionNotPermittedException(msg)

    def get_user_sessions(self, username):
        return self._rejson.jsonget(username, '.sessions')

    def get_user(self, username):
        if self._rejson.exists(username):
            user = self._rejson.jsonget(username)
            return user
        else:
            return False

    def get_user_password_hash(self, username):
        if self._rejson.exists(username):
            return self._rejson.jsonget(username, Path(".password_hash"))
        else:
            raise UserNotFoundException

    def delete_user(self, username):
        if self._rejson.exists(username):
            self._rejson.jsondel(username)
            return True
        else:
            raise UserNotFoundException(f"User {username} not found.")

    def update_user(self, username, user):
        if self._rejson.exists(username):
            self._rejson.jsonset(username, Path.rootPath(), user)
        else:
            return False

    def check_password(self, username, password):
        if self._rejson.exists(username):
            _log.info(f"Check password: {username} exists.")
            password_hash = self.get_user_password_hash(username).encode('utf-8')
            if bcrypt.hashpw(password.encode('utf-8'), password_hash) == password_hash:
                _log.info(f"Password match!")
                return True
            else:
                _log.warning(f"Incorrect password entered for {username}.")
                return False
        else:
            return False

    def get_all_usernames(self):
        return list(self._rejson.scan_iter())

    def get_friends(self, username):
        if self._rejson.exists(username):
            user = self.get_user(username)
            friends = user.friends
            return friends
        else:
            msg = f'No username {username} exists in UserStore.'
            _log.warning(msg)
            raise UserNotFoundException(msg)

    def add_friend_one_way(self, username, friend_username):
        """
        This (almost atomically) adds a user to friends list one way.
        """
        friend_exists = self._rejson.jsonarrindex(username, '.friends', friend_username)
        if friend_exists < 0:
            self._rejson.jsonarrappend(username, '.friends', friend_username)
            _log.info(f'{username} added {friend_username} as friend.')
            return True
        else:
            _log.warning(f'{friend_username} already in friends list for {username} at index {friend_exists}.')
            return False

    def add_friend_mutual(self, username, friend_username):
        """
        This adds users mutally to friends list. No approval mechanism for now.
        """
        if self._rejson.exists(username):
            if self._rejson.exists(friend_username):
                user_result = self.add_friend_one_way(username, friend_username)
                friend_result = self.add_friend_one_way(friend_username, username)
                if user_result and friend_result:
                    _log.info(f'Users added mutually to friends lists: {username}, {friend_username}')
                    return True
                else:
                    return False
            else:
                _log.error(f'No username exists for {friend_username} while adding as friend for {username}.')
                return False
        else:
            _log.error(f'No username {username} exists in userstore.')
            return False
