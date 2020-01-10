# SpeedTest

#######################
### Branch Overview ###
#######################

Branch             |   Description
-------------------|---------------------------------------------------------------------------------------
Jenkins_Based_v1.0 | - Uses jenkins automation server to schedule tasks. 
-------------------|---------------------------------------------------------------------------------------
Develop/v1.0       | - latest release under development. with use a python script to schedule task,                                                                           |   the email plot will be interpolated, and with give max, avg, and min speed readings


#########################
###   Jenkins Setup   ###
#########################

SPEED TEST setup
----------------

1. Download latest LTS version of jenkins from https://jenkins.io/download/

2. follow setup

3. once setup and looking at the jenkins dashboard click on new item near the top left.

4. select folder and name it Speed Test, click save.

5. new item from along the left side again.

6. select freestyle project and name it Execute speed test

7. Setup Speed test.
  a) select discard old builds under general in the config.
    i) set max # of builds to keep to 10
    
  b) select this project is paramaterized
    i) add string parameters:
      ia) Log_File with default value test.log
      
      ib) Threads with default value 0
      
  c) click advanced below the paramaters you just added
    i) select use custom workspace
    
    ii) for Directory enter the path to this repository. should have the python scripts in the directory
    
  d) for build triggers selct build periodically
    i) use the help icon to figure out how to set the period
    
    ii) eg of schedule that runs every 30 min: H/30 * * * *
    
  e) under build add build step "Execute windows batch command 
  
    i) %Python36_Path%\python.exe SpeedTester.py -Log %Log_file% -Threads %Threads%
    
    ii) %Python36_Path% is setup in jenkins global vars, alternatie to this is adding pthyon.exe to PATH env var
  
  f) click save
  
EMAIL setup

  6. select freestyle project and name it Send Email Notification

  7. Setup Speed test.
    a) select discard old builds under general in the config.
      i) set max # of builds to keep to 10

    b) select this project is paramaterized
      i) add string parameters:
        ia) Server with default value being what email you want to send the emails from (must be gmail)

        ib) Recipient_List with default value of the emails you want to receive the notification email. (only separated by spaces no commas!!)
        
        ic) Log_File with default value test.log
        
      ii) add Password Parameter:
        iia) Password with the default value being youre server email password
        
      iii) add boolean parameter:
        iiia) Clean with default value selected

    c) click advanced below the paramaters you just added
      i) select use custom workspace

      ii) for Directory enter the path to this repository. should have the python scripts in the directory

    d) for build triggers selct build periodically
      i) use the help icon to figure out how to set the period

      ii) eg of schedule that runs at 11:30 pm: 30 23 * * *

    e) under build add build step "Execute windows batch command 
---------------------------------------------------------------------------
del __results.*
%Python36_Path%\python.exe EmailNotification.py -Server %Server% -Password %Password% -Receiver %Recipient_List% -Log %Log_File%

copy %Log_File% __results.log
copy SpeedTest_Plot.png __results.png
rem del %Log_File% SpeedTest_Plot.png

if [%Clean%] equ [true] del %Log_File% SpeedTest_Plot.png
----------------------------------------------------------------------------
      i) %Python36_Path% is setup in jenkins global vars, alternatie to this is adding pthyon.exe to PATH env var

    f) under post-build actions add archive artifacts 
      i) for files to archive enter __results.*

    g) click save

