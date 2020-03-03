import util_tweet
import api_mongo as mongo
import config
import time
import my_util
import nltk
import sys

def start(use_async:bool):
    db = mongo.connect_to_db()
    api = util_tweet.autenticate()

    while True:
        users_allow_per_req = 100
        try:
            statuses = list(db.get_collection('statuses').aggregate([
                { "$match": { "userLoaded": { "$exists": False } } },
    { "$sample": { "size": users_allow_per_req } }
]))
            if len(statuses) == 0:
                print('no uses info left to be crawled sleep a while')
                time.sleep(30)
                
            poster_ids = [ status['user']['id'] for status in statuses ]
            users = util_tweet.crawl_rest_user(api,poster_ids)
            for user in users:
                mongo.insert_unique_user(db,user)
            for status in statuses:
                db['statuses'].update_one(
                    {'id':status['id']},
                    {"$set":{'userLoaded':True}}
                )

        except Exception as e:
            print(e)
            print("sleep for 1 mins")
            time.sleep(15*1)
    
def get_most_mentioned_users(api,db):
    print(f'collection size =', db.get_collection('statuses').count())
    
    # target_statuses = list(db.get_collection('statuses').aggregate([
    #     { "$match": { "mentioned_users_crawled": { "$exists": False } } },
    #     { "$sample": { "size": 100 } }
    # ]))

    target_statuses = list(db.get_collection('statuses').find())

    mentioned_users = [ s['entities']['user_mentions'] for s in target_statuses]
    mentioned_users = [ u['id'] for l in mentioned_users for u in l]
    print('number of all mentions =', len(mentioned_users))

    fdist = nltk.FreqDist(mentioned_users)
    stats = fdist.most_common()
    most_mentioned_users = stats[:100]
    most_mentioned_users = [ item[0] for item in most_mentioned_users]

    return most_mentioned_users

def crawl_users_timeline(api, db, users):
    for u in mentioned_users:
        statuses = util_tweet.crawl_user_timeline(api, u)
        if statuses is None:
            continue
        for s in statuses:
            mongo.insert_unique_status(db,s)

if __name__ == '__main__':
    minutes = int(sys.argv[1])
    timer = my_util.Timer(minutes)
    timer.start()
    db = mongo.connect_to_db()
    api = util_tweet.autenticate()
    
    while timer.out_of_time() == False:
        mentioned_users = get_most_mentioned_users(api,db)
        crawl_users_timeline(api, db, mentioned_users)