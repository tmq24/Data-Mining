import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

df = pd.read_csv('data.csv', header=None)
print('Dataframe:')
print(df)

records = []
for i in range(df.shape[0]):
    records.append([str(df.values[i, j]) for j in range(0, df.shape[1])])

te = TransactionEncoder()
te_ary = te.fit(records).transform(records)
df1 = pd.DataFrame(te_ary, columns=te.columns_)
print('Transaction dataframe:')
print(df1)

# Build Apriori model
frequent_itemsets = apriori(df1, min_support=0.6, use_colnames=True)
print('Frequent itemsets:')
print(frequent_itemsets)

# Build association rules using support metric
rules = association_rules(frequent_itemsets, metric="support", support_only=True, min_threshold=0.1)
rules = rules[['antecedents', 'consequents', 'support']]
print('Association rules:')
print(rules)