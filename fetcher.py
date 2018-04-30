import tweepy
import json
import re


def fetch_nijisanji_tweets(tokens):
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
        return map(lambda x: {'text': x.text, 'id': x.id}, data)
    except tweepy.error.TweepError as e:
        print(e)
        exit(-1)

def search_schedule(tweets):
    pattern = re.compile(r'\d+:\d+')
    for tweet in tweets:
        if pattern.search(tweet['text'].replace('\n', '')):
            return tweet
    return None

if __name__ == '__main__':
    tokens = json.load(open('config.json'))['tokens']
    tweets = fetch_tweets(tokens)
    with open('result.txt', 'w') as result:
        result.write(json.dumps({'tweets': tweets}, ensure_ascii=False))
