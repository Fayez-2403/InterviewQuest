from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings

warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

import os
from bertopic import BERTopic
import pandas as pd
from time import time

start_time = time()

model_merged_ngram = BERTopic.load("../model_merged_ngram_no_len")
print("time to load: ", time()-start_time)

tp = model_merged_ngram.get_topic_info()
print("time to get topic list: ", time()-start_time)

# Split the 'Bucket' column by underscores and join the parts with commas
tp['Bucket'] = tp['Name'].str.split('_').str[1:].str.join(', ')
print("time to filter: ", time()-start_time)

data = {
    'Bucket Number': tp['Topic'],
    'Bucket': tp['Bucket']
}

df = pd.DataFrame.from_dict(data)

df.to_csv('net_bucket.csv', index=False)
print("time to make csv: ", time()-start_time)
