#!/usr/bin/env python2

from __future__ import print_function

import argparse
import collections
import datetime
import dateutil.parser
import glob
import inspect
import os
import pdb
import pickle

# Tasklist - a dict of data to be persisted to disk
# There are two tasklists, pending and done

def data_save(tasklist, filename):
    '''Pickles and writes data to the disk'''
    pickle.dump(tasklist, open(filename, "w"))

def data_load(filename):
    '''Returns data from the disk or initialises'''
    try:
        return pickle.load(open(filename, "r"))
    except:
        return { 'pending': [], 'done': [], 'enabled': [] }

# Task - a dict

def task_get_next_id(data):
    '''Returns id of next task'''
    return 0

def task_print(task):
    '''Prints the name of the task'''
    print(task['name'])

def task_print_indexed(tasklist, task):
    '''Prints the index of the task along with its name'''
    index = tasklist.index(task)
    print("{}\t{}".format(index, task['name']))

# Commands 

def get_plugins():
    '''Returns list of plugins'''
    plugins = glob.glob("./plugins/*.py")
    plugins = map(lambda name: name.partition("plugins/")[2], plugins)
    plugins = map(lambda name: name.partition(".py")[0], plugins)
    return plugins

def int_or_next(data, id):
    '''Returns int of input or next task if none'''
    if id==None:
        return task_get_next_id(data)
    else:
        return int(id)

def subcommand(func):
    '''Decorator for subcommands which produces command line parser'''
    if not hasattr(subcommand, 'parser'):
        subcommand.parser = argparse.ArgumentParser(prog='sitm')
        subcommand.subparsers = subcommand.parser.add_subparsers(help='sub-commands')
    subparser = subcommand.subparsers.add_parser(func.__name__, help=func.__doc__)
    args, _, _, defaults = inspect.getargspec(func)
    try:
        len_defaults = len(defaults)
    except:
        len_defaults = 0
    compulsory = args[:len(args)-len_defaults]
    optional = args[len(args)-len_defaults:]
    if 'data' in compulsory:
        compulsory.remove('data')
    for arg in compulsory:
        subparser.add_argument(arg)
    for arg in optional:
        arg = "--" + arg
        subparser.add_argument(arg, default=None)
    subparser.set_defaults(func=lambda args:func(**args))
    return func

@subcommand
def add(data, name):
    '''Adds a new uncompleted task to the database'''
    task = {
            'name': name,
            'added': datetime.datetime.now()
           }
    data['pending'].append(task)
    return data

@subcommand
def cat(data, id=None):
    '''Prints full information for task'''
    id = int_or_next(data, id)
    for key, value in data['pending'][id].iteritems():
        print("{}\t{}".format(key, str(value)))

@subcommand
def disable(data, name):
    '''Disables specified plugin'''
    if name in data['enabled']:
        data['enabled'].remove(name)
        return data
    else:
        print("Plugin doesn't exist or is not enabled")

@subcommand
def do(data, id=None):
    '''Marks next task as completed'''
    id = int_or_next(data, id)
    task = data['pending'][id]
    del data['pending'][id]
    task['done'] = datetime.datetime.now()
    data['done'].append(task)
    return data

@subcommand
def enable(data, name):
    '''Enables specified plugin'''
    if name in get_plugins():
        data['enabled'].append(name)
    else:
        print("Plugin doesn't exist")
    return data

@subcommand
def log(data, name):
    '''Logs a completed task to the database'''
    task = { 'name': name,
             'added': datetime.datetime.now(),
             'done': datetime.datetime.now() }
    data['done'].append(task)
    return data

@subcommand
def ls(data):
    '''Prints list of all pending tasks'''
    for index, task in enumerate(data['pending']):
        print("{}\t{}".format(index, task['name']))

@subcommand
def next(data):
    '''Prints next task's name'''
    id = int_or_next(data, None)
    print(data['pending'][id]['name'])

@subcommand
def plugins(data):
    '''Prints a list of all plugins'''
    for plugin in get_plugins():
        if plugin in data['enabled']:
            status = "enabled"
        else:
            status = "disabled"
        print("{}\t{}".format(status, plugin))

@subcommand
def rm(data, id=None):
    '''Removes the next task'''
    id = int_or_next(data, id)
    data['pending'].pop(id)
    return data

@subcommand
def search(data, term):
    '''Prints pending tasks that match the search term'''
    tasks = filter(lambda task: term in task['name'], data['pending'])
    for index, task in enumerate(tasks):
        print("{}\t{}".format(index, task['name']))
    
@subcommand
def set(data, key, value, id=None):
    '''Sets a value on a task'''
    id = int_or_next(data, id)
    data['pending'][id][key] = value
    return data

# Main #

def main():
    # load plugins
    filename = os.path.expanduser('~/.sitm.dat')
    data = data_load(filename)
    for plugin in data['enabled']:
        plugin_f = open("./plugins/" + plugin + ".py", "r")
        exec(plugin_f.read())

    args = vars(subcommand.parser.parse_args())
    func = args.pop('func')
    args['data'] = data
    data = func(args)
    if data:
        data_save(data, filename)

if __name__ == '__main__':
    main()
