import getpass
import sched
import time
import SpeedTester
import EmailNotification
import datetime
import os

"""

Setup scheduale

used to set:
 o the regularity that the speed tests will run
 o the email server to use

list of recipeients will be read from file <recipients file>

"""

recipient_list = list()

def send_email(server_email, server_password, log_file_name):
    with open(recipient_file, 'r') as recipients:
            recipient_list = recipients.read().split('\n')

    EmailNotification.sendNotification(server_email, server_password, recipient_list, log_file_name)
    
if __name__ == "__main__":
    schedule = sched.scheduler(time.time, time.sleep)
    date = datetime.datetime.now()
    
    email_period = 86400 # 24 hrs * 3600 sec/hr
    email_priority = 1
    test_priority = 2
    test_threads = 0

    log_file = 'results/test_[{}-{}-{}].log'.format(date.day, date.month, date.year)
    recipient_file = "recipients"

    # setup

    #get email credentials
    email_addr = input("Enter email to send results from: ")
    email_pwrd = getpass.getpass(prompt="Password:")

    # get test schedule
    while (True):
        test_schedule = input("Enter testing schedule (HH:MM): " )
        try:
            hrs, mins = test_schedule.split(":")
            if hrs.isdigit() and mins.isdigit():
                hrs = int(hrs)
                mins = int(mins)
                if int(mins) >= 60:
                    print("Please enter proper date format")
                else:
                    break
            else:
                print("Please enter numeric date")
        except:
            print("Please enter the schedule in the correct format")

    test_period = hrs * 3600 + mins * 60


    # schedule tasks
    while(True):
        schedule.enter(email_period, email_priority, action=send_email, argument=(email_addr, email_pwrd, log_file)) 
        schedule.enter(test_period, test_priority, action=SpeedTester.testSpeed, argument=(test_threads, log_file)) 