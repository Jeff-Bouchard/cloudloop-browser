import datetime
from json import JSONEncoder
from json import JSONDecoder


class Loop(object):
    _type = "Loop"
    link = None
    creator = None
    hash = None
    created_at = None
    def __init__(self, link='', creator='', hash='', created_at=None):
        self._type = "Loop"
        self.link = link
        self.creator = creator
        self.hash = hash
        self.created_at = created_at if created_at else datetime.datetime.now().isoformat()

    def __str__(self):
        return f'{self._type}: Link:{self.link} Hash:{self.hash} Creator:{self.creator} CreatedAt: {self.created_at}'

    def __eq__(self, other):
        if isinstance(other, Loop):
            if other.link == self.link and \
                other.creator == self.creator and \
                other.hash == self.hash and \
                other.created_at == self.created_at:
                return True
            else:
                return False
        else:
            return False