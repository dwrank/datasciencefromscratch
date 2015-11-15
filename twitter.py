#!/usr/bin/env python

from __future__ import division

import sys
import json
from twython import Twython
from pprint import pprint
from twython.streaming.api import TwythonStreamer
from collections import Counter


def basic_query(consumer_key, consumer_secret):
    twitter = Twython(consumer_key, consumer_secret)
    
    # search for tweets containing the phrase "data science"
    for status in twitter.search(q='"data science"')['statuses']:
        user = status['user']['screen_name'].encode('utf-8')
        text = status['text'].encode('utf-8')
        print('%s : %s\n' % (user, text))


class MyStreamer(TwythonStreamer):
    '''specifies how to interact with the stream'''
    def __init__(self, selfconsumer_key, consumer_secret,
             access_token, access_token_secret,
             count):
        super(MyStreamer, self).__init__(selfconsumer_key, consumer_secret,
                                         access_token, access_token_secret)
        self.tweets = []
        self.count = count
        
    def on_success(self, data):
        '''handle data sent by twitter'''
        
        # filter out non-english tweets
        try:
            if data['lang'] == 'en':
                self.tweets.append(data)
                print('received tweet #%d: %s' % (len(self.tweets), data['entities']['hashtags'][0]['text']))
                sys.stdout.flush()
        except:
            pass
        
        # stop when we've collected enough
        if len(self.tweets) >= self.count:
            self.disconnect()

    def on_error(self, status_code, data):
        print status_code, data
        self.disconnect()


if __name__ == '__main__':
    with open('credentials.json', 'r') as f:
        json_data = json.loads(f.read())
    
    #basic_query(json_data['Consumer Key'], json_data['Consumer Secret'])
    
    stream = MyStreamer(json_data['Consumer Key'], json_data['Consumer Secret'],
                        json_data['Access Token'], json_data['Access Token Secret'],
                        1000)
    
    # starts consuming public statuses that contain the keyword 'data'
    #stream.statuses.filter(track='data')
    
    # if instead we wanted to start consuming a sample of *all* public statuses
    stream.statuses.sample()
    
    top_hashtags = Counter(hashtag['text'].lower()
                           for tweet in stream.tweets
                           for hashtag in tweet['entities']['hashtags'])
    
    print('Top 5: %s' % str(top_hashtags.most_common(5)))