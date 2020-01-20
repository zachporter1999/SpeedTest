# SpeedTest
# this branch is not working. DO NOT USE

# how to setup
this branch uses windows task scheduler to schedule the testing and emailing jobs.

run setup.py to setup the tasks

usage: setup.py [-h] [-Enable] [-Disable] [-Delete] [-XML XML XML]

optional arguments:
  -h, --help    show this help message and exit
  -Enable       used to enable the task
  -Disable      used to disable the task
  -Delete       used to delete the task
  -XML XML XML  The XML 2 config file used to setup the task. -XML <speed test config> <email notification config>
  
scheduler config files are found in the config folder
