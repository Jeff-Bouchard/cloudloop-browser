from user import User
from loop import Loop
from json import JSONDecoder, JSONEncoder


class CloudLoopEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object, User):
            # encode salted password to string for JSON
            user_dict = object.__dict__
            user_dict['password_hash'] = user_dict['password_hash'].decode('utf-8')
            return user_dict
        elif isinstance(object, Loop):
            return object.__dict__
        else:
            return JSONEncoder.default(self, object)


class CloudLoopDecoder(JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=custom_type_hook)


def custom_type_hook(dct):
    if "_type" in dct:
        if dct["_type"] == "User":
            # Never return password hash.
            return User(username=dct['username'], email=dct['email'], sessions=dct['sessions'], friends=dct['friends'])
        elif dct["_type"] == "Loop":
            return Loop(link=dct['link'], creator=dct['creator'], hash=dct['hash'], created_at=dct['created_at'])
        else:
            return dct
    else:
        return dct
