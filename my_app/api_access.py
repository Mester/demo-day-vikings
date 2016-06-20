import requests
from pprint import pprint as pp

# copy key i posted in slack here
client_id = "COPY IT HERE"
client_secret = "COPY IT HERE"

song_posts = []

client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
post_data = {"grant_type": "client_credentials"}
reddit_headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
r = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=reddit_headers)
print "### ACCESS TOKEN REQUEST ###"
print r.status_code

if r.ok:
    pp(r.json())
    token = r.json()['access_token']

    headers = {"Authorization": "bearer " + token, "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    r = requests.get("https://oauth.reddit.com/r/ListenToThis/hot", headers=headers)
    print r.status_code
    print "### REDDIT API DATA REQUEST ###"
    if r.ok:
        for post in r.json()['data']['children']:
            song_posts.append(post['data']['title'])

pp(song_posts)
