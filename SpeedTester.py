import speedtest
import argparse
import datetime

if __name__ == "__main__":

    print("Initializing...")

    parser = argparse.ArgumentParser()
    parser.add_argument('-Log',      required=True,  help="The file name to write the results to")
    parser.add_argument('-Threads',     required=True,  help="The number of threads to use")
    
    args = parser.parse_args()

    log_file_name = args.Log
    threads       = abs(int(args.Threads))

    # list of servers
    server = list()

    # create speedtest object
    test = speedtest.Speedtest()

    # run test
    print("Testing Upload...")
    test.upload(threads=threads)

    print("Testing Download...")
    test.download(threads=threads)

    # get results
    print("logging results...")
    results      = test.results.dict()
    upload       = results['upload']
    download     = results['download']
    time         = datetime.datetime.now()
    time_stamp   = "{}:{}".format(time.hour, time.minute)
    result_final = "[{}] | Upload: {} Mbits/s, Download: {} Mbits/s\n".format(time_stamp, round(upload*10e-6, 3), round(download*10e-6, 3))

    print(result_final)

    with open(log_file_name, 'a') as file:
        file.write(result_final)

    print("Test Finished")