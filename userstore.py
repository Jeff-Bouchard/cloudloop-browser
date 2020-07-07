from rejson import Client, Path
from user import User
from serde import CloudLoopDecoder, CloudLoopEncoder
import bcrypt
import logging

USER_JWT_PRIVATE_KEY='''-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEAu4fYnMBWsc55c5QLc1DpxQSs1Xr7TnBkLrScxl/GjAHd8H6Qc5SZ
WtLWaTnBBNJYaMKn5I+LvCqDATh8pe1ow0W6I9lvETtGPkszh3lV7mJUcq6/y8UnV9HpNm
81rk6TKlPsiSpqdPBKdr65FEJ49fiKS8ES9GZ/4UmlsGafRKjhWZnQ9Ava4yah8BsKyNCR
3jg96xxcseDxslQ2yH8fpaF8nfjora/JvOqgvUcBWAvDXxhH9gd886PomsQ+OzreArJPux
TiVCVwp9QHDFzuVZMXdoBfr0t7lR8ZlKND5Y5JievF8lUow/L5CmhZXc1qGM4MzGNhnL72
ov098Jbs9QAAA9BRPYCtUT2ArQAAAAdzc2gtcnNhAAABAQC7h9icwFaxznlzlAtzUOnFBK
zVevtOcGQutJzGX8aMAd3wfpBzlJla0tZpOcEE0lhowqfkj4u8KoMBOHyl7WjDRboj2W8R
O0Y+SzOHeVXuYlRyrr/LxSdX0ek2bzWuTpMqU+yJKmp08Ep2vrkUQnj1+IpLwRL0Zn/hSa
WwZp9EqOFZmdD0C9rjJqHwGwrI0JHeOD3rHFyx4PGyVDbIfx+loXyd+Oitr8m86qC9RwFY
C8NfGEf2B3zzo+iaxD47Ot4Csk+7FOJUJXCn1AcMXO5Vkxd2gF+vS3uVHxmUo0PljkmJ68
XyVSjD8vkKaFldzWoYzgzMY2Gcvvai/T3wluz1AAAAAwEAAQAAAQEAuchFIlWyDYi97XC3
P1DjpxmQmBW0LetOdK7dufFcY4vd8cmRFdAbdUz2uVxMCpjQmUhuyBIlnw6Gpojtg/yFEx
9a3vUkAXA1kLUzoXzlUrr7anoQ7LCu32PHpPPbvIl/ZimqZeEtghgjzSv5c0a/Sv8lExN9
0b5R5kDt8qpYEs2BMMaBPWdLiwlKEhHTcp2PbluT/DA6hJhzBKNqxZ7X9qrWWMhp2dGxJz
s8vncTpTiFL1S3Q/NuXMmqt6lZLgXVKRRcr5R1KW4I0I34RN1Td2LwLHcPx9OKwIdSqLru
p/kda8+Bqsb8IAFyhIxLO0bPEZnFBkVA0jvItoH1bd1o6QAAAIEA0wu1mtFZAafFn4iOvJ
WPo099jcRRiBcbE/EbEybD6/SxDmzSQqiat66VUYhGcJFR3N9RaK0cChDUjUlutxV7nH0K
SRIO2TgfBoy1QdxRPUs63V7CsUH5QNVwKD8cPMEoXDVmfzR2+psSLO5QTIUUJfXs8vSgZ3
uL1NCLBx/0yv8AAACBAOjrzj36vjXvSABZg6c3nuDuQHLefFpTyuNYZno/AvqeMf5y5XrF
F7yqGjlX7u11I7xsozZVJ2reHWs3kvJpQvD1vKTaQJjcPVM+lKlbmMF5o9VuC8tQYBJmWx
EfYvVvEAp4Nkzscd1vhl2/T3bQ+AgBOVU16DCGbSzuep0d/yaDAAAAgQDOHK6Z6/NKtoOZ
kiDbnMxVX99uqLW3YpfT9bR8tl14WniMvCpj/Lh3Vxq8iobbPaILyiUcgiIfKHWTlL9PXw
8bGcavKRdUekCByda9kGFpMPuBqKkVOxSw977a7rgmpLSXKrQaR9nR2flB6iEEJVCtiO/8
cIBqcYBz8+L4c5KFJwAAABRkYXRhbWFuY2VyQHByby5sb2NhbAECAwQF
-----END OPENSSH PRIVATE KEY-----'''
USER_JWT_PUBLIC_KEY='''ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7h9icwFaxznlzlAtzUOnFBKzVevtOcGQutJzGX8aMAd3wfpBzlJla0tZpOcEE0lhowqfkj4u8KoMBOHyl7WjDRboj2W8RO0Y+SzOHeVXuYlRyrr/LxSdX0ek2bzWuTpMqU+yJKmp08Ep2vrkUQnj1+IpLwRL0Zn/hSaWwZp9EqOFZmdD0C9rjJqHwGwrI0JHeOD3rHFyx4PGyVDbIfx+loXyd+Oitr8m86qC9RwFYC8NfGEf2B3zzo+iaxD47Ot4Csk+7FOJUJXCn1AcMXO5Vkxd2gF+vS3uVHxmUo0PljkmJ68XyVSjD8vkKaFldzWoYzgzMY2Gcvvai/T3wluz1 datamancer@pro.local'''

_log = logging.getLogger(__name__)

class UserStore(object):
    """
    UserStore is a secondary Redis DB which stores user data.
    """
    def __init__(self, flush=True, redis_host='cloudloop-rejson'):
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
            print(f"Storing user {user.__dict__}")
            self._rejson.jsonset(username, Path.rootPath(), user)
        else:
            return False
        return True

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
            _log.info(f'User {username} already in session {session_name}.')
            return True

    def get_user_sessions(self, username):
        return self._rejson.jsonget(username, '.sessions')

    def get_user(self, username):
        if self._rejson.exists(username):
            user = self._rejson.jsonget(username)
            return user
        else:
            return None  # Maybe dont do this

    def get_user_password_hash(self, username):
        if self._rejson.exists(username):
            return self._rejson.jsonget(username, Path(".password_hash"))

    def delete_user(self, username):
        if self._rejson.exists(username):
            self._rejson.jsondel(username)
        else:
            return False
        return True

    def update_user(self, username, user):
        if self._rejson.exists(username):
            self._rejson.jsonset(username, Path.rootPath(), user)
        else:
            return False

    def check_password(self, username, password):
        if self._rejson.exists(username):
            password_hash = self.get_user_password_hash(username).encode('utf-8')
            if bcrypt.hashpw(password.encode('utf-8'), password_hash) == password_hash:
                return True
            else:
                return False
        else:
            return False

    def get_all_usernames(self):
        return list(self._rejson.scan_iter())

    def get_friends(self, username):
        friends = []
        if self._rejson.exists(username):
            user = self._rejson[username]
            if user['friends']:
                friends = user['friends']
            else:
                _log.warning(f'No "friends" item for user {username} - apply migration.')
        else:
            _log.warning(f'No username {username} exists in UserStore.')
        return friends

    def add_friend_one_way(self, username, friend_username):
        """
        This (almost atomically) adds a user to friends list one way.
        """
        friend_exists = self._rejson.jsonarrindex(username, '.friends', friend_username)
        if friend_exists < 0:
            self._rejson.jsonarrappend(username, '.friends', friend_username)
            _log.info(f'{username} added {friend_username} as friend.')
        else:
            _log.warning(f'{friend_username} already in friends list for {username} at index {friend_exists}.')

    def add_friend_mutual(self, username, friend_username):
        """
        This adds users mutally to friends list. No approval mechanism for now.
        """
        if self._rejson.exists(username):
            if self._rejson.exists(friend_username):
                self.add_friend_one_way(username, friend_username)
                self.add_friend_one_way(friend_username, username)
            else:
                _log.error(f'No username exists for {friend_username} while adding as friend for {username}.')
        else:
            _log.error(f'No username {username} exists in userstore.')
