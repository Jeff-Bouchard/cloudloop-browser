import grequests

users = [f'user-{x}' for x in range(50)]
host = 'https://cloudloop.io/'

actions = []

for user in users:
    actions.append(grequests.post(f'{host}register_user', data='{"username":"user", "password":"password", "email:"me@me.com"}'))

grequests.map(actions)
