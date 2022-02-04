from flask import Flask, request
from flask_restful import Api, Resource
import json
from request import Request
from response import Response
from datetime import datetime


app = Flask(__name__)
api=Api(app)


def get(json_data):
    json_object = json.loads(json_data)
    print(json_object)
    return json_object

@app.route('/post_form', methods=['POST'])
def process_form():
    data = json.loads(request.data)
    #data = request.form
    req_name=data['name']
    sensor_system = data["sensor_system"]
    labels = data["labels"]
    # print("labels", type(labels))
    accuracy_factor = data["accuracy_factor"]
    maxsize_bignode = data["maxsizeofbignode"]
    maxsize_allnodes = data["maxsizeof_ALL"]
    modelset_limit = data["modelset_limit"]
    print(req_name, sensor_system, labels, accuracy_factor, maxsize_bignode, maxsize_allnodes, modelset_limit)
    my_request=Request(req_name, sensor_system, labels, maxsize_bignode, maxsize_allnodes, modelset_limit)
    print(my_request)

    start_mining = datetime.now()
    #request_list.append(my_request)
    modelSet_list = my_request.mine_request(my_request.name, accuracy_factor)
    # responese_name="response"+req_name[7:]
    responese_name = "response_" + req_name
    my_response = Response(responese_name, modelSet_list, modelset_limit)
    my_response.return_topModels()
    end_mining = datetime.now()
    response_time = (end_mining - start_mining).total_seconds() * 1000000
    response_time = round(response_time, 2)
    # print("time check: ", start_mining, end_mining, response_time)
    responese_name = responese_name + "_" + str(response_time)
    response_dic = dict()
    response_dic.clear()
    response_dic[responese_name] = my_response.create_response()
    json_response = json.dumps(response_dic, indent=4)
    print(json_response)


    return json_response



if __name__=="__main__":
    app.run(debug=True)