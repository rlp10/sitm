#!/usr/bin/env python2

@subcommand
def pomwork(data):
    '''Begin a pomodoro work block'''
    data = first(data, "begin timer for 25 minutes work - run pomrest when completed")
    return data

@subcommand
def pomrest(data):
    '''Begin a pomodorro rest block'''
    data = first(data, 'begin timer for 5 minutes rest - run pomwork when completed')
    return data

@subcommand
def pomreview(data):
    '''Reviews pomodoro blocks'''
    for task in data['done']:
        if 'begin timer for 25 minutes' in task['name']:
            print('work block began: {}'.format(task['done']))
        if 'begin timer for 5 minutes rest' in task['name']:
            print('rest block began: {}'.format(task['done']))
