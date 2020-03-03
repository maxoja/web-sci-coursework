import util_tweet
import api_mongo as mongo
import config
import time
import my_util
import nltk
import sys

def get_most_mentioned_users(api, db):
    print(f'collection size =', db.get_collection('statuses').count())

    target_statuses = list(db.get_collection('statuses').find())

    mentioned_users = [s['entities']['user_mentions'] for s in target_statuses]
    mentioned_users = [u['id'] for l in mentioned_users for u in l]
    print('number of all mentions =', len(mentioned_users))

    fdist = nltk.FreqDist(mentioned_users)
    stats = fdist.most_common()
    most_mentioned_users = stats[:100]
    most_mentioned_users = [item[0] for item in most_mentioned_users]

    return most_mentioned_users


def crawl_users_timeline(api, db, users):
    for u in mentioned_users:
        statuses = util_tweet.crawl_user_timeline(api, u)
        if statuses is None:
            continue
        for s in statuses:
            mongo.insert_unique_status(db, s)


if __name__ == '__main__':
    minutes = int(sys.argv[1])
    timer = my_util.Timer(minutes)
    timer.start()
    db = mongo.connect_to_db()
    api = util_tweet.autenticate()

    # keep getting popular mentioned users and crawl their feed
    while timer.out_of_time() == False:
        mentioned_users = get_most_mentioned_users(api, db)
        crawl_users_timeline(api, db, mentioned_users)
