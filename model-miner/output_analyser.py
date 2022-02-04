import json
from response import Response

def analyse_output():
    modelset_list = list()
    modelset_list.clear()
    modelsets_metrics=[0,0,0,0,0]
    modelset_numbers=0
    response_number=0
    response_dic = dict()
    response_dic.clear()
    file = open('output10_acc75-80-factor05-top200.json', "r")
    response_dic = json.load(file)
    for response in response_dic:
        response_number=response_number+1
        res_name=str(response)
        res_name_response = str(res_name).split("_")
        res_responseTime = res_name_response[1]
        modelsets_metrics[4] = modelsets_metrics[4] + float(res_responseTime)
        print("response time: ", res_responseTime)
        #print(response_dic[res_name])
        modelset_list=response_dic[res_name]
        print("request: ", res_name, len(modelset_list))
        res_name_time=res_name.split("_")
        response_time=res_name_time[1]
        if len(modelset_list) == 0: modelsets_metrics[3] = modelsets_metrics[3] + 1
        for modelset in modelset_list:
            modelset_numbers=modelset_numbers+1
            modelset_name=modelset["Modelset_name"]
            modelset_accuracy=modelset["avg_accuracy"]
            modelsets_metrics[0]=modelsets_metrics[0]+modelset_accuracy
            modelset_QSHL=modelset["query_sharing_level"]
            modelsets_metrics[1] = modelsets_metrics[1] + modelset_QSHL
            modelset_finalscore=modelset["final_score"]
            modelsets_metrics[2] = modelsets_metrics[2] + modelset_finalscore
            modelset_modelNum=modelset["number_of_models"]
            print("modelset: ", modelset_name, modelset_accuracy, modelset_QSHL, modelset_finalscore, modelset_modelNum)

    modelsets_metrics[0]=round(modelsets_metrics[0]/modelset_numbers, 4)
    modelsets_metrics[1] = round(modelsets_metrics[1] / modelset_numbers, 4)
    modelsets_metrics[2] = round(modelsets_metrics[2] / modelset_numbers, 4)
    modelsets_metrics[4] = round(modelsets_metrics[4] / response_number, 4)
    print(modelset_numbers, modelsets_metrics[0], modelsets_metrics[1], modelsets_metrics[2], modelsets_metrics[3], modelsets_metrics[4])




if __name__ == '__main__':
    analyse_output()