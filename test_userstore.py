import pytest


@pytest.fixture
def store():
    from userstore import UserStore
    return UserStore(flush=True)


def test_userstore_init(store):
    assert store._data == dict()
    assert list(store._data.keys()) == []


def test_search_usernames(store):
    results = store.search_users(query='dummy')
    assert results == []


def test_search_usernames(store):
    store.create_user(username='test1', password='password1')
    results = store.search_users(query='st')
    assert len(results) == 1
    assert results[0] == 'test1'
