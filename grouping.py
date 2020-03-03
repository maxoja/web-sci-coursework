import api_mongo as mongo

def popular_users(statuses):
    pass

def popular_tags(statuses):
    pass

def popular_entities(statuses):
    pass

if __name__ == '__main__':
    db = mongo.connect_to_db()
    polarity_exists = {'polarity':{'$exists':True}}

    negative_statuses = db.statuses.find( {'$and':[polarity_exists,{'polarity':{'$lte':-0.2}}]})
    negative_statuses = list(negative_statuses)

    neutral_statuses = db.statuses.find({'$and':[polarity_exists, {'polarity':{'$gt':-0.2}},{'polarity':{'$lt':0.2}}]})
    neutral_statuses = list(neutral_statuses)

    positive_statuses = db.statuses.find({'$and':[polarity_exists,{'polarity':{'$gte':0.2}}]})
    positive_statuses = list(positive_statuses)

    total = len(negative_statuses) + len(neutral_statuses) + len(positive_statuses)
    print(f'from all {db.statuses.count()} documents in statuses collection')
    print(f'there are {total} with their polarities analysed')
    print(f'there are {len(negative_statuses)} negative (less than -0.2) statuses')
    print(f'there are {len(neutral_statuses)} neutral (between -0.2 and 0.2) statuses')
    print(f'there are {len(positive_statuses)} positive (more than 0.2) statuses')