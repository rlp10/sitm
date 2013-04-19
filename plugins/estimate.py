#!/usr/bin/env python2

@add_hook
def estimate_time_to_completion(data, task):
    '''Prints an estimate of when the task will be completed'''
    # calculate minutes per task
    done = len(data['done'])
    now = datetime.datetime.now()
    earliest = min([task['added'] for task in data['done'] + data['pending']])
    difference = now - earliest
    diff_in_mins = difference.seconds / 60
    time_per_task = diff_in_mins / done
    
    # number of tasks before the one pending
    todo = len(data['pending'])
    estimated_time = time_per_task * todo
    time = now + datetime.timedelta(minutes=estimated_time)
    print('Estimated Completion Time: {}'.format(str(time)))
    return data
