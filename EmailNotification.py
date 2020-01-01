import os
import gmail
import argparse
import datetime

if __name__ == "__main__":

    #parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-Server',   type=str,  required=True,  help="The email to send the results from")
    parser.add_argument('-Password', type=str, required=True,  help="The password for the server")
    parser.add_argument('-Receiver', type=str, required=True,  help="The addresses to send results to", nargs='+')
    parser.add_argument('-Log',      type=str, required=True,  help="The file name to read the results from")
    
    args = parser.parse_args()

    server_email    = args.Server
    server_password = args.Password
    recipient_list  = args.Receiver
    log_file_name   = args.Log

    #log into email
    print("Logging into {}...".format(server_email))
    mail_server = gmail.GMail(server_email, server_password)

    time = datetime.datetime.now()
    results = str()

    #read results
    print("Reading Results...")
    with open(log_file_name, 'r') as file:
        results = file.read()

    #send results
    for recipient in recipient_list:
        print("Sending results to {}...".format(recipient))
        msg = gmail.Message('Speed Test [{}:{}, {}/{}/{}]'.format(time.hour, time.minute, time.day, time.month, time.year),\
                            to=recipient,\
                            text=results)
        mail_server.send(msg)

    #clean up file
    os.remove(log_file_name)
        