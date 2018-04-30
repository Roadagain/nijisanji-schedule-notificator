import json
import fetcher
import poster

def main():
    config = json.load(open('config.json'))
    tokens = config['tokens']
    payload = config['payload']
    url = config['webhook_url']

    tweets = fetcher.fetch_nijisanji_tweets(tokens)
    schedule_id = fetcher.search_schedule(tweets)['id']
    payload['text'] = 'https://twitter.com/nijisanji_app/status/' + str(schedule_id)
    poster.post_to_slack(url, payload)

if __name__ == '__main__':
    main()
