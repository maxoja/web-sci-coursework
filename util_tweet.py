import tweepy
import time
import api_mongo as mongo
import config
from credentials import *

def autenticate():

    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    api = tweepy.API(auth)
    return api

def crawl_rest_tweets(api, searchQuery, sinceId=None, max_id=-1, tweetCount=0): # "#python"
    maxTweets = 10000 # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits

    try:
        if (max_id <= 0):
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended')
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                        since_id=sinceId, tweet_mode='extended')
        else:
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                        max_id=str(max_id - 1), tweet_mode='extended')
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                        max_id=str(max_id - 1),
                                        since_id=sinceId, tweet_mode='extended')
        tweetCount += len(new_tweets)
        print("Downloaded {0} tweets".format(len(new_tweets)))
        max_id = new_tweets[-1].id
        return new_tweets, sinceId, max_id, tweetCount
    except tweepy.TweepError as e:
        # Just exit if any error
        print("stop with error", str(e))
        return None

def crawl_user_timeline(api, user_id):
    result = []
    try:
        new_tweets = api.user_timeline(user_id, tweet_mode='extended')
        time.sleep(1/((1500/900)*0.9))
        print(f"Downloaded {len(new_tweets)} tweets for user {user_id}")
        max_id = new_tweets[-1].id
        result += new_tweets

        # new_tweets = api.user_timeline(user_id, tweet_mode='extended', since_id=max_id)
        # time.sleep(1/((1500/900)*0.9))
        # print(f"Downloaded {len(new_tweets)} tweets for user {user_id}")
        # result += new_tweets
        return result

    except tweepy.TweepError as e:
        # Just exit if any error
        print("stop with error", str(e))
        return None

def crawl_rest_users(api, user_ids:[int]): # "#python"
    # return api.get_user(user_id)
    return api.lookup_users(user_ids)
    
if __name__ == "__main__":
    api = autenticate()
    print("authentication success")
    sample_user_id = 1228773433015701506
    print("success in crawling user", crawl_rest_users(api,[sample_user_id]))

