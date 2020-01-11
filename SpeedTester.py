import speedtest
import argparse
import datetime

def testSpeed(threads):

    date = datetime.datetime.now()
    log_file_name = "results/results_[{}-{}-{}].log".format(date.day, date.month, date.year)
    server = list()
    test = speedtest.Speedtest()

    print("Initializing...")

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
    time_stamp   = "{}/{}/{} {}:{}".format(date.day, date.month, date.year, date.hour, date.minute)
    result_final = "[{}] | Upload: {} Mbits/s, Download: {} Mbits/s\n".format(time_stamp, round(upload*10e-6, 3), round(download*10e-6, 3))

    print(result_final)

    with open(log_file_name, 'a') as file:
        file.write(result_final)

    print("Test Finished")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-Threads',     required=True,  help="The number of threads to use")
    
    args = parser.parse_args()

    threads       = abs(int(args.Threads))

    testSpeed(threads)