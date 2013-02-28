Plan
====

Introduction
------------

At its core is a simple framework, which provides basic task management functions, necessary for maintaining lists of tasks, both those pending and those completed.  This core is then extended by plugins, which each represent a different productivity technique (such as the pomodorro technique).

Sitm will activate and deactive these plugins systematically in order to gather information as to the user's productivity using different techniques.  Over a period of time, sitm will build up a profile of which plugins are likely to be most effective in optimising the user's productivity.

Initially, sitm will only offer a simple command line interface, but in due course this could hopefully be extended to other domains.

It will be coded in python2.

Sub-commands
------------

- add: Adds a new task to the pending list
- done: Marks a task as done
- mod: Modify the attribute(s) of a task
- rm: Deletes a task
- ls: Lists tasks
- config: prints or sets configuration values
- plugins: Lists all plugins, with their status (activated/deactivated) and other information
- active: Activates specified plugin
- deactivate: Deactivates specified plugin
- report: Reports on your productivity for each period in which a different plugin was used

It is proposed to use the argparse library to implement the parsing of these sub-commands.

Classes
-------

- Tasklist: The list of all tasks (pending and complete)
- Task
- Plugin
- Record: A record showing the activation and deactivation of a certain plugin

Persistence
-----------

Each class which can be persisted should have a save() method and load(id) method for the purposes of persistence.

Data will be stored in a single sqlite file.  The attributes will be an arbitrary key/value list, so that plugins can store information on tasks without editing the database schema.

As well as the mandatory database fields, tasks will have a list of key/values so that plugins can store arbitrary information about them.

The database will have the following tables:

1. Tasks: task_id (autonumber), added (dt), done (dt), text (str)
2. TaskAttributes: task_id (int), key (str), value (str)
3. Config: key (str), value (str)
4. Records: plugin_name (str), activated (dt), deactivated (dt)

Plugins
-------

Plugins will each extend the Plugin class, and may implement the following methods:

- on_activate(): Code to run when the plugin is activated
- on_deactivate(): Code to run when the plugin is deactivated
- on_first(): This function is run on every active plugin everytime the program is run, before anything else is done.
- on_last(): This function is run on every active plugin, after everything else is done.
- on_add(task): After a task is added, this function is called for every active plugin with the task_id of the added task.  It returns a dictionary where the keys represent the names of task attributes and the values the text to prompt the user with.  This allows plugins to require the user to enter further information about new tasks when they are added.
- on_done(task): After a task is marked done, this function is called.  It returns a dictionary where the keys represent attributes and the values text to prompt the user with.
- on_rm(task): After a task is deleted, this function is called.
- on_mod(task, key): After a task is modified, this function is called
- on_ls(tasks): Tasks is a dictionary with task_id's as keys and weights.  This dictionary is passed between each active plugins ls functions, which modify the weights and may remove tasks.  The main ls command will then print the tasks with the lightest at the top and the heaviest at the bottom.
- on_custom_command(name, args): This exposes a new sub-command with the specified name, which will run this function when called with a list of arguments.
- on_notify(message): Code to run when notify is called
- on_plugin(plugin): Returns a string to be printed about the plugin when the plugins command is run
- on_report(record): Returns a string to be printed about each period when the report command is run

Self-Improvement
----------------

This is the tough part.  Let me have your ideas folks.  The specification above would simply allow the user to manually decide which plugins to activate and deactivate.

Measuring productivity could be done by considering the rate of task completion (average number of completed tasks per hour).  Alternatively, sitm could randomly ask the user to rate their own producvitiy on a scale of 0-5 and then average this result of a period in order to rate producivity.

Each plugin could be initially considered to have a 50% chance of improving productivity.  Bayes could then be used once the plugin was activated in order to re-assess this estimate.  The longer the plugin was active for, the more confident sitm could be as to whether or not the plugin made a difference.

Sitm would need to strike a balance between the using the plugins which had proved themselves effective, but also experiments with new plugins.  Perhaps this could be dealt with by some configuration variables, indicating whether the user wanted sitm to be conservative or explorative in activating new plugins.

Potential Future Features
-------------------------

- Anonymous collection of data to allow community review of plugin effectiveness
- Affinity analysis between users for plugin recommendations