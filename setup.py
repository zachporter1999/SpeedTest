import sys
import argparse
import os

PLATFORM = sys.platform

AIX = 'aix'
LINUX = 'linux'
WINDOWS = 'win32'
CYGWIN = 'cygwin'
MACOS = 'darwin'

def setup_aix(parser):
    return

def setup_linux(parser):
    return 

def setup_windows(parser):

    #parse args
    parser.add_argument('-XML', nargs=2, type=str,  required=True,  help="The XML 2 config file used to setup the task.  -XML <speed test config> <email notification config>")
    
    args = parser.parse_args()

    testConfig, emailConfig = args.XML

    testSpeedTask = 'test_Internet_Speed_Periodic'
    emailTestTask = 'email_Speed_Test_Results_Periodic'

    createTestSched = 'schtasks /create /tn {} /xml {}'.format(testSpeedTask, testConfig)
    deleteTestSched = 'schtasks /delete /tn {}'.format(testSpeedTask)

    createEmailSched = 'schtasks /create /tn {} /xml {}'.format(emailTestTask, emailConfig)
    deleteEmailSched = 'schtasks /delete /tn {}'.format(emailTestTask)

    print("Scheduling with configs {} and {}".format(testConfig, emailConfig))

    os.system(deleteTestSched)
    os.system(createTestSched)

    os.system(deleteEmailSched)
    os.system(createEmailSched)

    return

def setup_cygwin(parser):
    return 

def setup_mac(parser):
    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    if PLATFORM == AIX:
        #AIX setup
        setup_aix(parser)

    elif PLATFORM == LINUX:
        #Linux setup
        setup_linux(parser)

    elif PLATFORM == WINDOWS:
        #Windows setup
        setup_windows(parser)
    
    elif PLATFORM == CYGWIN:
        #Cygwin setup
        setup_cygwin(parser)
    
    elif PLATFORM == MACOS:
        #Mac setup
        setup_mac(parser)