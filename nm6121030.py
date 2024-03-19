import argparse
from collections import defaultdict
import time


def generate_sequences(input_path="seqdata.dat.txt"):
    # read the input_path
    with open(input_path, "r") as f:
        lines = f.readlines()

    # generate the sequences table
    sequences = {}

    for line in lines:
        seq = line.split()
        seq_id = seq.pop(0)  # extract the sequence id

        transaction_table = {}

        for i in range(0, len(seq), 2):
            transaction_time = int(seq[i])
            item_id = int(seq[i + 1])

            if transaction_time in transaction_table:
                transaction_table[transaction_time].append(item_id)
            else:
                transaction_table[transaction_time] = [item_id]

        sequences[seq_id] = list(transaction_table.values())

        # print(sequences)  # {'1': [[166, 4103, 8715], [4103, 8715], [166, 3704, 6568, 8375, 8715], [166, 9406]]}

    return sequences


def PrefixSpan(sequences, min_support):
    frequent_items = find_frequent_items(sequences, min_support)
    # print(f"len of 1-item frequent_items after pruning: {len(frequent_items)}")

    frequent_patterns = []
    for item in frequent_items:
        projected_db = build_projected_database(sequences, [item])
        frequent_patterns.extend(prefix_span_mining(projected_db, [item], min_support))

    return frequent_patterns


def prefix_span_mining(projected_db, prefix, min_support):
    frequent_items = find_frequent_items(projected_db, min_support)

    # 步驟2: 對每個頻繁項目進行遞歸
    frequent_patterns = []
    for item in frequent_items:
        new_prefix = prefix + [item]
        projected_db = build_projected_database(projected_db, new_prefix)
        frequent_patterns.append(new_prefix)
        frequent_patterns.extend(prefix_span_mining(projected_db, new_prefix, min_support))

    return frequent_patterns


def find_frequent_items(sequences, min_support):
    item_counts = defaultdict(int)
    for sid, sequence in sequences.items():  # '103': [ [1,2,3], [3,2,1] ]
        itemset = set()
        for transaction in sequence:  # [1,2,3]
            itemset.update(transaction)
        for item in itemset:
            item_counts[item] += 1

    frequent_items = [item for item, count in item_counts.items() if count >= min_support]
    return frequent_items


def build_projected_database(sequences, prefix):
    projected_db = defaultdict(list)
    for sid, sequence in sequences.items():
        prefix_index = 0
        for transaction_index, transaction in enumerate(sequence):
            if prefix_index >= len(prefix):
                break
            if transaction[prefix_index : prefix_index + len(prefix)] == prefix:
                remaining_sequence = sequence[transaction_index + 1 :]
                projected_db[sid].extend(remaining_sequence)
                prefix_index = len(prefix)
    return projected_db


def output_results(results):
    pass


# Output Format: (given min_sup = 187)
# `9126 -1 7088 9126 -1 SUP: 187
# The numbers are the items.
# In this example, -1 is used to distinguish the different time pattern in a sequence.
# You can use any symbol like (), ||, to replace it.

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Apriori Algorithm")
    parser.add_argument("--input", type=str, default="seqdata.data.txt", help="input file name")
    parser.add_argument("--min_supp", type=int, default=200, help="input min_supp")
    args = parser.parse_args()

    # get the input file, min_supp and min_conf
    input_file = args.input
    min_supp = args.min_supp
    print(f"input file: {input_file}")
    print(f"min_supp: {min_supp}")

    sequences = generate_sequences("seqdata.dat.txt")

    ##### start time #####
    start = time.time()

    results = PrefixSpan(sequences, min_supp)

    end = time.time()
    ##### end time #####

    print(f"Time: {end - start} seconds")
    output_results(results)
