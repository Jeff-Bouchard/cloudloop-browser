from userstore import UserStore

def add_friends_column(dry_run=True):
    userstore = UserStore(flush=False, redis_host='cloudloop-rejson')
    for username in userstore.get_all_usernames():
        user = userstore[username]
        if not user['friends']:
            user['friends'] = []
        print(user)
        if not dry_run:
            userstore.update_user(username, user)
