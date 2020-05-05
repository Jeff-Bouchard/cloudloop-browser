import datetime

class Loop(object):
    def __init__(self, link, creator, hash, created_at=None):
        dict.__init__(self, link=link, creator=creator, hash=hash, created_at=datetime.datetime.now().isoformat())
