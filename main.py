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
    schedule_id = str(fetcher.search_schedule(tweets)['id'])
    if os.path.exists(OLD_SCHEDULE):
        old_schedule_id = open(OLD_SCHEDULE).readline().strip()
    else:
        old_schedule_id = None
    if schedule_id != old_schedule_id:
        payload['text'] = 'https://twitter.com/nijisanji_app/status/' + schedule_id
        poster.post_to_slack(url, payload)
        open(OLD_SCHEDULE, 'w').write(schedule_id)

if __name__ == '__main__':
    main()
