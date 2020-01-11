import gmail
import argparse
import datetime
from matplotlib import pyplot as plt

def sendNotification(server_email, server_password, recipient_list):
    date = datetime.datetime.now()
    plot_file_name = "results/summary_[{}-{}-{}].png".format(date.day, date.month, date.year) 
    log_file_name = "results/results_[{}-{}-{}].log".format(date.day, date.month, date.year)


    #log into email
    print("Logging into {}...".format(server_email))
    mail_server = gmail.GMail(server_email, server_password)

    time = datetime.datetime.now()
    time_points = list()
    upload_points = list()
    download_points = list()
    results = str()

    # midnight time in unix time
    midnight = datetime.datetime(time.year, time.month, time.day).timestamp()

    #read results
    print("Reading Results...")
    with open(log_file_name, 'r') as file:
        results = file.read()

    for line in results.split('\n'):
        if len(line) > 0:
            words = line.split(' ')
            test_date = words[0].strip('[]').split('/')
            test_time = words[1].strip('[]').split(':')
            upload    = words[4]
            download  = words[7]

            timestamp = datetime.datetime(int(test_date[2]), int(test_date[1]), int(test_date[0]), int(test_time[0]), int(test_time[1])).timestamp()

            time_points.append((float(timestamp) - midnight)//3600)
            upload_points.append(float(upload))
            download_points.append(float(download))

    plt.plot(time_points, upload_points, color='blue', label="Upload")
    plt.plot(time_points, download_points, color='orange', label="Download")
    plt.ylabel("Speed(Mbits/s)")
    plt.xlabel("Time(Hours)")
    plt.title("Upload and Download Speed Summary")
    plt.legend(loc="upper left")
    plt.savefig(plot_file_name)

    #send results
    for recipient in recipient_list:
        print("Sending results to {}...".format(recipient))
        msg = gmail.Message('Speed Test [{}:{}, {}/{}/{}]'.format(time.hour, time.minute, time.day, time.month, time.year),\
                            to=recipient,\
                            attachments=[plot_file_name, log_file_name])
        mail_server.send(msg)

if __name__ == "__main__":
    #parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-Server',   type=str,  required=True,  help="The email to send the results from")
    parser.add_argument('-Password', type=str, required=True,  help="The password for the server")
    parser.add_argument('-Receiver', type=str, required=True,  help="The addresses to send results to", nargs='+')
    
    args = parser.parse_args()

    server_email    = args.Server
    server_password = args.Password
    recipient_list  = args.Receiver

    sendNotification(server_email, server_password, recipient_list)