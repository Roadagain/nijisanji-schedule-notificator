import tweepy
import json
from itertools import chain
from functools import reduce
import tweetfilter
from datetime import datetime

def fetch_tweets(screen_name, tokens):
    auth = tweepy.OAuthHandler(tokens['consumer_key'], tokens['consumer_secret'])
    auth.set_access_token(tokens['access_token'], tokens['access_token_secret'])
    params = {
            'screen_name': screen_name,
            'exclude_replies': False,
            'include_rts': False,
            'trim_user': True,
            'tweet_mode': 'extended',
            }

    api = tweepy.API(auth)
    try:
        data = api.user_timeline(**params)[::-1]
        return map(tweetfilter.diet_tweet_object, data)
    except tweepy.error.TweepError as e:
        print(e)
        exit(-1)

def fetch_nijisanji_tweets(tokens):
    accounts = ['nijisanji_app', 'NijisanjiGamers', 'Nijisanji_Seeds']
    tweets = [fetch_tweets(i, tokens) for i in accounts]
    return reduce(chain, tweets)

if __name__ == '__main__':
    def support_datetime_default(o):
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(repr(o) + " is not JSON serializable")

    tokens = json.load(open('config.json'))['tokens']
    tweets = list(fetch_nijisanji_tweets(tokens))
    schedule = tweetfilter.search_schedule(tweets)
    print(schedule)
    dumped_tweets = json.dumps({'tweets': tweets}, ensure_ascii=False, default=support_datetime_default)
    with open('result.json', 'w') as result:
        result.write(dumped_tweets)
