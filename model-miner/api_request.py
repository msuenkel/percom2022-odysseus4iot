import requests
import json
import json
#from request import Request

BASE="http://127.0.0.1:5000/"


if __name__ == '__main__':
    request_list = list()
    request_list.clear()
    response_dic = dict()
    response_dic.clear()
    file = open('requests_ms2.json', "r")
    requests_dic = json.load(file)

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

        json_data={"name":req_name, "sensor_system":sensor_system, "labels": labels, "accuracy_factor": accuracy_factor,
                   "maxsizeofbignode": maxsize_bignode, "maxsizeof_ALL": maxsize_allnodes, "modelset_limit": modelset_limit}

        #json_dump = json.dumps(json_data)
        #print(json_dump)

        #request_line=sensor_system+"/"+labels+"/" #+accuracy_factor+"/"+maxsize_bignode+"/"+maxsize_allnodes+"/"+modelset_limit
        response=requests.post(BASE+"/post_form", json=json_data)
        #r = requests.post('https://reqbin.com/echo/post/json')
        print(response.json())



