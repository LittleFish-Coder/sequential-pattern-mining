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

        transactions = defaultdict(list)
        for i in range(0, len(seq), 2):
            tid = seq[i]
            item = seq[i + 1]
            transactions[tid].append(item)
        # make each itemsets in transaction.values() into tuple
        for tid, itemsets in transactions.items():
            transactions[tid] = tuple(itemsets)
        sequences[seq_id] = list(transactions.values())

    # print(sequences)  # {'sid': [ itemsets, itemsets, ...], }
    return sequences


def PrefixSpan(sequences, prefix, min_sup):
    # Find frequent items for the given prefix
    freq_items = find_frequent_items(sequences, min_sup)

    # output the frequent items
    for item, count in freq_items.items():
        yield (item,), count

    # for each frequent item, extend the prefix and project the sequences
    for item, count in freq_items.items():
        new_prefix = prefix + (item,)
        new_sequences = projected_database(sequences, new_prefix)

        # if the projected database is not empty, recursively call PrefixSpan
        if new_sequences:
            for projected_sequence, projected_count in PrefixSpan(
                new_sequences, new_prefix, min_sup
            ):
                yield projected_sequence + (item,), projected_count

    return None


def projected_database(sequences, prefix):
    projected_sequences = {}
    for sid, sequence in sequences.items():
        projected_sequence = []
        for itemset in sequence:
            projected_itemset = []
            for i in range(len(itemset)):
                if itemset[i] == prefix[0]:
                    projected_itemset = itemset[i + 1 :]
                    break
            if projected_itemset:
                projected_sequence.append(projected_itemset)
        if projected_sequence:
            projected_sequences[sid] = projected_sequence

    return projected_sequences


def find_frequent_items(sequences, min_sup):
    item_counts = defaultdict(int)
    for sid, sequence in sequences.items():
        curr_sequence_itemset = set()
        for itemset in sequence:
            for item in itemset:
                curr_sequence_itemset.add(item)
        for item in curr_sequence_itemset:
            item_counts[item] += 1

    # Find the frequent items
    frequent_items = {item: count for item, count in item_counts.items() if count >= min_sup}

    return frequent_items


def output_results(results, min_sup, output_path="output.txt"):

    with open(output_path, "w") as f:
        f.write(f"min_sup: {min_sup}\n")
        for itemset, count in results:
            f.write(f"{itemset} SUP: {count}\n")
            print(f"{itemset} SUP: {count}")


# Output Format: (given min_sup = 187)
# `9126 -1 7088 9126 -1 SUP: 187
# The numbers are the items.
# In this example, -1 is used to distinguish the different time pattern in a sequence.
# You can use any symbol like (), ||, to replace it.

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Apriori Algorithm")
    parser.add_argument("--input", type=str, default="seqdata.data.txt", help="input file name")
    parser.add_argument("--min_sup", type=int, default=187, help="input min_sup")
    parser.add_argument("--output", type=str, default="output.txt", help="output file name")
    args = parser.parse_args()

    # get the input file, min_supp and output_path
    input_file = args.input
    min_sup = args.min_sup
    output_path = args.output
    print(f"input file: {input_file}")
    print(f"min_sup: {min_sup}")

    sequences = generate_sequences("seqdata.dat.txt")
    # print(f"len of sequences: {len(sequences)}")

    ##### start time #####
    start = time.time()
    sequential_pattern = list(PrefixSpan(sequences, tuple(), min_sup))
    end = time.time()
    ##### end time #####

    print(f"Time: {end - start} seconds")
    # print(f"sequential_pattern: {sequential_pattern}")
    output_results(sequential_pattern, min_sup)
