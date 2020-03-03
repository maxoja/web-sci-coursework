import api_mongo as mongo
import pickle
import nltk
import networkx as nx
import matplotlib.pyplot as plt
import random
from networkx.generators.triads import triad_graph
from networkx.algorithms.triads import triadic_census

MAX_GROUP_SIZE = 3000
# MAX_GROUP_SIZE = 1000000
SHOW_PROGRESS = False

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

def gen_type1_graph(links):
    G = nx.DiGraph()
    for user in links:
        G.add_node(user)
    
    for i,user in enumerate(links):
        if SHOW_PROGRESS: print('progress', i, len(links.keys()))
        for mentioned_user in links[user]:
            G.add_edge(user,mentioned_user[1], weight=mentioned_user[0])
    return G

def gen_type2_graph(links):
    G = nx.Graph()
    for tag in links:
        G.add_node(tag)
    
    for tag in links:
        for co_tag in links[tag]:
            G.add_edge(tag,co_tag, weight=5)
    return G

def draw_type1_graph(links, name):
    G = gen_type1_graph(links)
    print(f'plotting {name} graph')
    print(f'with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges')
    draw(G)

def draw_type2_graph(links, name):
    G = gen_type2_graph(links)
    print('plotting',name,'graph')
    print(f'with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges')
    draw(G)

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
def retweet_links(group):
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
def reply_links(group):
    result = {}

    group = group_sampling(group)

    for status in group:
        owner = status['user']['id']
        replied_user = status['in_reply_to_user_id']

        if replied_user is None or replied_user == 'null':
            continue

        if not owner in result:
            result[owner] = [replied_user]
        else:
            result[owner].append(replied_user)

    for user in result:
        result[user] = nltk.FreqDist(result[user]).most_common()

    return result

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

if __name__ == "__main__":    
    db = mongo.connect_to_db()
    num_groups = db.get_collection('meta').find_one()['clusters']
    print(num_groups)

    for k in range(num_groups+1):
        if k == num_groups: # all statuses
            print('loadin all statuses from DB ...')
            group = list(db.statuses.find())

            print(f'group {k} of size {len(group)}')
            mention_interaction = mention_links(group)
            G = gen_type1_graph(mention_interaction)
            print('counting mention triads')
            print(triadic_census(G))
            # draw_type1_graph(mention_interaction,str(k)+'-mention')

            reply_interaction = reply_links(group)
            G = gen_type1_graph(reply_interaction)
            print('counting reply triads')
            print(triadic_census(G))
            # draw_type1_graph(reply_links, str(k)+'-reply')
            
            hashtag_together = hashtag_occuring_together(group)
            # draw_type2_graph(hashtag_together, str(k)+'-hashtag')

            retweet_interaction = retweet_links(group)
            G = gen_type1_graph(retweet_interaction)
            print('counting retweet triads')
            print(triadic_census(G))
            # draw_type1_graph(retweet_interaction, str(k)+'-retweet')
        else:
            print(f'loading group {k} statuses from DB ...')
            group = list(db.get_collection(f'group_{k}').find())

            print(f'group {k} of size {len(group)}')
            mention_interaction = mention_links(group)
            G = gen_type1_graph(mention_interaction)
            print('counting mention triads')
            print(triadic_census(G))
            # draw_type1_graph(mention_interaction,str(k)+'-mention')

            reply_interaction = reply_links(group)
            G = gen_type1_graph(reply_interaction)
            print('counting reply triads')
            print(triadic_census(G))
            # draw_type1_graph(reply_interaction, str(k)+'-reply')
            
            hashtag_together = hashtag_occuring_together(group)
            # draw_type2_graph(hashtag_together, str(k)+'-hashtag')

