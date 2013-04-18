#!/usr/bin/env python2

@subcommand
def review(data):
    '''Prints a report of the user's productivity'''

    def count_done(data, date):
        '''Count tasks done on that day'''
        completed = [ task for task in data['done'] if task['done'].date() == date ]
        return len(completed)

    def count_new(data, date):
        new = [ task for task in data['done'] + data['pending'] if task['added'].date() == date ]
        return len(new)

    def difference(data, date):
        return count_new(data, date) - count_done(data, date)

    headers = [ 'date', 'new', 'done', 'diff' ]
    funcs = [ count_new, count_done, difference ]
    
    days = [ task['added'].date() for task in data['pending'] + data['done'] ]
    days = [ task['done'].date() for task in data['done'] ]
    days = __builtins__.set(days)

    for header in headers:
        print('{:12s}'.format(header), end='')
    print('')
    for day in days:
        print('{:12s}'.format(str(day)), end='')
        for func in funcs:
            print('{:12}'.format(str(func(data, day))), end='')
        print('')
