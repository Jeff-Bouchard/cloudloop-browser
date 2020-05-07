import pytest

from datetime import timedelta, datetime

from sessionstore import SessionStore, Loop, SessionNotFoundException, SessionActionNotPermittedException, \
    SessionAlreadyExistsException, UserNotInvitedSession

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
    assert session['private'] == False


def test_session_types():
    store = SessionStore()
    session = store.create_session(session_name='test_session', creator='test_user')
    assert type(session['name']) is str
    assert type(session['created_at']) is str
    assert type(session['private']) is bool
    assert type(session['creator']) is str
    assert type(session['generation']) is int
    assert type(session['users']) is list
    assert type(session['users_online']) is dict
    assert type(session['slots']) is dict
    assert type(session['library']) is list


def test_get_session_data():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    session = store.get_session_data('test_session')
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
    assert len(store.get_slots_with_int_keys('test_session')) == 1
    assert isinstance(store.get_slots_with_int_keys('test_session')[1], Loop)


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


def test_delete_slot_user_not_owner():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.add_slot(session_name='test_session', username='test_user')
    store.join_session(session_name='test_session', username='test_user_2', inviter='test_user')
    with pytest.raises(SessionActionNotPermittedException):
        store.delete_slot(session_name='test_session', username='test_user_2', slot_number=1)


def test_delete_slot_success():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.add_slot(session_name='test_session', username='test_user')
    assert store.delete_slot(session_name='test_session', username='test_user', slot_number=1)


def test_add_and_delete_many_slot():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    list(map(lambda y: store.add_slot(session_name='test_session', username='test_user'), range(100)))
    results = list(map(lambda x: store.delete_slot(session_name='test_session', username='test_user', slot_number=x),
                       range(1, 101)))
    assert results == [True for x in range(100)]
    assert len(store['test_session']['slots']) == 0


def test_add_loop_failure_bad_session():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    loop = Loop(link='http://test.link', creator='test_user', hash='test_hash', created_at='test_timestamp')
    with pytest.raises(SessionNotFoundException):
        store.add_loop(session_name='test_session_2', username='test_user', loop=loop)


def test_add_loop_failure_user_not_in_session():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    loop = Loop(link='http://test.link', creator='test_user_2', hash='test_hash', created_at='test_timestamp')
    with pytest.raises(SessionActionNotPermittedException):
        store.add_loop(session_name='test_session', username='test_user_2', loop=loop)


def test_add_loop_success_created():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.join_session(session_name='test_session', username='test_user_2', inviter='test_user')
    loop = Loop(link='http://test.link', creator='test_user_2', hash='test_hash', created_at='test_timestamp')
    store.add_loop(session_name='test_session', username='test_user_2', loop=loop)
    assert len(store['test_session']['library']) == 1
    assert len(store['test_session']['slots']) == 0
    assert store.get_library('test_session')[0] == loop


def test_add_loop_success_idempotent():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.join_session(session_name='test_session', username='test_user_2', inviter='test_user')
    loop = Loop(link='http://test.link', creator='test_user_2', hash='test_hash', created_at='test_timestamp')
    store.add_loop(session_name='test_session', username='test_user_2', loop=loop)
    store.add_loop(session_name='test_session', username='test_user_2', loop=loop)
    assert len(store['test_session']['library']) == 1
    assert len(store['test_session']['slots']) == 0
    assert store.get_library('test_session')[0] == loop


def test_update_slot_failure_bad_session():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.join_session(session_name='test_session', username='test_user_2', inviter='test_user')
    loop = Loop(link='http://test.link', creator='test_user_2', hash='test_hash', created_at='test_timestamp')
    store.add_loop(session_name='test_session', username='test_user_2', loop=loop)
    with pytest.raises(SessionNotFoundException):
        store.update_slot(session_name='test_session_2', username='test_user', slot_number=1, loop=loop)


def test_update_slot_failure_user_not_in_session():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.join_session(session_name='test_session', username='test_user_2', inviter='test_user')
    loop = Loop(link='http://test.link', creator='test_user_2', hash='test_hash', created_at='test_timestamp')
    store.add_loop(session_name='test_session', username='test_user_2', loop=loop)
    with pytest.raises(SessionActionNotPermittedException):
        store.update_slot(session_name='test_session', username='test_user_3', slot_number=1, loop=loop)


def test_update_slot_failure_slot_not_exist():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.join_session(session_name='test_session', username='test_user_2', inviter='test_user')
    loop = Loop(link='http://test.link', creator='test_user_2', hash='test_hash', created_at='test_timestamp')
    store.add_loop(session_name='test_session', username='test_user_2', loop=loop)
    with pytest.raises(SessionActionNotPermittedException):
        store.update_slot(session_name='test_session', username='test_user_2', slot_number=1, loop=loop)

def test_update_slot_failure_slot_not_exist_with_slots():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.join_session(session_name='test_session', username='test_user_2', inviter='test_user')
    store.add_slot(session_name='test_session', username='test_user')
    loop = Loop(link='http://test.link', creator='test_user_2', hash='test_hash', created_at='test_timestamp')
    store.add_loop(session_name='test_session', username='test_user_2', loop=loop)
    with pytest.raises(SessionActionNotPermittedException):
        store.update_slot(session_name='test_session', username='test_user', slot_number=2, loop=loop)

def test_update_slot_failure_user_not_slot_owner():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.join_session(session_name='test_session', username='test_user_2', inviter='test_user')
    store.add_slot(session_name='test_session', username='test_user')
    loop = Loop(link='http://test.link', creator='test_user_2', hash='test_hash', created_at='test_timestamp')
    store.add_loop(session_name='test_session', username='test_user_2', loop=loop)
    with pytest.raises(SessionActionNotPermittedException):
        store.update_slot(session_name='test_session', username='test_user_2', slot_number=1, loop=loop)

def test_update_slot_success_new_loop():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.join_session(session_name='test_session', username='test_user_2', inviter='test_user')
    store.add_slot(session_name='test_session', username='test_user')
    loop = Loop(link='http://test.link', creator='test_user', hash='test_hash', created_at='test_timestamp')
    store.update_slot(session_name='test_session', username='test_user', loop=loop, slot_number=1)
    assert len(store['test_session']['library']) == 1
    assert store.get_slots_with_int_keys('test_session')[1] == loop

def test_update_slot_success_loop_exists():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.join_session(session_name='test_session', username='test_user_2', inviter='test_user')
    store.add_slot(session_name='test_session', username='test_user')
    loop = Loop(link='http://test.link', creator='test_user', hash='test_hash', created_at='test_timestamp')
    store.add_loop(session_name='test_session', username='test_user', loop=loop)
    store.update_slot(session_name='test_session', username='test_user', loop=loop, slot_number=1)
    assert len(store['test_session']['library']) == 1
    assert store.get_slots_with_int_keys('test_session')[1] == loop


def test_update_slot_success_empty_loop():
    store = SessionStore()
    store.create_session(session_name='test_session', creator='test_user')
    store.join_session(session_name='test_session', username='test_user_2', inviter='test_user')
    store.add_slot(session_name='test_session', username='test_user')
    loop = Loop(link='http://test.link', creator='test_user', hash='test_hash', created_at='test_timestamp')
    empty_loop = Loop()
    store.add_loop(session_name='test_session', username='test_user', loop=loop)
    store.update_slot(session_name='test_session', username='test_user', loop=loop, slot_number=1)
    store.update_slot(session_name='test_session', username='test_user', loop=empty_loop, slot_number=1)
    assert len(store.get_library('test_session')) == 1
    assert store.get_slots_with_int_keys('test_session')[1] == empty_loop


def test_create_loop():
    loop = Loop(link='http://test.link', creator='test_user', hash='test_hash')
    assert type(loop) == Loop
    assert loop.link == 'http://test.link'
    assert loop.creator == 'test_user'
    assert loop.hash == 'test_hash'
