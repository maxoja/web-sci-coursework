import pickle
import nltk
import networkx as nx
import matplotlib.pyplot as plt

# A (Users occuring together)
# links of mentions
def mention_links(group, group_name='default'):
    result = {}

    for status in group:
        # owner = status['user']['name']
        owner = status['user']['id']
        # mentioned_users = list(map(lambda x:x['name'],status['entities']['user_mentions']))
        mentioned_users = list(map(lambda x:x['id'],status['entities']['user_mentions']))
        for user in mentioned_users:
            if not owner in result:
                result[owner] = [u for u in mentioned_users]
            else:
                result[owner] += mentioned_users

    for user in result:
        result[user] = nltk.FreqDist(result[user]).most_common()

    return result

# links of retweet
def retweet_links(group, group_name='default'):
    result = {}

    for status in group:
        owner = status['user']['id']
        
        if not 'retweeted_status' in status:
            continue

        if not owner in result:
            result[owner] = [status['retweeted_status']['user']['id']]
        else:
            result[owner].append(status['retweeted_status']['user']['id'])

    for user in result:
        result[user] = nltk.FreqDist(result[user]).most_common()

    return result

# links of reply
# this will be left unimplemented since {'reply_count':{$gt:0}} returns no document

# B
# hashtag ocurring together
def hashtag_occuring_together(group, group_name='default'):
    result = {}

    for status in group:
        # owner = status['user']['name']
        # mentioned_users = list(map(lambda x:x['name'],status['entities']['user_mentions']))
        hashtags = list(map(lambda x:x['text'],status['entities']['hashtags']))
        for hashtag in hashtags:
            if not hashtag in result:
                result[hashtag] = set(hashtags)
            else:
                result[hashtag].update(hashtags)

    for hashtag in result:
        result[hashtag].remove(hashtag)

    return result

# print(mention_links(groups[0]))
# print(hashtag_occuring_together(groups[0]))
# print(retweet_links(groups[0]))

import api_mongo as mongo
db = mongo.connect_to_db()
num_groups = db.get_collection('meta').find_one()['clusters']
print(num_groups)

for k in range(num_groups+1):
    if k == num_groups: # all statuses
        continue

    group = list(db.get_collection(f'group_{k}').find())

# for k,group in groups.items():
    print(f'group {k}')
    mention_interaction = mention_links(group, str(k))
    #there will be no retweet links
    hashtag_together = hashtag_occuring_together(group, str(k))

    print('mention links')
    G = nx.Graph()
    for user in mention_interaction:
        G.add_node(user)
    
    for user in mention_interaction:
        for mentioned_user in mention_interaction[user]:
            G.add_edge(user,mentioned_user[1], weight=mentioned_user[0], width=mentioned_user[0])

    pos = nx.spring_layout(G,scale=1,k=0.5)
    nx.draw_networkx(G,with_labels = False, node_size = 10)
    plt.show()


    print('hashtag occuring together')
    G = nx.Graph()
    for tag in hashtag_together:
        G.add_node(tag)
    
    for tag in hashtag_together:
        for co_tag in hashtag_together[tag]:
            G.add_edge(tag,co_tag, weight=5, width=5)

    pos = nx.spring_layout(G,scale=1,k=0.5)

    # nx.draw(G,pos,font_size=8)
    nx.draw_networkx(G,with_labels = False, node_size = 10)
    plt.show()
    break


