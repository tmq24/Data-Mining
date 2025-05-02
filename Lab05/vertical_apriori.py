from operator import itemgetter
from tabnanny import verbose
import numpy as np
import pandas as pd
from pyECLAT import ECLAT

df = pd.read_csv('data.csv', header=None)
print('Dataframe:')
print(df)


eclat_instance = ECLAT(data=df, verbose=True)
print('ECLAT Instance:')
print(eclat_instance.df_bin)

items_per_transaction = eclat_instance.df_bin.astype(int).sum(axis=1)
min_support = 0.6  
min_combination = 2  
max_combination = max(items_per_transaction) 
rule_indices, rule_supports = eclat_instance.fit(min_support=min_support,
                                               min_combination=min_combination,
                                               max_combination=max_combination,
                                               separator=' & ',
                                               verbose=True)

result = pd.DataFrame(rule_supports.items(), columns=['Item', 'Support'])
result = result.sort_values(by=['Support'], ascending=False)
print(result)