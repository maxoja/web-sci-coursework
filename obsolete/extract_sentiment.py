import util_tweet
import api_mongo as mongo
import config
import time
import api_sentiment

def start():
    db = mongo.connect_to_db()
    batch_size = 1000
    progress = 0
    while True:
        try:
            statuses = list(db.get_collection('statuses').aggregate([
                { "$match": { "polarity": { "$exists": False } } },
                { "$sample": { "size": batch_size } }
            ]))

            for status in statuses:
                status_id = status['id']
                if status['truncated'] == False:
                    if 'text' in status:
                        polarity = api_sentiment.calculate_polarity(status['text'])
                    else:
                        polarity = api_sentiment.calculate_polarity(status['full_text'])
                else:
                    polarity = api_sentiment.calculate_polarity(status['extended_tweet']['full_text'])

                db['statuses'].update_one({'id':status_id},{"$set":{"polarity":polarity}})
                progress += 1
                print('update status with id', status_id, "\tprogress",progress)
            
            if len(statuses) == 0:
                print('all statuses were analysed, sleep a while')
                time.sleep(30)

        except Exception as e:
            print(e)
            print("sleep for 10 sec")
            time.sleep(10)
    
if __name__ == '__main__':
    start()