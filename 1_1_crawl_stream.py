import api_mongo as mongo
import util_tweet
import tweepy
import config
import my_util
import sys

class StreamListener(tweepy.StreamListener):
    def __init__(self, timer:my_util.Timer):
        timer.start()
        self.timer= timer
        super(StreamListener, self).__init__()

    def set_db(self, db):
        self.db = db

    def on_status(self, status):
        if self.timer.out_of_time():
            return False

        # uniquely insert the obtained status to mongo DB (automatically deny duplicates)
        mongo.insert_unique_status(self.db, status)
        print('insert status with timestamp:', status.timestamp_ms)
        return True

    def on_error(self, status_code):
        print('error', status_code)

def start(timer:my_util.Timer):
    db = mongo.connect_to_db()
    myStreamListener = StreamListener(timer)
    myStreamListener.set_db(db)
    
    api = util_tweet.autenticate()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(languages=['en'], track=config.chosen_topics, locations=config.worldwide_locations, is_async=False)
    print("done")

if __name__ == '__main__':
    # run stream crawler by the given duration
    minute = int(sys.argv[1])
    start(my_util.Timer(minute))