import gmail
import argparse
import datetime
from matplotlib import pyplot as plt

PLOT_FILE_NAME    = "SpeedTest_Plot.png" 

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
    time_points = list()
    upload_points = list()
    download_points = list()
    results = str()

    #read results
    print("Reading Results...")
    with open(log_file_name, 'r') as file:
        results = file.read()

    for line in results.split('\n'):
        if len(line) > 0:
            words = line.split(' ')
            test_time = words[0].strip('[]')
            upload    = words[3]
            download  = words[6]

            time_points.append(test_time)
            upload_points.append(float(upload))
            download_points.append(float(download))

    plt.plot(time_points, upload_points, color='blue', label="Upload")
    plt.plot(time_points, download_points, color='orange', label="Download")
    plt.ylabel("Speed(Mbits/s)")
    plt.xlabel("Time(Hours)")
    plt.title("Upload and Download Speed Summary")
    plt.legend(loc="upper left")
    plt.savefig(PLOT_FILE_NAME)

    #send results
    for recipient in recipient_list:
        print("Sending results to {}...".format(recipient))
        msg = gmail.Message('Speed Test [{}:{}, {}/{}/{}]'.format(time.hour, time.minute, time.day, time.month, time.year),\
                            to=recipient,\
                            attachments=[PLOT_FILE_NAME, log_file_name])
        mail_server.send(msg)
