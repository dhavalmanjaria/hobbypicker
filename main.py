# Hobby picker
# Pick a few activities you want to do at a certain time. Ideally they should be activities
# you want to do every day. Assign weights to them based on 3 criteria, in this case time of day.
# This application will roll a die , add the weights will be added to the roll and a winner
# will be selected.

import csv
import argparse
import random

def debugger(is_debug):
    def debug(line, is_debug):
        if is_debug:
            print(line)
    return debug


def read_csv(filename):
    retval = []
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            retval.append(row)

    return retval

def filter_tasks(data, criterion):
    tasks = {}
    for item in data:
        tasks[item['Task']] = item[criterion]

    return tasks

def tie_breaker(rolls_tup):
    '''
    Break a tie by collecting all keys with the same value in a list,
    and returning 1 random value
    :param rolls:
    :return:
    '''
    existing_values = []
    tied_values = []
    for r in rolls_tup:
        k, v = r
        if v in existing_values:
            tied_values.append(k)
            # Do a backtrack search for all keys with this value
            tied_values += [r[0] for r in rolls_tup if r[1] == v]
        existing_values.append(v)

    # remove duplicates
    tied_values = list(set(tied_values))
    if tied_values:
        print(f'{tied_values=}')
        return tied_values[random.randint(0, len(tied_values) - 1)]


def roll_dice(die, tasks):
    rolls = []
    tasks_tup = [[k, v] for k, v in tasks.items()]
    for r in tasks_tup:
        k, v = r
        die_roll = random.randint(1, die + 1)
        print(f'task={k} value={v} {die_roll=} total={int(v) + die_roll}')
        rolls.append([k, int(v) + die_roll])
    print('---------')
    tie_winner = tie_breaker(rolls)
    if tie_winner:
        for r in rolls:
            k, v = r
            if k == tie_winner:
                print(f'{tie_winner=}')
                r[1] += 1
                break

    rolls = sorted(rolls, key=lambda t: t[1], reverse=True)
    print('--------------')
    for r in rolls:
        print(f'{r[0]:30}: {r[1]}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='hobbypicker')
    parser.add_argument("-r", '--read-file', help='the file to read', required=True)
    parser.add_argument("-c", '--criteria-column', help='the column to select weights from', required=True)
    parser.add_argument("-d", '--die', help='the die to use', required=True)
    opts = parser.parse_args()

    data = read_csv(opts.read_file)
    roll_dice(
        die=int(opts.die),
        tasks=filter_tasks(data, opts.criteria_column),
    )