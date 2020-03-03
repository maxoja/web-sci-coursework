# topics = ["coronavirys", "wuhan", "valentinewithnobody", "valentinesday2020"]
all_topics = []
chosen_topics = ['corona virus','stock price', 'sonic movie', 'brexit']

rest_query = '''corona virus OR wuhan OR #valentineswithnobody OR #valentinesday2020'''
#boundingbox.klokantech.com
# locations = [-85.97616108,36.9451024072,-85.8496475238,37.05198895]
worldwide_locations = [-180,-90,180,90]


[
    'created_at',
    'id',
    'id_str',
    'text',
    'source',
    'truncated',
    'in_reply_to_status_id',
    'in_reply_to_status_id_str',
    'in_reply_to_user_id',
    'in_reply_to_user_id_str',
    'in_reply_to_screen_name',
    'user',
    'geo',
    'coordinates',
    'place',
    'contributors',
    'is_quote_status',
    'quote_count',
    'reply_count',
    'retweet_count',
    'favorite_count',
    'entities',
    'favorited',
    'retweeted',
    'filter_level',
    'lang',
    'timestamp_ms'
]