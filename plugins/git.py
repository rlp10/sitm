#!/usr/bin/env python2

@do_hook
def add_git_after_code(data, task):
    '''Adds a task about git after any command containing the word "code"'''
    if 'code' in task['name']:
        data = first(data, "consider git repo for recent changes")
    return data

