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
    parser.add_argument('-Enable',  action='store_true', required=False,  help="used to enable the task")
    parser.add_argument('-Disable', action='store_true', required=False,  help="used to disable the task")
    parser.add_argument('-Delete',  action='store_true', required=False,  help="used to delete the task")
    parser.add_argument('-XML',     nargs=2,             required=False,  help="The XML 2 config file used to setup the task.  -XML <speed test config> <email notification config>")
    
    args = parser.parse_args()

    enable = args.Enable
    disable = args.Disable
    delete = args.Delete
    xmls = args.XML

    testSpeedTask = 'test_Internet_Speed_Periodic'
    emailTestTask = 'email_Speed_Test_Results_Periodic'

    deleteTestSched = 'schtasks /delete /tn {}'.format(testSpeedTask)
    deleteEmailSched = 'schtasks /delete /tn {}'.format(emailTestTask)

    disableTestSched = 'schtasks /change /tn {} /DISABLE'.format(testSpeedTask)
    disableEmailSched = 'schtasks /change /tn {} /DISABLE'.format(emailTestTask)

    enableTestSched = 'schtasks /change /tn {} /ENABLE'.format(testSpeedTask)
    enableEmailSched = 'schtasks /change /tn {} /ENABLE'.format(emailTestTask)

    if xmls != None:
        testConfig, emailConfig = xmls
        createTestSched = 'schtasks /create /tn {} /xml {}'.format(testSpeedTask, testConfig)
        createEmailSched = 'schtasks /create /tn {} /xml {}'.format(emailTestTask, emailConfig)

    if  xmls != None:

        print("Scheduling with configs {} and {}...".format(testConfig, emailConfig))

        os.system(deleteTestSched)
        os.system(createTestSched)

        os.system(deleteEmailSched)
        os.system(createEmailSched)

    elif delete:

        print("delteing tasks...")

        os.system(deleteTestSched)
        os.system(deleteEmailSched)

    elif disable:

        print("disabling tasks...")

        os.system(disableTestSched)
        os.system(disableEmailSched)

    elif enable:

        print('enabling tasks...')
        
        os.system(enableTestSched)
        os.system(enableEmailSched)

    else:
        print("usage: setup.py [-h] [-Enable] [-Disable] [-Delete] [-XML XML XML]")
        print()
        print("optional arguments:")
        print("-h, --help    show this help message and exit")
        print("-Enable       used to enable the task")
        print("-Disable      used to disable the task")
        print("-Delete       used to delete the task")
        print("-XML XML XML  The XML 2 config file used to setup the task. -XML <speed test config> <email notification config>")


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