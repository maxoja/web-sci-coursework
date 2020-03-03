from pymongo import MongoClient, ASCENDING
from random import randint, shuffle
import json
import tweepy
from credentials import *

def insert_unique_status(db, status:tweepy.models.Status):
    status_dict = status._json
    db['statuses'].create_index([('id', ASCENDING)],unique=True)
    try:
        insert_doc(db, 'statuses', status_dict)
        print("inserted status with id", status.id)
    except Exception as e:
        print('insert_unique_status() catch error')
        print(e)

def insert_unique_user(db, user:tweepy.models.User):
    user_dict = user._json
    db['users'].create_index([('id', ASCENDING)],unique=True)
    try:
        insert_doc(db, 'users', user_dict)
        print("inserted user with id", user.id)
    except Exception as e:
        print('insert_unique_user() catch error')
        print(e)

def insert_replace_unique_group(db, i, group_statuses):
    doc_dict = {'id':i,'statuses':group_statuses}
    collection_name = 'group_'+str(i)
    try:
        db.drop_collection(collection_name)
        for j,s in enumerate(group_statuses):
            insert_doc(db, collection_name, s)
            if (j+1)%5000 == 0:
                print(f'progress:{(j+1)/len(group_statuses):.02f}')
        print("created and inserted statuses to collection",collection_name)
    except Exception as e:        
        print('error')
        print(e)

def insert_doc(db, collection:str, doc):
    db[collection].insert_one(doc)


def connect_to_db():
    url = mongo_url
    client = MongoClient(url)
    db = client.get_database(mongo_db_name)
    db.reviews.create_index([('rating', ASCENDING)],unique=True)
    return db

if __name__ == '__main__':
    #test if everything works
    db = connect_to_db()

    names = ['Kitchen','Animal','State', 'Tastey', 'Big','City','Fish', 'Pizza','Goat', 'Salty','Sandwich','Lazy', 'Fun']
    company_type = ['LLC','Inc','Company','Corporation']
    company_cuisine = ['Pizza', 'Bar Food', 'Fast Food', 'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']
    
    for x in range(1, 501):
        shuffle(names)
        shuffle(company_type)
        shuffle(company_cuisine)

        business = {
            'name' : names[0]  + ' ' + company_type[0],
            'rating' : randint(1, 5),
            'cuisine' : company_cuisine[0] 
        }

        try:
            result=db.reviews.insert_one(business)
            print(f'Created {x} of 500 as {result.inserted_id}')
        except:
            pass

    print('finished creating 500 business reviews')