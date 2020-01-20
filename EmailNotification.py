import gmail
import argparse
import datetime
import numpy
from scipy.interpolate import splrep, splev
from matplotlib import pyplot as plt

def sendNotification():
    plot_file_name = "SpeedTest_Plot.png" 

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

    # midnight time in unix time
    midnight = datetime.datetime(time.year, time.month, 9).timestamp()

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

    time_new = numpy.linspace(time_points[0], time_points[len(time_points)-1], 100)

    upload_spline   = splrep(time_points, upload_points)
    download_spline = splrep(time_points, download_points)

    upload_points   = splev(time_new, upload_spline,   der=0)
    download_points = splev(time_new, download_spline, der=0)

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
        msg = gmail.Message('Speed Test [{}:{}, {}/{}/{}]'.format(time.hour, time.minute, time.day, time.month, time.year),\
                            to=recipient,\
                            attachments=[plot_file_name, log_file_name])
        mail_server.send(msg)

if __name__ == "__main__":
    sendNotification()