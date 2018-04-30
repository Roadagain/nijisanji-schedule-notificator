import tweepy
import json

# load tokens
with open('tokens.json') as json_data:
    tokens = json.load(json_data)
    json_data.close()

auth = tweepy.OAuthHandler(tokens['consumer_key'], tokens['consumer_secret'])
auth.set_access_token(tokens['access_token'], tokens['access_token_secret'])
params = {
        'screen_name': 'nijisanji_app',
        'exclude_replies': True,
        'trim_user': True,
        }

api = tweepy.API(auth)
try:
    data = api.user_timeline(**params)
except tweepy.error.TweepError as e:
    print(e)
    exit(-1)
tweets = list(map(lambda x: x.text, data))

with open('result.txt', 'w') as result:
    result.write(json.dumps({'tweets': tweets}, ensure_ascii=False))
# print(data)
