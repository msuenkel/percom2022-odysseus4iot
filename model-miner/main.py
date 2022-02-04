# This is a sample Python script.
import json
from request import Request
from response import Response
from datetime import datetime

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main_miner():

    #accuracy_factor=0.5

    # First step: read from json file and create the list of requests
    # reading from input file (requests)
    request_list=list()
    request_list.clear()
    response_dic=dict()
    response_dic.clear()
    file = open('requests_ms2.json', "r")
    requests_dic = json.load(file)
    #print(type(requests_dic))

    for request in requests_dic:
        req_name=str(request)
        print(requests_dic[req_name])
        sensor_system=requests_dic[req_name]["sensor_system"]
        labels=requests_dic[req_name]["labels"]
        #print("labels", type(labels))
        accuracy_factor = requests_dic[req_name]["accuracy_factor"]
        maxsize_bignode= requests_dic[req_name]["maxsizeofbignode"]
        maxsize_allnodes=requests_dic[req_name]["maxsizeof_ALL"]
        modelset_limit= requests_dic[req_name]["modelset_limit"]
        my_request=Request(req_name, sensor_system, labels, maxsize_bignode, maxsize_allnodes, modelset_limit)
        print(my_request)
        start_mining=datetime.now()
        request_list.append(my_request)
        modelSet_list=my_request.mine_request(my_request.name, accuracy_factor)
        #responese_name="response"+req_name[7:]
        responese_name = "response_" + req_name
        my_response=Response(responese_name, modelSet_list, modelset_limit)
        my_response.return_topModels()
        end_mining = datetime.now()
        response_time = (end_mining - start_mining).total_seconds()*1000000
        response_time=round(response_time, 2)
        #print("time check: ", start_mining, end_mining, response_time)
        responese_name = responese_name + "_" + str(response_time)
        response_dic[responese_name]=my_response.create_response()
        print(my_response)


    file.close()


    with open("response_ms.json", 'w') as fout:
        json_dumps_str = json.dumps(response_dic, indent=4)
        print(json_dumps_str, file=fout)

    # extract each request
    #for request in request_list:
    #    print("start mining", request.name)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_miner()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
