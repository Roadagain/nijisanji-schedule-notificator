import tweepy
import json
import re
import datetime
import pytz
import itertools
import functools

def diet_tweet_object(tweet):
    return {
            'text': tweet.full_text,
            'id': tweet.id,
            'created_at': tweet.created_at,
            'reply_to': tweet.in_reply_to_status_id
            }

def fetch_tweets(screen_name, tokens):
    auth = tweepy.OAuthHandler(tokens['consumer_key'], tokens['consumer_secret'])
    auth.set_access_token(tokens['access_token'], tokens['access_token_secret'])
    params = {
            'screen_name': screen_name,
            'exclude_replies': False,
            'trim_user': True,
            'tweet_mode': 'extended',
            }

    api = tweepy.API(auth)
    try:
        data = api.user_timeline(**params)[::-1]
        return map(diet_tweet_object, data)
    except tweepy.error.TweepError as e:
        print(e)
        exit(-1)

def fetch_nijisanji_tweets(tokens):
    accounts = ['nijisanji_app', 'NijisanjiGamers', 'Nijisanji_Seeds']
    tweets = [fetch_tweets(i, tokens) for i in accounts]
    return functools.reduce(itertools.chain, tweets)

def search_schedule(tweets):
    def has_schedule(tweet):
        today = datetime.date.today()
        today_strs = [
                f'{today.month}/{today.day}',
                f'{today.month}月{today.day}日',
                ]
        created_at = tweet['created_at'].astimezone(pytz.timezone('Asia/Tokyo')).date()
        if today == created_at:
            today_strs.append('本日')
        text = tweet['text'].replace('\n', ' ')
        return any([s in text for s in today_strs])

    indexed_tweets = {}
    scheduled = []
    for tweet in tweets:
        indexed_tweets[tweet['id']] = tweet
        reply_to = tweet['reply_to']
        if has_schedule(tweet):
            scheduled.append(tweet)
        elif reply_to in indexed_tweets and has_schedule(indexed_tweets[reply_to]):
            # TODO: 再帰的にリプライを遡る
            scheduled.append(tweet)
    return scheduled

if __name__ == '__main__':
    tokens = json.load(open('config.json'))['tokens']
    tweets = list(fetch_nijisanji_tweets(tokens))
    schedule = search_schedule(tweets)
    print(schedule)
    with open('result.json', 'w') as result:
        result.write(json.dumps({'tweets': tweets}, ensure_ascii=False))
