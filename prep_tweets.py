# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
from tqdm.notebook import trange, tqdm

# %%
from minet.twitter import TwitterAPIScraper
scraper = TwitterAPIScraper()

# %%
accounts = [
    'lemondefr',
    'mediapart',
    'mediapartblogs'
]

since = '2022-01-01'

# %%
dfs = {}

for account in accounts:
    tweets = list(scraper.search_tweets(f'from:@{account} since:{since}'))
    dfs[account] = pd.DataFrame.from_records(tweets)

# %%
for account, tweets in dfs.items():
    tweets.to_parquet(f'datasets/{account}.par', index=False)
    tweets.to_csv(f'datasets/{account}.csv', index=False)

# %%
tweets = (
    pd
    .concat(list(dfs.values()))
    .set_index('id')
    .assign(
        local_time=lambda d: pd.to_datetime(d.local_time)
    )
)

tweets

# %%
tweets.to_parquet('datasets/tweets.par')
tweets.to_csv('datasets/tweets.csv')

# %%
