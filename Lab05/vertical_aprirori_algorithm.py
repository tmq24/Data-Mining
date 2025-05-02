import pandas as pd
from itertools import combinations
import math

def load_data(filename):
    df = pd.read_csv(filename, header=None)
    transactions = []
    for i in range(df.shape[0]):
        transaction = [str(df.values[i, j]) for j in range(df.shape[1]) if pd.notna(df.values[i, j])]
        transactions.append(transaction)
    return transactions

def custom_round(x):
    frac = x - int(x)
    if frac <= 0.5:
        return math.ceil(x)
    else:
        return round(x)

def vertical_apriori(transactions, min_sup=0.6):
    n = len(transactions)
    min_count = custom_round(min_sup * n)
    # Create TID-list for each item
    item_tid = {}
    for tid, transaction in enumerate(transactions):
        for item in transaction:
            item_tid.setdefault(item, set()).add(tid)
    # Filter 1-itemset with support
    L = [{frozenset([item]): tids for item, tids in item_tid.items() if len(tids) >= min_count}]
    support_data = {frozenset([item]): len(tids)/n for item, tids in item_tid.items() if len(tids) >= min_count}
    k = 2
    while L[-1]:
        prev_L = L[-1]
        candidates = {}
        prev_items = list(prev_L.keys())
        for i in range(len(prev_items)):
            for j in range(i+1, len(prev_items)):
                itemset1 = prev_items[i]
                itemset2 = prev_items[j]
                candidate = itemset1 | itemset2
                if len(candidate) != k:
                    continue
                # Intersection of TID-lists to create new candidate TID-list
                tids = prev_L[itemset1] & prev_L[itemset2]
                if len(tids) >= min_count:
                    candidates[candidate] = tids
        if not candidates:
            break
        # Save support of candidates that meet the condition
        for itemset, tids in candidates.items():
            support_data[itemset] = len(tids)/n
        L.append(candidates)
        k += 1
    # Combine all frequent itemsets
    all_freq = {}
    for level in L:
        all_freq.update(level)
    return all_freq, support_data

def generate_rules(frequent_itemsets, support_data, min_conf=0.6):
    rules = []
    for itemset in frequent_itemsets:
        if len(itemset) < 2:
            continue
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                if not consequent:
                    continue
                support = support_data[itemset]
                confidence = support_data[itemset] / support_data.get(antecedent, 1)
                if confidence >= min_conf:
                    rules.append((set(antecedent), set(consequent), support, confidence))
    return rules
    
if __name__ == "__main__":
    transactions = load_data("data.csv")
    min_sup = 0.6
    min_conf = 0.8
    freq_itemsets, support_data = vertical_apriori(transactions, min_sup)
    print("Frequent itemsets (vertical, min_sup=0.6):")
    for itemset, tids in freq_itemsets.items():
        print(list(itemset), "support:", support_data[itemset])

    print("\nAssociation Rules (min_conf=0.8):")
    rules = generate_rules(freq_itemsets, support_data, min_conf)
    for antecedent, consequent, support, confidence in rules:
        print(f"{antecedent} & {consequent} (support={support:.2f}, confidence={confidence:.2f})")