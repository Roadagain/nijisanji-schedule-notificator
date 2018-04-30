from requests_oauthlib import OAuth1Session
import json

# load tokens
with open('tokens.json') as json_data:
    tokens = json.load(json_data)
    json_data.close()

url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
params = { 'user_id': 'nijisanji_app' }

CK, CKS, AT, ATS = [tokens['consumerKey'], tokens['consumerKeySecret'], tokens['accessToken'], tokens['accessTokenSecret']]
twitter = OAuth1Session(CK, CKS, AT, ATS)
req = twitter.get(url, params=params)

if req.status_code == 200:
    data = json.loads(req.text)
    tweets = list(map(lambda x: x['text'], data))
    with open('result.txt', 'w') as result:
        result.write(json.dumps({'tweets': tweets}, ensure_ascii=False))
    # print(data)
else:
    print(req.status_code)
