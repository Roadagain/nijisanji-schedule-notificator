import json
import fetcher
import poster
import os

OLD_SCHEDULE = 'old_schedule.txt'

def main():
    config = json.load(open('config.json'))
    tokens = config['tokens']
    payload = config['payload']
    url = config['webhook_url']

    tweets = fetcher.fetch_nijisanji_tweets(tokens)
    schedule_tweet = fetcher.search_schedule(tweets)
    if schedule_tweet is None:
        schedule_id = 0
    else:
        schedule_id = schedule_tweet['id']
    if os.path.exists(OLD_SCHEDULE):
        old_schedule_id = int(open(OLD_SCHEDULE).readline().strip() or 0)
    else:
        old_schedule_id = 0
    if schedule_id > old_schedule_id:
        payload['text'] = 'https://twitter.com/nijisanji_app/status/' + str(schedule_id)
        poster.post_to_slack(url, payload)
        open(OLD_SCHEDULE, 'w').write(str(schedule_id))

if __name__ == '__main__':
    main()
