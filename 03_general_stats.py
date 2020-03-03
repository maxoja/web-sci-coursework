import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import api_mongo as mongo
import pickle
import nltk

db = mongo.connect_to_db()
print('collection loading')
all_statuses = list(db.get_collection('statuses').find())
print('collection loaded with size =', len(all_statuses))

if __name__ == '__main__':
    owners = []
    tags = []
    mentions = []
    for status in all_statuses:
        owners.append(status['user']['name'])
        tags += [ h['text'] for h in status['entities']['hashtags']]
        mentions += [ m['name'] for m in status['entities']['user_mentions']]

    top_owners = nltk.FreqDist(owners).most_common(5)
    top_tags = nltk.FreqDist(tags).most_common(5)
    top_mentions = nltk.FreqDist(mentions).most_common(5)

    out_str = f'[group all]'
    out_str += f'\nsize of {len(all_statuses)}'
    out_str += f'\nunique posters {len(set(owners))}'
    out_str += f'\nunique hashtags {len(set(tags))}'
    out_str += f'\nunique mentions {len(set(mentions))}'
    out_str += '\n\nimportant posters'
    for poster in top_owners:
        out_str += '\n' + str(poster)

    out_str += '\n\nimportant hashtags'
    for tag in top_tags:
        out_str += '\n' + str(tag)
    
    out_str += '\n\nimportant mentions'
    for mention in top_mentions:
        out_str += '\n' + str(mention)

    with open('group_all.txt','w',encoding='utf-8') as out:
        out.write(out_str)
