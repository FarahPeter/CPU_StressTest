import random
import multiprocessing
import json
import socket
import time
from datetime import datetime
from datetime import date


# Write Data in JSON file
def WriteToJSON(ar):
    with open('History.json', 'w') as f:
        json.dump(ar, f)


def stress_test_cpu_process(process_id,semaphore,lastThread,singleThreaded=True):
    #print(f"Process#{process_id} started")

    # Generating a large list of random numbers
    #print(f"Process#{process_id}, Generating a large list of random numbers")
    sizeOfList=20000
    large_list=[0]*sizeOfList
    itrationNumber=30000000
    multiplicationfactor = 0.25
    for i in range (itrationNumber):
        if(i<sizeOfList):
            large_list[i]=random.random()
        else:
            x=random.random()
        #print progress %
        #the multiplication factor is relative to how much time this take relatively to the sort operation
        if ( int(((i+1)/itrationNumber)*100*multiplicationfactor) != int(((i)/itrationNumber)*100*multiplicationfactor)):
            #print(f"Process#{process_id}, {int((i + 1) / itrationNumber * 100 * multiplicationfactor)} %")
            if(process_id==(lastThread-1) or singleThreaded):
                print(f"{int((i + 1) / itrationNumber * 100 * multiplicationfactor)} %")

    # Performing a bubble sort on the list
    #print(f"Process#{process_id}, Sorting a large list")
    multiplicationfactor = 0.75
    for i in range(sizeOfList):
        for j in range(sizeOfList - 1):
            if large_list[j] > large_list[j + 1]:
                large_list[j], large_list[j + 1] = large_list[j + 1], large_list[j]

        #print process progress %
        if ( int(((i+1)/sizeOfList)*100*multiplicationfactor) != int(((i)/sizeOfList)*100*multiplicationfactor)):
            #print(f"Process#{process_id}, {int(25 + ((i + 1) / sizeOfList * 100 * multiplicationfactor))} %")
            if (process_id == lastThread-1 or singleThreaded):
                print(f"{int(25+ ((i+1)/sizeOfList)* 100 * multiplicationfactor)} %")


    #print("Process {} completed".format(process_id))
    semaphore.release()


def stress_test_cpu_multiprocessing(num_processes):
    start_time = time.time()
    processes = []
    #pcThreadCount = multiprocessing.cpu_count()
    semaphore = multiprocessing.Semaphore(num_processes)
    for i in range(num_processes):
        semaphore.acquire()
        if (num_processes==1):
            process = multiprocessing.Process(target=stress_test_cpu_process, args=(i,semaphore,num_processes,True))
        else:
            process = multiprocessing.Process(target=stress_test_cpu_process, args=(i,semaphore,num_processes,False))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()

    #print("Time taken to complete the stress test: {:.2f} seconds".format(time.time() - start_time))
    score=int(100/(time.time()-start_time) *100)
    return (score)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    '''while True:
        num_processes = input("Shose number of threads for multy core test: ")
        try:
            num_processes=int(num_processes)
            if (num_processes<=0):
                print("Value must be positive")
            else:
                break
        except:
            print("Value must be an integer")
    '''

    print("Performing single core test")
    singleCoreScore=stress_test_cpu_multiprocessing(1)

    print("Performing multy core test")
    pcThreadCount = multiprocessing.cpu_count()
    num_processes=pcThreadCount
    multyCoreScore=stress_test_cpu_multiprocessing(num_processes)*num_processes

    #read previous score from json file
    try:
        f = open('History.json')
        data = json.load(f)
        print("Previous runs:")
        for name in data:
            print(str(name)+": "+str(data[name]))
        f.close()
    except Exception as e:
        data={}

    host_name = socket.gethostname()
    data[str(host_name)+" on "+str(date.today().strftime("%b-%d-%Y")) + " at " + str(
                datetime.now().strftime("%H-%M-%S"))]={"Single Core Score":singleCoreScore,"multy core score":multyCoreScore}
    WriteToJSON(data)
    print()
    print()
    print("Your score:")
    print("--------------------")
    print(f"Single core score: {singleCoreScore}")
    print(f"Multy core score: {multyCoreScore}")
    print("--------------------")
    print()
    print()
    input("--Press Enter to exit--")

