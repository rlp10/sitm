#!/usr/bin/env python2

@subcommand
def addreward(data, name):
    '''Adds a reward to the list of rewards'''
    if not 'rewards' in data.keys():
        data['rewards'] = []
    data['rewards'].append(name)
    return data

@subcommand
def rewards(data):
    '''Lists all rewards'''
    map(lambda tup: print("{}\t{}".format(*tup)), enumerate(data['rewards']))

@subcommand
def rmreward(data, id):
    '''Removes specified reward'''
    id = int(id)
    del data['rewards'][id]
    return data

@do_hook
def add_reward(data, task):
    '''Adds a reward as the top task half the time'''
    if " (random)" in task['name']:
        return data # do nothing if it's a reward already
    if random.choice([True, False]):
        reward = random.choice(data['rewards'])
        data = first(data, reward + " (reward)")
    return data
