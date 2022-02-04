

import random
import json


def create_input_file(request_number):

    request_dict=dict()
    labels=['Liegen', 'Gehen', 'Grasen', 'Stehen', 'Wiederkauen']
    sensor_system = "Blaupunkt_BST-BNO055-DS000-14_NDOF_10_AO"
    accuracy_factor=1


    join = ''.join

    for i in range(request_number):
        request_name="request"+str(i+1)
        my_request=dict()

        my_request['sensor_system'] =sensor_system
        labels_number=random.randint(1,5)
        generated_labels = random.sample(labels, labels_number)
        labels_list=list()
        labels_list.clear()
        for label in generated_labels:
            my_label=dict()
            my_label["label"]=label
            generated_accuracy=round(random.uniform(75, 80), 2)
            my_label["acc_threh"]=generated_accuracy
            labels_list.append(my_label)

        my_request["labels"]=labels_list
        #my_request["accuracy_factor"] = accuracy_factor
        max_size_bigNode=random.randint(28, 1000000)
        my_request["maxsizeofbignode"]=max_size_bigNode
        max_size_allNodes=random.randint(max_size_bigNode, 1000000)
        my_request["maxsizeof_ALL"]=max_size_allNodes
        modelset_limit=random.randint(1, 5)
        my_request["modelset_limit"]=modelset_limit

        request_dict[request_name]=my_request

    json_object = json.dumps(request_dict, indent=4)

    # Writing to sample.json
    with open("input10_acc75-80.json", "w") as outfile:
        outfile.write(json_object)



if __name__ == '__main__':
    create_input_file(10)
