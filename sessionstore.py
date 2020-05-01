import datetime
import logging
from collections import namedtuple

Loop = namedtuple('Loop',['link', 'creator', 'hash', 'created_at'], defaults=["","","",datetime.datetime.now().isoformat()])

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
    The backing persistent datastore will be redis or timescaleDB (postgres)
    We will just save a snapshot of each session, keyed by session name.
    """
    def __init__(self):
        self._data = {}
        self._next_slot = 1 # eventually implement a pointer here for atomic seeks

    def __getitem__(self, item):
        return self.get_session(item)

    def get_session_names(self):
        return list(self._data.keys())

    def get_session(self, session_name):
        if session_name in self._data:
            return self._data[session_name]
        else:
            raise SessionNotFoundException(f'Session {session_name} not found.')

    def get_loop_from_library(self, session_name, loop_id):
        try:
            library = self.get_loops_in_library(session_name)
            loop = next(filter(lambda x: x.link == loop_id, library), None)
            return loop
        except SessionNotFoundException as e:
            raise e

    def get_loops_in_library(self, session_name):
        if session_name in self._data:
            session = self._data[session_name]
            library = session['library']
            return library
        else:
            raise SessionNotFoundException(f'Session {session_name} not found.')

    def next_slot(self, session_name):
        """Get next available slot key, iterating up from 1. Very very dumb and slow."""
        slots = self[session_name]['slots']
        slot_keys = slots.keys()
        slot_no = 1 # slot 0 is metronome
        while slot_no in slot_keys:
            slot_no+=1 # VERY STUPID, THIS WILL BOTTLENECK HEAVILY
        return slot_no

    def lock_redis(self):
        # mutex, maybe implement this as contextmanager
        pass

    def sync(self):
        # Lock redis, pull session data, update self._data, unlock redis.
        pass

    def create_session(self, session_name, creator, private=False):
        if session_name in self._data:
            raise SessionAlreadyExistsException(f'Session {session_name} already exists. Aborting create_session.')
        else:
            self._data[session_name] = {
                "name": session_name,
                "created_at": datetime.datetime.now().isoformat(),
                "private": private,
                "creator": creator,
                "generation": 0,
                "users": [creator],
                "users_online": [],
                "slots":{},
                "library":[]
            }
            return self._data[session_name]

    def join_session(self, session_name, username, inviter=None):
        if session_name in self._data:
            session = self._data[session_name]
            if username in session['users']:
                _log.info(f'User {username} already exists in session.')
                return True
            else:
                if session['private'] == True:
                    if inviter in session['users']:
                        session['users'].append(username)
                        _log.info(f'User {username} added to private session {session_name} by user {inviter}.')
                        return True
                    else:
                        msg = f'Inviter {inviter} not in private session {session_name}, cannot add user {username} to session.'
                        raise SessionActionNotPermittedException(msg)

                else:
                    session['users'].append(username)
                    _log.info(f'User {username} added to session {session_name}.')
                    return True
        else:
            raise SessionNotFoundException(f'Session {session_name} not found.')

    def add_loop(self, session_name, username, loop):
        if session_name in self._data:
            session = self._data[session_name]
            if username in session['users']:
                if loop in session['library']:
                    _log.info(f'Loop {loop.link} already exists in {session_name} library.')
                    return True
                else:
                    _log.info(f'Loop {loop.link } added to session {session_name} by {username}.')
                    session['library'].append(loop)
                    return True
            else:
                msg = f'Operation not permitted. User {username} not in session {session_name}.'
                raise SessionActionNotPermittedException(msg)

        else:
            raise SessionNotFoundException(f'Session {session_name} not found.')

    def add_slot(self, session_name, username):
        if session_name in self._data:
            session = self._data[session_name]
            if username in session['users']:
                slots = session['slots']
                next_slot = self.next_slot(session_name)
                slots[next_slot] = Loop(link='', creator=username, hash='')
                return True
            else:
                raise SessionActionNotPermittedException(f'User {username} is not permitted to add slot in session {session_name}.')
        else:
            raise SessionNotFoundException(f'Session {session_name} not found.')

    def delete_slot(self, session_name, username, slot_number):
        if session_name in self._data:
            session = self._data[session_name]
            if username in session['users']:
                if slot_number in session['slots'].keys():
                    if session['slots'][slot_number].creator == username:
                        del session['slots'][slot_number]
                        _log.info(f'User {username} deleted slot {slot_number} from {session_name}')
                        return True
                    else:
                        msg = f'Loop in slot {slot_number} does not belong to user {username} in session {session_name}.'
                        raise SessionActionNotPermittedException(msg)
                else:
                    msg = f'Slot {slot_number} does not exist in session {session_name}.'
                    raise SessionActionNotPermittedException(msg)
            else:
                msg = f'User {username} not in session {session_name}.'
                raise SessionActionNotPermittedException(msg)
        else:
            raise SessionNotFoundException(f'Session {session_name} not found.')

    def update_slot(self, session_name, username, slot_number, loop):
        if session_name in self._data:
            session = self._data[session_name]
            if username in session['users']:
                if loop not in session['library'] and loop.link != '':
                    session['library'].append(loop)
                    _log.info(f'Added {loop.hash} to library for session {session_name}')
                if slot_number in session['slots'].keys():
                    if session['slots'][slot_number].creator == username:
                        session['slots'][slot_number] = loop
                        _log.info(f'User {username} updated slot {slot_number} in {session_name} with loop {loop.hash}')
                        return True
                    else:
                        msg = f'Loop in slot {slot_number} does not belong to user {username} in session {session_name}.'
                        raise SessionActionNotPermittedException(msg)
                else:
                    msg = f'Slot {slot_number} does not exist in session {session_name}.'
                    raise SessionActionNotPermittedException(msg)
            else:
                msg = f'User {username} not in session {session_name}.'
                raise SessionActionNotPermittedException(msg)
        else:
            raise SessionNotFoundException(f'Session {session_name} not found.')








