import speedtest
import argparse
import datetime
import os

def testSpeed():
    print("Initializing...")

    date = datetime.datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('-Threads',     required=True,  help="The number of threads to use")
    
    args = parser.parse_args()

    log_location = '__results[{}-{}-{}]'.format(date.day, date.month, date.year)
    log_file_name = os.path.join(log_location, 'results.log')
    if not os.path.isdir(log_location):
        os.mkdir(log_location)

    threads       = abs(int(args.Threads))

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
    time_stamp   = int(date.timestamp())
    result_final = "[{}] | Upload: {} Mbits/s, Download: {} Mbits/s\n".format(time_stamp, round(upload*10e-6, 3), round(download*10e-6, 3))

    print(result_final)

    with open(log_file_name, 'a') as file:
        file.write(result_final)

    print("Test Finished")

if __name__ == "__main__":
    testSpeed()