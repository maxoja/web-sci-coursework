import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import api_mongo as mongo
import pickle
import nltk

from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

seed = 26
max_clusters = 50
best_k = 8

db = mongo.connect_to_db()
all_statuses = list(db.get_collection('statuses').find({'retweeted_status':{'$exists':False}}))
print('collection loading with size =', len(all_statuses))
# texts = [ s['text'] if 'text' in s else s['full_text'] for s in all_statuses if s['truncated'] == False and 'text' in s ]
# texts += [ s['full_text'] for s in all_statuses if s['truncated'] == False and not 'text' in s ]
# texts += [ s['extended_tweet']['full_text']  for s in all_statuses if s['truncated'] ]
texts = []
for s in all_statuses:
    if s['truncated']:
        texts.append(s['extended_tweet']['full_text'])
    else:
        if 'full_text' in s:
            texts.append(s['full_text'])
        else:
            texts.append(s['text'])

print(f'extract texts = {len(texts)}')
tfidf = TfidfVectorizer(
    min_df = 5,
    max_df = 0.95,
    max_features = 8000,
    stop_words = 'english'
)

tfidf.fit(texts)
vectors = tfidf.transform(texts)

def find_optimal_clusters(data, max_k):
    iters = range(2, max_k+1, 1)
    
    sse = []
    for k in iters:
        sse.append(MiniBatchKMeans(n_clusters=k, init_size=1024, batch_size=2048, random_state=seed).fit(data).inertia_)
        print('Fit {} clusters'.format(k))
        
    print('plotting kmean graph')
    f, ax = plt.subplots(1, 1)
    ax.plot(iters, sse, marker='o')
    ax.set_xlabel('Cluster Centers')
    ax.set_xticks(iters)
    ax.set_xticklabels(iters)
    ax.set_ylabel('SSE')
    ax.set_title('SSE by Cluster Center Plot')
    plt.show()

def plot_tsne_pca(data, labels):
    print('plotting clustering graph')
    max_label = max(labels)
    max_items = np.random.choice(range(data.shape[0]), size=3000, replace=False)
    
    pca = PCA(n_components=2).fit_transform(data[max_items,:].todense())
    tsne = TSNE().fit_transform(PCA(n_components=50).fit_transform(data[max_items,:].todense()))
    
    
    idx = np.random.choice(range(pca.shape[0]), size=300, replace=False)
    label_subset = labels[max_items]
    label_subset = [cm.get_cmap('hsv')(i/max_label) for i in label_subset[idx]]
    
    f, ax = plt.subplots(1, 2, figsize=(14, 6))
    
    ax[0].scatter(pca[idx, 0], pca[idx, 1], c=label_subset)
    ax[0].set_title('PCA Cluster Plot')
    
    ax[1].scatter(tsne[idx, 0], tsne[idx, 1], c=label_subset)
    ax[1].set_title('TSNE Cluster Plot')
    plt.show()
    
def get_top_keywords(data, model, labels, n_terms):
    for i in range(data.shape[0]):
        cluster = model.predict(data[i:i+1])
        print(f'{cluster} {texts[i][:50]}')
    # df = pd.DataFrame(data.todense()).groupby(clusters).mean()
    
    # for i,r in df.iterrows():
    #     print('\nCluster {}'.format(i))
    #     print(r)
    #     print(','.join([labels[t] for t in np.argsort(r)[-n_terms:]]))
            
if __name__ == '__main__':
    # print('max clusters =',max_clusters)
    # find_optimal_clusters(vectors,max_clusters)
    model = MiniBatchKMeans(n_clusters=best_k, init_size=1024, batch_size=2048, random_state=seed).fit(vectors)
    cluster_predict = model.predict(vectors)
    
    print('inserting/replacing groups to DB')
    packed = list(zip(cluster_predict, texts, all_statuses))

    n_clusters = best_k

    for i in range(n_clusters):
        group = list(filter(lambda x:x[0] == i, packed))
        group = list(map(lambda x: x[2],group))

        owners = []
        tags = []
        mentions = []
        for status in group:
            owners.append(status['user']['name'])
            tags += [ h['text'] for h in status['entities']['hashtags']]
            mentions += [ m['name'] for m in status['entities']['user_mentions']]

        top_owners = nltk.FreqDist(owners).most_common(5)
        top_tags = nltk.FreqDist(tags).most_common(5)
        top_mentions = nltk.FreqDist(mentions).most_common(5)

        out_str = f'[group {i}]'
        out_str += f'\nsize of {len(group)}'
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

        with open('report/stats/group_'+str(i)+'.txt','w',encoding='utf-8') as out:
            out.write(out_str)
            # print(out_str.encode("utf-8"))

        mongo.insert_replace_unique_group(db, i, group)

    db.get_collection('meta').insert({'clusters':n_clusters})
    
    # plot_tsne_pca(vectors, cluster_predict)
    # clusters = model.predict(vectors)
    # get_top_keywords(vectors, model, tfidf.get_feature_names(), 10)
