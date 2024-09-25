#!/usr/bin/env python

"""Check if there are tasks which are overdue. If so, nag the user."""
import time
import traceback
import tkinter as tk
from datetime import datetime, timedelta

root = None

def set_last_run(tasks):
    """Update the last_run field for the tasks, if they ever have been run.
       Updates tasks in place."""
    with open('tasks.txt', 'r') as taskfile:
        lines = taskfile.read().split('\n')
        for line in lines:
            pieces = line.split('\t')
            if len(pieces) > 1:
                taskname = pieces[0]
                last_run = datetime.strptime(pieces[1], '%Y-%m-%d')
                tasks[taskname]['last_run'] = last_run
    pass

def save_last_run(tasks):
    """Store a record of when tasks were last run."""
    with open('tasks.txt', 'w') as taskfile:
        for taskname in tasks:
            task = tasks[taskname]
            if task.get('last_run'):
                taskfile.write('{}\t{}\n'.format(taskname, task['last_run'].strftime('%Y-%m-%d')))

def load_tasks():
    """Create a dictionary of tasks which need to be done.
       A task has a name, 
       a flag indicating calendar (true) or elapsed (false)
       elapsed has an interval in days
       calendar is monthly or anual (monthly true)
       and a date (ay of month or month/day)"""
    tasks = {}
    tasks['est1'] = {'cal':True, 'monthly':False, 'when':'4/12'}
    tasks['est2'] = {'cal':True, 'monthly':False, 'when':'6/12'}
    tasks['est3'] = {'cal':True, 'monthly':False, 'when':'9/12'}
    tasks['est4'] = {'cal':True, 'monthly':False, 'when':'1/12'}
    tasks['statements'] =  {'cal':True, 'monthly':True, 'when':'10'}
    tasks['draino'] = {'cal':False, 'elapsed':'60'}
    tasks['vacuum'] = {'cal':False, 'elapsed':'30'}
    return tasks

def schedule_tasks(tasks):
    """Go through list of tasks. Based on the rules and last_run, see if the task
       is overdue."""
    today = datetime.now()
    for taskname in tasks:
        try:
            task = tasks[taskname]
            if task.get('last_run') is None:
                task['overdue'] = True
                continue
            if task.get('cal'):
                if task.get('monthly'):
                    when = "{}-{}-{}".format(today.year, today.month, task['when'])
                else:
                    pieces = task['when'].split('/')
                    when = "{}-{}-{}".format(today.year, pieces[0], pieces[1])
                scheduled = datetime.strptime(when, "%Y-%m-%d")
                if scheduled > task['last_run']:
                    task['overdue'] = True
            else:
                scheduled = task['last_run'] + timedelta(days=int(task['elapsed']))
                if today > scheduled:
                    task['overdue'] = True
        except Exception:
            traceback.print_exc()

def mark_as_done(taskname, tasks):
    print("done with {}".format(taskname))
    tasks[taskname]['last_run'] = datetime.now()
    root.destroy()

def remind_later(taskname):
    print("remind later {}".format(taskname))
    root.destroy()


def show_modal(taskname, tasks):
    global root
    root = tk.Tk()
    root.title(taskname)
    #mark_task_done = lambda taskname: mark_as_done(taskname)
    #remind_task_later = lambda taskname: remind_later(taskname)
    done_button = tk.Button(root, text="Done", command=lambda : mark_as_done(taskname, tasks))
    done_button.pack(side=tk.LEFT, padx=100, pady=10)
    remind_button = tk.Button(root, text="Later", command=lambda : remind_later(taskname))
    remind_button.pack(side=tk.RIGHT, padx=100, pady=10)
    root.mainloop()

if __name__ == '__main__':
    #root = tk.Tk()
    #root.mainloop()
    while(True):
        tasks = load_tasks()
        set_last_run(tasks)
        schedule_tasks(tasks)
        for taskname in tasks:
            task = tasks[taskname]
            if task.get('overdue'): # not true is false :-)
                show_modal(taskname, tasks)
        save_last_run(tasks)
        print("done loop")
        time.sleep(3600 * 24)

