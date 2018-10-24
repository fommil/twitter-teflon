# Copyright: 2017 - 2018 Sam Halliday
# License: http://www.gnu.org/licenses/gpl-3.0.en.html
#
# Similar to unlike.py but uses the like.js obtained from
#
# Settings and Privacy => Your Twitter Data => Download Data
#
# then take like.js, remove the jsonp bit and save as like.json
import tweepy
import time
import sys
import os
import json

consumer_key = os.environ['TWITTER_consumer_key']
consumer_secret = os.environ['TWITTER_consumer_secret']
access_token = os.environ['TWITTER_access_token']
access_token_secret = os.environ['TWITTER_access_token_secret']

archive = "like.json"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler = auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = api.me().screen_name

def archive_cursor():
    with open(archive) as json_data:
        for entry in json.load(json_data):
            yield int(entry['like']['tweetId'])

# http://docs.tweepy.org/en/v3.5.0/api.html
# http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html

# https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-favorites-list
# 75 / 15 minutes

# https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/post-favorites-destroy
# unspecified rate limit

if __name__ == "__main__":
    for i in archive_cursor():
        print("trying {}".format(i))
        try:
            api.get_status(i)
        except tweepy.error.RateLimitError:
            print("RATE LIMIT!")
            sys.exit(1)
        except tweepy.error.TweepError as e:
            if e.api_code == 136:
                continue;
            print("FAILURE UNEXPECTED {} {}".format(i, e))
            sys.exit(1)
        try:
            # we could avoid this by detecting the Troolean state better
            api.destroy_favorite(i)
            print("SUCCESS {}".format(i))
        except tweepy.error.RateLimitError:
            print("RATE LIMIT!")
            sys.exit(1)
        except tweepy.error.TweepError as e:
            if e.api_code == 144:
                try:
                    print("retrying {}".format(i))
                    api.create_favorite(i)
                    api.destroy_favorite(i)
                except tweepy.error.RateLimitError:
                    print("RATE LIMIT!")
                    sys.exit(1)
                except tweepy.error.TweepError as e2:
                    print("FAILURE {} {}".format(i, e2))
            else:
                print("FAILURE {} {}".format(i, e))
