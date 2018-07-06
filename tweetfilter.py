from datetime import date
from pytz import timezone

def diet_tweet_object(tweet):
    return {
            'text': tweet.full_text,
            'id': tweet.id,
            'created_at': tweet.created_at,
            'reply_to': tweet.in_reply_to_status_id
            }

def search_schedule(tweets):
    def has_schedule(tweet):
        today = date.today()
        today_strs = [
                f'{today.month}/{today.day}',
                f'{today.month}月{today.day}日',
                ]
        created_at = tweet['created_at'].astimezone(timezone('Asia/Tokyo')).date()
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
