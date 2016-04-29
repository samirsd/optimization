#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import sys

import time
start_time = time.time()
Item = namedtuple("Item", ['index', 'value', 'weight'])


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0

    weight = 0
    taken = [0] * len(items)

    # ks_vd = sorted(items, key=lambda items: items.value / items.weight, reverse=True)

    def dp_knapsack(items, capacity, weight, value):
        totval = 0
        table = [[0 for w in range(capacity + 1)] for j in range(len(items) + 1)]

        for j in range(1, len(items) + 1):
            item, weight, value = items[j - 1]
            for w in range(1, capacity + 1):
                if weight > w:
                    table[j][w] = table[j - 1][w]
                else:
                    table[j][w] = max(table[j - 1][w],
                                      table[j - 1][w - weight] + value)

        result = []
        w = capacity
        for j in range(len(items), 0, -1):

            was_added = table[j][w] != table[j - 1][w]

            if was_added:
                taken[items[j - 1].index] = 1
                item, weight, value = items[j - 1]
                result.append(items[j - 1])
                w -= weight
            totval += value
        print(str(totval) + ' ' + str(0) + '\n')
        return result

    dp_knapsack(items, capacity, weight, value)

    #
    # for item in items:
    #     if len(items) is 0:
    #         return 0
    #     else:
    #         if weight + item.weight <= capacity:
    #             taken[item.index] = 1
    #             value += item.value
    #             weight += item.weight


    # # prepare the solution in the specified output format
    # output_data = str(value) + ' ' + str(0) + '\n'
    # output_data += ' '.join(map(str, taken))
    # return output_data


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()

        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print(solve_it(input_data))

    else:
        print('This test requires an input file.  Please select one from '
              'the data directory. (i.e. python solver.py ./data/ks_4_0)')

    print("--- %s seconds ---" % (time.time() - start_time))






# ks_vd = sorted(items, key=lambda items: items.value/items.weight, reverse=False)
