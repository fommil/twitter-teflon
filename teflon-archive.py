# Copyright: 2017 - 2018 Sam Halliday
# License: http://www.gnu.org/licenses/gpl-3.0.en.html
#
# This is a variant of teflon.py that gains access to your entire backcatalog of
# tweets, bypassing the 3200 limit on the timeline API, by using the Request
# Archive zip file.
#
# This will unretweet everything you've retweeted, and delete any tweets that are
#
# 1. low scoring (below threshold likes)
# 2. older than an age (e.g. a week)
#
# To run:
#
# 1. create an application at https://apps.twitter.com to get the 4 keys.
# 2. request your archive from twitter and download
# 3. python teflon-archive.py
import datetime
import re
import sys
import tweepy
import time
import zipfile
import os

consumer_key = os.environ['TWITTER_consumer_key']
consumer_secret = os.environ['TWITTER_consumer_secret']
access_token = os.environ['TWITTER_access_token']
access_token_secret = os.environ['TWITTER_access_token_secret']

archive = "/path/to/archive.zip"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler = auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = api.me().screen_name

def archive_cursor():
    with zipfile.ZipFile(archive, 'r') as myzip:
        for entry in myzip.namelist():
            if not entry.startswith("data/js/tweets"):
                continue
            content = str(myzip.read(entry), 'utf-8')
            for m in re.finditer('^  "id" : (\d+),$', content, re.M):
                yield m.group(1)

# http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html
def purge():
    for i in archive_cursor():
        try:
            t = api.get_status(i)
            age = datetime.datetime.utcnow() - t.created_at
            if age.days < 30:
                # prefer teflon.py
                continue
            if t.retweeted or t.text.startswith("RT "):
                print("DELETE (RETWEET): {}".format(t.id))
                api.destroy_status(t.id);
            else:
                counts = t.retweet_count + t.favorite_count
                if counts < 50:
                  print("DELETE (LOW SCORE): http://twitter.com/{}/status/{} counts={} age={}".format(user, t.id, counts, age.days))
                  api.destroy_status(t.id);
                else:
                  print("KEEP: http://twitter.com/{}/status/{} score={} age={}".format(user, t.id, counts, age.days))
        except tweepy.error.TweepError as e:
            print("PROBLEM with {}".format(i))

if __name__ == "__main__":
    purge()

