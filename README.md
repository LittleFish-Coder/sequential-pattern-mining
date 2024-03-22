# Data Mining & Social Network Analysis Assignment 2

To run the program, see the [Usage](#Usage) section at the end of the document.

## Introduction

In this assignment, I use **PrefixSpan** to find frequent sequential pattern given by minimum support. The dataset contains **20000** sequences and **3092** different items. The program also prints the time taken to find the frequent sequential pattern.

## PrefixSpan Algorithm

The PrefixSpan algorithm is a popular sequential pattern mining algorithm used for finding frequent sequential patterns in a given dataset of sequences. It follows a divide-and-conquer approach by recursively projecting the database and growing the frequent prefixes.

- **Step 1.** Find frequent 1-itemsets: Find the frequent 1-itemsets (items) in the database based on the given minimum support threshold.
- **Step 2.** Generate projected databases: For each frequent 1-itemset, construct a projected database by extracting the suffixes (or prefixes) of sequences that contain the frequent item.
- **Step 3.** Recursive mining: Recursively mine the projected databases to find frequent patterns by growing the prefixes with frequent items.
- **Step 4.** Merge results: Merge the frequent sequences found in each projected database to obtain the final set of frequent sequences.

## Final Output Format

Given the min*sup, the program writes the output to the `output*{min_sup}.txt` file.

In the `output.txt` file, each line contains a frequent sequential pattern:

`{item1, item2, ...} (support)`

## Time Execution Comparison

| Minimum Support | Time Taken | # of Frequent Sequential Pattern |
| --------------- | ---------- | -------------------------------- |
| 100             | 2.21s      | 148                              |
| 187             | 0.21s      | 14                               |

## Usage

clone the repository and run the following command in the terminal:

```bash
git clone https://github.com/LittleFish-Coder/sequential-pattern-mining.git
```

```bash
cd sequential-pattern-mining
```

```bash
python nm6121030.py
```

add arguments to the command line to change the default values of the program.

- `--input` to change the input file (default: seqdata.data.txt)
- `--min_sup` to change the minimum support (default: 187)

### Example

```bash
python nm6121030.py --input seqdata.data.txt --min_supp 187
```
