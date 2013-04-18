#!/usr/bin/env python2

@subcommand
def catcontext(data):
    print(data['config']['context'])

@subcommand
def context(data, context):
    '''Sets the current context'''
    data['config']['context'] = context
    return data

@subcommand
def contexts(data):
    '''Prints a list of all contexts in pending tasks'''
    cons = map(lambda task: task.get('context', None), data['pending'])
    cons = filter(lambda con: not con==None, cons)
    cons = __builtins__.set(cons)
    map(print, cons)

@pending_hook
def filter_by_context(data, tasks):
    '''Filter tasks based on current context'''
    con = data['config']['context']
    tasks = [task for task in tasks if task.get('context', con) == con]
    return tasks

