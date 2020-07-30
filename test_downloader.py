import grequests

demo_skylink= [
        'sia://AADgNCmJ-8S0Bgm3pkJUfR17UTTYN-KYXTglQm9_jv3lGg',
        'sia://AABGmWEkMuYfXVWslXJGuS0cOYPAhyp-sz7Qz4a6Kt7Z8g',
        'sia://AADIlFgsjFRp5NjW8-NDDh4wexzsHSELy_Zt0OEYNatKvw',
        'sia://AAAhXjOgsmTpW4xeMXI00lwx4Frh2rlzLyg3uwSAUR-0SA',
        'sia://AAB0WxMLTIjdXj2YUwTvwAvTPnaPxeGx7AucBvF7Qp-g7g'
        ]

host='https://cloudloop.io/download'
action_items = []


for skylink in demo_skylink:
    action_items.append(grequests.get(f'{host}?skylink={skylink}', hooks= { 'response':print(f'done with {skylink}')}))

grequests.map(action_items)
