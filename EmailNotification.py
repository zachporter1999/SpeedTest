import gmail
import argparse
import datetime
import numpy
import os
from scipy.interpolate import splrep, splev
from matplotlib import pyplot as plt

def sendNotification():
    date = datetime.datetime.now()
    log_location = '__results[{}-{}-{}]'.format(date.day, date.month, date.year)
    plot_file_name = os.path.join(log_location, 'results.png')
    log_file_name  = os.path.join(log_location, 'results.log')

    #parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-Server',   type=str,  required=True,  help="The email to send the results from")
    parser.add_argument('-Password', type=str, required=True,  help="The password for the server")
    parser.add_argument('-Receiver', type=str, required=True,  help="The addresses to send results to", nargs='+')
    
    args = parser.parse_args()

    server_email    = args.Server
    server_password = args.Password
    recipient_list  = args.Receiver

    #log into email
    print("Logging into {}...".format(server_email))
    mail_server = gmail.GMail(server_email, server_password)

    time_points = list()
    upload_points = list()
    download_points = list()
    results = str()

    # midnight time in unix time
    midnight = datetime.datetime(date.year, date.month, date.day).timestamp()

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

            time_points.append((float(test_time) - midnight)/3600)
            upload_points.append(float(upload))
            download_points.append(float(download))

    # interpolate results with spline
    time_new = numpy.linspace(time_points[0], time_points[len(time_points)-1], 100)

    upload_spline   = splrep(time_points, upload_points)
    download_spline = splrep(time_points, download_points)

    upload_points   = splev(time_new, upload_spline,   der=0)
    download_points = splev(time_new, download_spline, der=0)

    # generate plot
    plt.plot(time_new, upload_points, color='blue', label="Upload")
    plt.plot(time_new, download_points, color='orange', label="Download")
    plt.ylabel("Speed(Mbits/s)")
    plt.xlabel("Time(Hours)")
    plt.title("Upload and Download Speed Summary")
    plt.legend(loc="upper left")
    plt.savefig(plot_file_name)

    #send results
    for recipient in recipient_list:
        print("Sending results to {}...".format(recipient))
        msg = gmail.Message('Speed Test [{}:{}, {}/{}/{}]'.format(date.hour, date.minute, date.day, date.month, date.year),\
                            to=recipient,\
                            attachments=[plot_file_name, log_file_name])
        mail_server.send(msg)

    # move results to package
    os.replace(log_location, os.path.join('pkg', log_location))

if __name__ == "__main__":
    sendNotification()