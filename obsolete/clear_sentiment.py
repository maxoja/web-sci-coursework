import util_tweet
import api_mongo as mongo
import config
import time
import api_sentiment

db = mongo.connect_to_db()

# db['statuses'].update({},{"$unset":{"polarity":0}}, multi=True)
# db['statuses'].remove({"$and":[{"truncated":True},{"extended_tweet":{"$exists":False}}]},multi=True)