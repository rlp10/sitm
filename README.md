Sitm
====

Sitm is the Self-Improving Task Manager.

As well as acting as a task management program, it also helps you to adopt strategies to increase your productivity.  The program does this by offering a number of plugins which can be enabled or disabled.

Status
------

Currently a basic command line task management system has been written, along with the plugin framework.

Usage
-----

```bash
$ sitm add "do something cool" # add a task

$ sitm next # prints the next task
do something cool 

$ sitm ls # lists all pending tasks, with id number
0   do something cool

$ sitm do # marks next task as done

$ sitm do --id 11 # marks task with id 11 as done

$ sitm log "eat breakfast" # same as adding then doing the task

$ sitm rm # removes next task

$ sitm plugins # lists plugins
...

$ sitm enable test # enables plugin called test

$ sitm disable test # disables plugin called test

sitm -h # show all subcommands
...
```

Data
----

All data is stored in a file called .sitm.dat in the user's home directory.

Aliases
-------

A file called aliases is included which can be sourced in your shell.
