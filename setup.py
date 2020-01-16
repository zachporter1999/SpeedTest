import sys
import argparse
import os
import xml.etree.ElementTree as ET

PLATFORM = sys.platform

AIX = 'aix'
LINUX = 'linux'
WINDOWS = 'win32'
CYGWIN = 'cygwin'
MACOS = 'darwin'

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__)) # directory of this script

def setup_aix(parser):
    return

def setup_linux(parser):
    return 

def setup_windows(parser):

    #parse args
    parser.add_argument('-Enable',  action='store_true', required=False,  help="used to enable the task")
    parser.add_argument('-Disable', action='store_true', required=False,  help="used to disable the task")
    parser.add_argument('-Delete',  action='store_true', required=False,  help="used to delete the task")
    parser.add_argument('-Create',  action='store_true', required=False,  help="used to create the task")
    
    args = parser.parse_args()

    enable = args.Enable
    disable = args.Disable
    delete = args.Delete
    create = args.Create


    testSpeedTask = 'test_Internet_Speed_Periodic'
    emailTestTask = 'email_Speed_Test_Results_Periodic'

    deleteTestSched = 'schtasks /delete /tn {}'.format(testSpeedTask)
    deleteEmailSched = 'schtasks /delete /tn {}'.format(emailTestTask)

    disableTestSched = 'schtasks /change /tn {} /DISABLE'.format(testSpeedTask)
    disableEmailSched = 'schtasks /change /tn {} /DISABLE'.format(emailTestTask)

    enableTestSched = 'schtasks /change /tn {} /ENABLE'.format(testSpeedTask)
    enableEmailSched = 'schtasks /change /tn {} /ENABLE'.format(emailTestTask)

    working_directory = "WorkingDirectory"
    periodic_interval = 'Interval'

    test_speed_template_xml = r"Configs\testSpeedTemplate.xml"
    send_email_template_xml = r"Configs\sendEmailTemplate.xml"

    createTestSched = 'schtasks /create /tn {} /xml {}'.format(testSpeedTask, test_speed_template_xml)
    createEmailSched = 'schtasks /create /tn {} /xml {}'.format(emailTestTask, send_email_template_xml)


    if  create:

        # edit xml
        ET.register_namespace('', "http://schemas.microsoft.com/windows/2004/02/mit/task")
        tree = ET.parse(test_speed_template_xml)
        root = tree.getroot()
        for child in root.iter():

            # sets the working directory
            if working_directory in child.tag:
                child.text = str(SCRIPT_DIR)
                print("Setting up working directory")

            if periodic_interval in child.tag:
                print("Enter how often you would like the tests to be run.")
                print("(eg. for a test to run ever 30 min enter 30M, for every hour enter 1H)")
                time = input("time: ").upper()

                ### error trapping of input ###

                child.text = "PT{}".format(time)

        # write to the template
        tree.write(test_speed_template_xml)

        print("Scheduling with configs {} and {}...".format(test_speed_template_xml, send_email_template_xml))

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