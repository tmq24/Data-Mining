import pandas as pd
from itertools import combinations

def load_data(filename):
    df = pd.read_csv(filename, header=None)
    transactions = []
    for i in range(df.shape[0]):
        transaction = [str(df.values[i, j]) for j in range(df.shape[1]) if pd.notna(df.values[i, j])]
        transactions.append(transaction)
    return transactions

def has_infrequent_subset(candidate, prev_frequent):
    k = len(candidate)
    for subset in combinations(candidate, k - 1):
        if frozenset(subset) not in prev_frequent:
            return True
    return False

def get_candidates(Lk_minus_1, k):
    candidates = set()
    Lk_minus_1 = list(Lk_minus_1)
    for i in range(len(Lk_minus_1)):
        for j in range(i+1, len(Lk_minus_1)):
            l1, l2 = sorted(Lk_minus_1[i]), sorted(Lk_minus_1[j])
            if l1[:k-2] == l2[:k-2]:
                candidate = frozenset(set(l1) | set(l2))
                if not has_infrequent_subset(candidate, Lk_minus_1):
                    candidates.add(candidate)
    return candidates

def apriori(transactions, min_sup=0.6):
    n = len(transactions)
    item_count = {}
    for t in transactions:
        for item in t:
            item_count[item] = item_count.get(item, 0) + 1
    L1 = set([frozenset([item]) for item, count in item_count.items() if count / n >= min_sup])
    L = [L1]
    support_data = {frozenset([item]): count / n for item, count in item_count.items()}

    k = 2
    while L[-1]:
        Ck = get_candidates(L[-1], k)
        item_count = {c: 0 for c in Ck}
        for t in transactions:
            t_set = set(t)
            for c in Ck:
                if c.issubset(t_set):
                    item_count[c] += 1
        Lk = set([c for c, count in item_count.items() if count / n >= min_sup])
        for c in Lk:
            support_data[c] = item_count[c] / n
        if Lk:
            L.append(Lk)
        k += 1
        if not Lk:
            break
    frequent_itemsets = set().union(*L)
    return frequent_itemsets, support_data

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
    min_conf = 0.6
    frequent_itemsets, support_data = apriori(transactions, min_sup)
    print("Frequent itemsets (min_sup=0.6):")
    for itemset in frequent_itemsets:
        print(list(itemset), ":", support_data[itemset])

    print("\nAssociation Rules (min_conf=0.6):")
    rules = generate_rules(frequent_itemsets, support_data, min_conf)
    for antecedent, consequent, support, confidence in rules:
        print(f"{antecedent} -> {consequent} (support={support:.2f}, confidence={confidence:.2f})")