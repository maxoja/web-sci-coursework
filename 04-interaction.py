import api_mongo as mongo
import pickle
import nltk
import networkx as nx
import matplotlib.pyplot as plt
import random

MAX_GROUP_SIZE = 2000

def group_sampling(group):
    if len(group) > MAX_GROUP_SIZE:
        group = group.copy()
        random.shuffle(group)
        group = group[:MAX_GROUP_SIZE]

    return group

def draw(G):
    # pos = nx.spring_layout(G,scale=1,k=0.5)
    # nx.draw_networkx(G,with_labels = False, node_size = 10)
    nx.draw(G,with_labels=True, node_size=5, font_size=0)
    plt.show()

# A (Users occuring together)
# links of mentions
def mention_links(group):
    result = {}
    
    group = group_sampling(group)

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

    group = group_sampling(group)

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
def hashtag_occuring_together(group):
    result = {}
    
    group = group_sampling(group)

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

def draw_mention_graph(i, group):
    mention_interaction = mention_links(group)
    G = nx.Graph()
    for user in mention_interaction:
        G.add_node(user)
    
    for i,user in enumerate(mention_interaction):
        print('progress', i, len(mention_interaction.keys()))
        for mentioned_user in mention_interaction[user]:
            G.add_edge(user,mentioned_user[1], weight=mentioned_user[0])

    print('ploting mention graph')
    print(f'with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges')
    draw(G)

def draw_hash_tag_graph(i, group):
    hashtag_together = hashtag_occuring_together(group)
    G = nx.Graph()
    for tag in hashtag_together:
        G.add_node(tag)
    
    for tag in hashtag_together:
        for co_tag in hashtag_together[tag]:
            G.add_edge(tag,co_tag, weight=5)

    print('plotting hashtag graph')
    print(f'with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges')
    draw(G)

def draw_retweet_graph(i, group):
    retweet_interaction = retweet_links(group)

    G = nx.Graph()

    for user in retweet_interaction:
        G.add_node(user)
    
    for i,user in enumerate(retweet_interaction):
        print('progress', i, len(retweet_interaction.keys()))
        for retweeted_users in retweet_interaction[user]:
            G.add_edge(user,retweeted_user[1], weight=retweeted_user[0])

    print('ploting retweet graph')
    print(f'with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges')
    draw(G)

db = mongo.connect_to_db()
num_groups = db.get_collection('meta').find_one()['clusters']
print(num_groups)

for k in range(num_groups+1)[:3]:
    if k == num_groups: # all statuses
        print('loadin all statuses from DB ...')
        group = list(db.statuses.find())
    else:
        print(f'loading group {k} statuses from DB ...')
        group = list(db.get_collection(f'group_{k}').find())

    print(f'group {k} of size {len(group)}')
    print(f'generating mention graph')
    draw_mention_graph(k, group)
    print(f'generating hashtag graph')
    draw_hash_tag_graph(k, group)  

