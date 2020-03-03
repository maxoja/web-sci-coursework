import util_tweet
import api_mongo as mongo
import config
import time

def start(use_async:bool):
    db = mongo.connect_to_db()
    api = util_tweet.autenticate()

    while True:
        result = util_tweet.crawl_rest_tweets(api,config.rest_query)
        while not result is None:
            tweets, a, b, c = result
            for tweet_status in tweets:
                mongo.insert_unique_status(db, tweet_status)
            result = util_tweet.crawl_rest_tweets(api,config.rest_query, a, b, c)

        time.sleep(60*1)


    
if __name__ == '__main__':
    start(False)