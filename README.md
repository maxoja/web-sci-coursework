# websci-coursework

## setup
- install dependencies `pip install -r requirements.txt` (virtual environment recommended but not necessary)
- import data collection from `data/*` directory into MongoDB
- set credential values in `credentials-template.py` and rename it to `credentials.py`

## run
- run scripts in the following order (crawling scripts can be skipped)
- `python 1_1_crawl_stream.py <TIME_MINUTE>` - crawl using streaming API on topics/location specified in `config.py`. you can specify how much time you want it to run
- `python 1_2_crawl_rest_user.py <TIME_MINUTE>` - crawl using REST API on top of user analysis result of data from the first script in MongoDB. you can specify running period. this script is meant to be run parallely with the first script but not necessary.
- `python 2_1_grouping_and stats.py` - this script pulls all tweets data from MongoDB and cluster them. It will render k-mean's k value optimisation chart as well as pushing grouped tweets back to MongoDB collections. The statistics of each group will also be computed and save in text files in `report/stats/group_[id].txt`
- `python 2_2_general_stats.py` - run same statistics computation same as 2_1 script but on general data of all tweets and save to `report/stats/group_all.txt`
- `python 3to4_analysis.py` - run this script to perform network analysis. The result will be printed out but not saved to any file.

## Credit Reference
- [Python K-Mean clustering on text data](https://www.kaggle.com/jbencina/clustering-documents-with-tfidf-and-kmeans)