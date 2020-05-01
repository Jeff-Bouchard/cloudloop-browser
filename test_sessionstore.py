import pytest

from datetime import timedelta, datetime

from sessionstore import SessionStore, Loop, SessionNotFoundException, SessionActionNotPermittedException, SessionAlreadyExistsException, UserNotInvitedSession


def test_sessionstore_init():
    store = SessionStore()
    assert store._data == dict()
    assert list(store._data.keys()) == []


def test_sessionstore_get_session_names_empty():
    store = SessionStore()
    names = store.get_session_names()
    assert names == []


def test_sessionstore_supports_indexing_empty():
    store = SessionStore()
    with pytest.raises(SessionNotFoundException):
        store['sessionName']


def test_create_session():
    store = SessionStore()
    session = store.create_session(session_name='test_session', creator='test_user')
    assert session is not None
    assert session['name'] == 'test_session'
    assert session['creator'] == 'test_user'
    assert set(session.keys()) == {'name',
                                   'created_at',
                                   'private',
                                   'creator',
                                   'generation',
                                   'users',
                                   'users_online',
                                   'slots',
                                   'library'}


def test_new_session_is_not_private():
    store = SessionStore()
    session = store.create_session(session_name='test_session', creator='test_user')
    assert session['private'] ==  False


def test_session_types():
    store = SessionStore()
    session = store.create_session(session_name='test_session', creator='test_user')
    assert type(session['name']) is str
    assert type(session['created_at']) is str
    assert type(session['private']) is bool
    assert type(session['creator']) is str
    assert type(session['generation']) is int
    assert type(session['users']) is list
    assert type(session['users_online']) is list
    assert type(session['slots']) is dict
    assert type(session['library']) is list


def test_get_session():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    session = store.get_session('test_session')
    assert session['name'] == 'test_session'


def test_index_into_session():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    session = store['test_session']
    assert session['name'] == 'test_session'

def test_join_public_session():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.join_session(session_name='test_session', username='test_user_2')
    assert len(store['test_session']['users']) == 2
    assert set(store['test_session']['users']) == {'test_user', 'test_user_2'}

def test_fail_join_private_session_no_inviter():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user', private=True)
    with pytest.raises(SessionActionNotPermittedException):
        store.join_session(session_name='test_session', username='test_user_2')

def test_fail_join_private_session_self_inviter():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user', private=True)
    with pytest.raises(SessionActionNotPermittedException):
        store.join_session(session_name='test_session', username='test_user_2', inviter='test_user_2')

def test_fail_join_private_session_wrong_inviter():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user', private=True)
    with pytest.raises(SessionActionNotPermittedException):
        store.join_session(session_name='test_session', username='test_user_2', inviter='test_user_3')

def test_join_private_session_invited():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user', private=True)
    assert store.join_session(session_name='test_session', username='test_user_2', inviter='test_user') is True

def test_get_session_names_none():
    store = SessionStore()
    names = store.get_session_names()
    assert type(names) == list
    assert len(names) == 0

def test_get_session_names_single():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user', private=True)
    names = store.get_session_names()
    assert type(names) == list
    assert names[0] == 'test_session'


def test_add_slot_fail_invalid_session():
    store = SessionStore()
    with pytest.raises(SessionNotFoundException):
        store.add_slot(session_name='session_does_not_exist', username='test_user')


def test_add_slot_fail_user_not_in_session():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    with pytest.raises(SessionActionNotPermittedException):
        store.add_slot(session_name='test_session', username='test_user_2')


def test_add_slot_success():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.add_slot(session_name='test_session', username='test_user')
    assert len(store['test_session']['slots']) == 1
    assert type(store['test_session']['slots'][1]) is Loop

def test_delete_slot_fail_ownership():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.join_session(session_name='test_session', username='test_user_2', inviter='test_user')
    store.add_slot(session_name='test_session', username='test_user')
    with pytest.raises(SessionActionNotPermittedException):
        store.delete_slot(session_name='test_session', username='test_user_2', slot_number=1)

def test_delete_slot_fail_slot_number():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.add_slot(session_name='test_session', username='test_user')
    with pytest.raises(SessionActionNotPermittedException):
        store.delete_slot(session_name='test_session', username='test_user', slot_number=2)

def test_delete_slot_failure_session_not_exist():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.add_slot(session_name='test_session', username='test_user')
    with pytest.raises(SessionNotFoundException):
        store.delete_slot(session_name='test_session_2', username='test_user', slot_number=1)


def test_delete_slot_failure_user_not_in_session():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.add_slot(session_name='test_session', username='test_user')
    with pytest.raises(SessionActionNotPermittedException):
        store.delete_slot(session_name='test_session', username='test_user_2', slot_number=1)


def test_create_loop():
    loop = Loop(link='http://test.link', creator='test_user', hash='test_hash')
    assert type(loop) == Loop
    assert loop.link == 'http://test.link'
    assert loop.creator == 'test_user'
    assert loop.hash == 'test_hash'