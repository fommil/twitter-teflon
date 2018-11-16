# Copyright: 2017 - 2018 Sam Halliday
# License: http://www.gnu.org/licenses/gpl-3.0.en.html
#
# This will unretweet everything you've retweeted, and delete any tweets that are
#
# 1. low scoring (below threshold likes)
# 2. older than an age (e.g. a week)
#
# To run:
#
# 1. create an application at https://apps.twitter.com to get the 4 keys.
# 2. python teflon.py
import datetime
import sys
import tweepy
import time
import os

consumer_key = os.environ['TWITTER_consumer_key']
consumer_secret = os.environ['TWITTER_consumer_secret']
access_token = os.environ['TWITTER_access_token']
access_token_secret = os.environ['TWITTER_access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler = auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = api.me().screen_name

# http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html
def purge():
    for t in tweepy.Cursor(api.user_timeline).items():
        age = datetime.datetime.utcnow() - t.created_at
        if age.days < 1:
            continue
        if t.retweeted:
            print("DELETE (RETWEET): {}".format(t.id))
            api.destroy_status(t.id);
        else:
            counts = t.retweet_count + t.favorite_count
            if counts > 5 and age.days < 7:
              continue
            if counts > 10 and age.days < 30:
              continue
            if counts < 20:
              print("DELETE (LOW SCORE): http://twitter.com/{}/status/{} counts={} age={}".format(user, t.id, counts, age.days))
              api.destroy_status(t.id);
            else:
              print("KEEP: http://twitter.com/{}/status/{} score={} age={}".format(user, t.id, counts, age.days))

if __name__ == "__main__":
    purge()
