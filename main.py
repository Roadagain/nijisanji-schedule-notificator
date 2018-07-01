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

    if os.path.exists(OLD_SCHEDULE):
        old_schedule_id = int(open(OLD_SCHEDULE).readline().strip() or 0)
    else:
        old_schedule_id = 0

    tweets = fetcher.fetch_nijisanji_tweets(tokens)
    schedule_tweets = [t for t in fetcher.search_schedule(tweets) if t['id'] > old_schedule_id]
    if schedule_tweets == []:
        schedule_id = 0
    else:
        print(schedule_tweets)
        schedule_id = schedule_tweets[0]['id']
    if schedule_id > old_schedule_id:
        ids = [str(tweet['id']) for tweet in schedule_tweets]
        links = ['https://twitter.com/nijisanji_app/status/' + i for i in ids]
        payload['text'] = '\n'.join(links)
        poster.post_to_slack(url, payload)
        open(OLD_SCHEDULE, 'w').write(str(schedule_id))

if __name__ == '__main__':
    main()
