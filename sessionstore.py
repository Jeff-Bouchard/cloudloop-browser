import datetime
import logging
from rejson import Client, Path
from loop import Loop
from serde import CloudLoopEncoder, CloudLoopDecoder
import json


class SessionAlreadyExistsException(Exception):
    pass


class SessionActionNotPermittedException(Exception):
    pass


class SessionNotFoundException(Exception):
    pass


class UserNotInvitedSession(Exception):
    pass


_log = logging.getLogger(__name__)


class SessionStore(object):
    """
    SessionStore is the in-memory source of truth for all of the sessions on a cloudloop host.
    This store will be backed by Redis, and we will broadcast a snapshot of state to our users
    based on the contents in this store.
    Since python/flask is single-threaded, if we make all changes here atomic, we can guarantee
    session integrity across all sessions.
    The backing persistent datastore is redis rejson
    We will just save a snapshot of each session, keyed by session name.
    """

    def __init__(self, flush=True, redis_host='cloudloop-rejson'):
        self._data = {}
        self._next_slot = 0  # eventually a FIFO queue (list.append(in) + list.pop(0)
        self._rejson = Client(host=redis_host,
                              port=6379,
                              decode_responses=True,
                              # password='cloudloop',
                              encoder=CloudLoopEncoder(),
                              decoder=CloudLoopDecoder(),
                              db=1)

        if flush:
            self._rejson.flushall()

    def __getitem__(self, session_name):
        return self.get_session_data(session_name)

    def get_session_names(self):
        return list(self._rejson.scan_iter())

    def get_public_session_headers(self):
        public_session_headers = []
        sessions = self.get_session_names()
        if len(sessions) > 0:
            session_privacy = self.get_sessions_data(sessions, '.private')
            public_sessions_names = list(
                map(lambda y: y[0], filter(lambda x: x[1] == False, zip(sessions, session_privacy))))
            public_sessions_creators = self.get_sessions_data(public_sessions_names, '.creator')
            public_sessions_users_online = self.get_sessions_data(public_sessions_names, '.users_online')
            for x in range(len(public_sessions_names)):
                entry = {}
                entry['name'] = public_sessions_names[x]
                entry['creator'] = public_sessions_creators[x]
                entry['users_online'] = len(public_sessions_users_online[x])
                public_session_headers.append(entry)
        return public_session_headers

    def get_session_users_online(self, session_names):
        return self._rejson.jsonmget('.users_online', *session_names)

    def get_sessions_data(self, session_names, path=Path.rootPath()):
        sessions = self._rejson.jsonmget(path, *session_names)
        return sessions

    def get_session_data(self, session_name, path=Path.rootPath()):
        if self._rejson.exists(session_name):
            session_data = self._rejson.jsonget(session_name, path)
            if isinstance(session_data, dict):
                if 'slots' in session_data:
                    session_data['slots'] = {int(key): loop for key, loop in session_data['slots'].items()}
                    return session_data
                else:
                    return session_data
            else:
                return session_data
        else:
            raise SessionNotFoundException(f'Session {session_name} not found.')

    def get_slots_with_int_keys(self, session_name):
        slots = self.get_session_data(session_name, '.slots')
        slots = {int(key): loop for key, loop in slots.items()}
        return slots

    def get_library(self, session_name):
        library = self.get_session_data(session_name, '.library')
        return library

    def check_user_auth(self, session_name, username):
        return username in self.get_session_data(session_name, path='.users')

    def get_loop_from_library(self, session_name, loop_id):
        try:
            library = self.get_library(session_name)
            loop = next(filter(lambda x: x.link == loop_id, library), None)
            return loop
        except SessionNotFoundException as e:
            raise e

    def next_slot(self, session_name):
        """Get next available slot key, iterating up from 1. Very very dumb and slow."""
        slots = self.get_session_data(session_name, '.slots')
        slot_keys = map(int, slots.keys())
        slot_no = 0
        while slot_no in slot_keys:
            slot_no += 1  # VERY STUPID, THIS WILL BOTTLENECK HEAVILY
        return slot_no

    def lock_redis(self):
        # mutex, maybe implement this as contextmanager
        pass

    def sync(self):
        # Lock redis, pull session data, update self._data, unlock redis.
        pass

    def create_session(self, session_name, creator, private=False):
        """
        MUTATES DATASTORE
        """
        if session_name in self.get_session_names():
            raise SessionAlreadyExistsException(f'Session {session_name} already exists. Aborting create_session.')
        else:
            session_data = {
                "name": session_name,
                "created_at": datetime.datetime.now().isoformat(),
                "private": private,
                "creator": creator,
                "generation": 0,
                "users": [creator],
                "users_online": {},
                "slots": {},
                "library": []  # Eventually use a set here.
            }
            self._rejson.jsonset(session_name, Path.rootPath(), session_data)
            return session_data

    def join_session(self, session_name, username, inviter=None):
        """
        MUTATES DATASTORE
        """
        users = self.get_session_data(session_name, '.users')
        if username in users:
            _log.info(f'User {username} already exists in session.')
            return True
        elif inviter in users:
            self._rejson.jsonarrappend(session_name, '.users', username)
            _log.info(f'User {username} added to session {session_name} by user {inviter}.')
            return True
        elif not self.get_session_data(session_name, 'private'):
            self._rejson.jsonarrappend(session_name, '.users', username)
            _log.info(f'User {username} added self to public session {session_name}.')
            return True
        else:
            msg = f'Inviter {inviter} not in private session {session_name}, cannot add user {username} to session.'
            _log.warning(msg)
            raise SessionActionNotPermittedException(msg)

    def delete_session(self, session_name, username):
        session = self[session_name]
        if session:
            if session['creator'] == username:
                self._rejson.delete(session_name)
                _log.info(f'User {username} deleted session {session_name}.')
                return True
            else:
                msg = f'User {username} is not creator of session {session_name}. Cannot Delete.'
                raise SessionActionNotPermittedException(msg)
        else:
            msg = f'Session {session_name} not found.'
            raise SessionNotFoundException(msg)

    def add_loop(self, session_name, username, loop):
        """
        MUTATES DATASTORE
        """
        if loop.link == '':
            return True
        if self.check_user_auth(session_name, username):
            loop_library = self.get_library(session_name)
            if loop in loop_library:
                _log.info(f'Loop {loop.link} already exists in {session_name} library.')
                return True
            else:
                _log.info(f'Loop {loop.link} added to session {session_name} by {username}.')
                self._rejson.jsonarrappend(session_name, '.library', loop)
                next_slot = self.add_slot(session_name=session_name, username=username)
                self.update_slot(session_name=session_name, username=username, loop=loop, slot_number=next_slot)
                return True
        else:
            msg = f'Operation not permitted. User {username} not in session {session_name}.'
            _log.warning(msg)
            raise SessionActionNotPermittedException(msg)

    def add_slot(self, session_name, username):
        """
        MUTATES DATASTORE
        """
        if self.check_user_auth(session_name, username):
            next_slot = self.next_slot(session_name)
            new_loop = Loop(link='', creator=username, hash='')
            self._rejson.jsonset(session_name, f'.slots.{next_slot}', new_loop)
            return next_slot
        else:
            raise SessionActionNotPermittedException(
                f'User {username} is not permitted to add slot in session {session_name}.')

    def delete_slot(self, session_name, username, slot_number):
        """
        MUTATES DATASTORE
        """
        if self.check_user_auth(session_name, username):
            slots = self.get_slots_with_int_keys(session_name)
            if slot_number in slots:
                if slots[slot_number].creator == username:
                    self._rejson.jsondel(session_name, f'.slots.{slot_number}')
                    _log.info(f'User {username} deleted slot {slot_number} from {session_name}')
                    return True
                else:
                    msg = f'Loop in slot {slot_number} does not belong to user {username} in session {session_name}.'
                    _log.warning(msg)
                    raise SessionActionNotPermittedException(msg)
            else:
                msg = f'Slot {slot_number} does not exist in session {session_name}.'
                _log.warning(msg)
                raise SessionActionNotPermittedException(msg)
        else:
            msg = f'User {username} not in session {session_name}.'
            _log.warning(msg)
            raise SessionActionNotPermittedException(msg)

    def update_slot(self, session_name, username, slot_number, loop):
        """
        MUTATES DATASTORE
        """
        self.add_loop(session_name, username, loop)
        slots = self.get_slots_with_int_keys(session_name)
        if slot_number in slots:
            if slots[slot_number].creator == username:
                self._rejson.jsonset(session_name, f'.slots.{slot_number}', loop)
                print(f'User {username} updated slot {slot_number} in {session_name} with loop {loop.hash}')
                return True
            else:
                msg = f'Loop in slot {slot_number} does not belong to user {username} in session {session_name}.'
                raise SessionActionNotPermittedException(msg)
        else:
            msg = f'Slot {slot_number} does not exist in session {session_name}.'
            raise SessionActionNotPermittedException(msg)

    def user_connect(self, session_name, username):
        """MUTATES DATASTORE"""
        if self.check_user_auth(session_name=session_name, username=username):
            self._rejson.jsonset(session_name, '.users_online', {username: datetime.datetime.now().isoformat()})

    def user_disconnect(self, session_name, username):
        """MUTATES DATASTORE"""
        if self.check_user_auth(session_name=session_name, username=username):
            if self._rejson.jsonget(session_name, f'.users_online.{username}') is not None:
                print(f'{username} has gone offline in {session_name}')
                self._rejson.jsondel(session_name, f'.users_online.{username}')
