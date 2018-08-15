# Copyright: 2017 - 2018 Sam Halliday
# License: http://www.gnu.org/licenses/gpl-3.0.en.html
#
# This will unfavorite / unlike everything that is exposed over the public API.
#
# To run:
#
# 1. create an application at https://apps.twitter.com to get the 4 keys.
# 2. python unlike.py
# 3. script finishes, check twitter, oh no, still lots of likes left.
# 4. Realise that twitter's implementation is a raging dumpster fire.
# 5. https://twittercommunity.com/t/many-tweets-in-a-zombie-favorite-but-not-favorite-state/105620
# 6. :facepalm:
# 7. go and "like" everything via the UI with the accompanying javascript tool
# 8. repeat
import tweepy
import time
import sys
import os

consumer_key = os.environ['TWITTER_consumer_key']
consumer_secret = os.environ['TWITTER_consumer_secret']
access_token = os.environ['TWITTER_access_token']
access_token_secret = os.environ['TWITTER_access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler = auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = api.me().screen_name

# http://docs.tweepy.org/en/v3.5.0/api.html
# http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html

# https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-favorites-list
# 75 / 15 minutes

# https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/post-favorites-destroy
# unspecified rate limit

def purge():
    print("getting likes")
    tweets = api.favorites(user)
    if len(tweets) == 0:
        print("no favorites left")
        sys.exit(0)
    for f in tweets:
        try:
          api.destroy_favorite(f.id)
          print("SUCCESS {}".format(f.text))
        except tweepy.error.TweepError:
          print("FAILURE {} {}".format(f.text, f.id))

if __name__ == "__main__":
    while 1:
        purge()
