import requests
import json

def post_to_slack(url, payload):
    requests.post(url, data=json.dumps(payload))

if __name__ == '__main__':
    url = open('url.txt').readline().strip()
    payload = json.load(open('payload.json'))
    payload['text'] = 'post test'
    post_to_slack(url, payload)
