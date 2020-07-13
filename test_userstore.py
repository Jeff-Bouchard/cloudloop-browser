import pytest
from userstore import UserStore

def test_userstore_init():
    store = UserStore(flush=True)
    assert store._data == dict()
    assert list(store._data.keys()) == []


def test_userstore_get_session_names_empty():
    store = UserStore(flush=True)
    names = store.get_session_names()
    assert names == []