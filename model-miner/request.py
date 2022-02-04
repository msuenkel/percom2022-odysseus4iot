from carmodels_connector import CARModels_Connect
from model_set import ML_Model
from model_set import Model_Set
import logging

class Request:

    top_model_limit=100


    def __init__(self, name, sensor_system, labels,maxsize_bignode, maxsize_allnodes, modelset_limit):
        self.name = name
        self.sensor_system = sensor_system
        self.labels_dict=dict()
        self.labels_dict.clear()
        for label_acc in labels:
            label=label_acc["label"]
            acc=label_acc["acc_threh"]
            acc=round(acc/100, 4)
            self.labels_dict[label]=acc
        #self.labels_dict=sorted(self.labels_dict.keys())

        self.maxsize_bignode= maxsize_bignode*1000
        self.maxsize_allnodes = maxsize_allnodes*1000
        self.modelset_limit= modelset_limit

    def __str__(self):
        return f"{self.name} , {self.sensor_system} , {self.labels_dict} , {self.maxsize_bignode} , " \
               f"{self.maxsize_allnodes} , {self.modelset_limit}"

    # Instance method



    def mine_request(self, request_name, accuracy_factor):

        print(type(self.labels_dict), self.labels_dict)
        logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

        models_dict=dict()
        models_dict.clear()
        modelSet_name=""

        # define the query for all labels in a request
        query = "SELECT id, binary_model, labels, sensor_system, algorithm, frequency, window_type, window_size, " \
                "window_stride, features, test_accuracy, model_size_in_bytes FROM public.trained_models where " \
                "labels like {} and test_accuracy>={} and model_size_in_bytes<={} and window_size<=10000"
        main_query=""

        modelSet_list = list()
        models_list=list()
        previous_Modelsets = list()

        for key in self.labels_dict:
            previous_Modelsets.clear()
            previous_Modelsets=modelSet_list.copy()
            modelSet_list.clear()
            label=key
            #modelSet_name=modelSet_name+label+"_"
            accuracy=self.labels_dict[key]
            label="'%"+label+"%'"
            main_query=query.format(label, accuracy, self.maxsize_bignode*1000)

            carConnector = CARModels_Connect()
            result_list=list()
            result_list.clear()
            result_list = carConnector.select_query(main_query)
            print(main_query)
            #form dictionry of models selected from database
            models_list.clear()
            for result in result_list:
                id=result[0]
                model_type=result[1]
                labels=result[2]
                label_list=labels.split("_")
                sensor_system=result[3]
                algorithm=result[4]
                frequency=result[5]
                window_type=result[6]
                window_size=result[7]
                window_stride=result[8]
                feature_set=result[9]
                model_accuracy=result[10]
                model_size=result[11]
                model=ML_Model(id, model_type, label_list, model_accuracy, sensor_system , frequency, window_type, window_size,
                           window_stride, feature_set, model_size, algorithm)
                model.set_preprocessing()
                #print(model)
                models_list.append(model)
            print("modelsets from this iteration:", request_name, key, accuracy, len(previous_Modelsets), len(models_list))

            if len(models_list)==0:
                modelSet_list.clear()
                return modelSet_list


            if len(previous_Modelsets)>0:
                bestModelset_list= return_top_modelsets(previous_Modelsets, accuracy_factor, self.top_model_limit)
                print("just best models are : ", len(bestModelset_list))
                for modelSet in bestModelset_list:
                    #print("main label ", key, value, modelSet.name)
                    if key in modelSet.model_labels:
                        if modelSet.model_labels[key]>=accuracy:
                            modelSet_list.append(modelSet)
                            continue
                    for nextModel in models_list:
                        #print("next modelID", nextModelID)
                        allModels_size=modelSet.overall_size+nextModel.model_size
                        #print("allowed size and models size", self.maxsize_allnodes, allModels_size)
                        if (allModels_size<=self.maxsize_allnodes):
                            modelSet_name=modelSet.name+"_"+str(nextModel.id)
                            new_modelSet = Model_Set(modelSet_name)
                            #logging.info(modelSet)
                            #print("under study modelset:" , modelSet)
                            #print(i, "ADD next modelID", key, value, nextModelID, nextModel.labels, nextModel.accuracy)
                            logging.info(nextModel)
                            for existModel in modelSet.ml_models:
                                new_modelSet.add_model(existModel)
                            new_modelSet.add_model(nextModel)
                            modelSet_list.append(new_modelSet)
                            #print("new modelset added", new_modelSet)
                            logging.info(new_modelSet)
                print("for this iteration modelset list", len(modelSet_list))

            else:
                for nextModel in models_list:
                    modelSet_name = str(nextModel.id)
                    new_modelSet = Model_Set(modelSet_name)
                    new_modelSet.add_model(nextModel)
                    modelSet_list.append(new_modelSet)
                print("for first iteration modelset list", len(modelSet_list))

        print("modelsets from last iteration: ", len(modelSet_list))
        #define final score
        print("calculate modelSets score ...")
        highest_score=0
        #fake_modelset=list()
        #fake_modelset=return_top_modelsets(modelSet_list, accuracy_factor, self.top_model_limit)
        for model_set in modelSet_list:
            model_set.define_querySharing_level()
            model_set.define_finalScore(accuracy_factor)
            if model_set.finalScore> highest_score:
                highest_score=model_set.finalScore


        print("highest score :", highest_score)
        return modelSet_list



def return_top_modelsets(modelset_list, accuracy_factor, top_model_limit):
    score_list=list()
    score_list.clear()
    sorted_modelset_list=list()
    sorted_modelset_list.clear()
    final_modelset_list=list()
    final_modelset_list.clear()
    name_check_list=list()
    name_check_list.clear()

    if len(modelset_list)<=top_model_limit:
        return modelset_list

    for modelset in modelset_list:
        modelset.define_intermediate_score(accuracy_factor)
        score_list.append(modelset.intermediateScore)

    score_list.sort(reverse=True)
    #print("scores are: ", score_list)
    for i in range(0, top_model_limit):
        for modelset in modelset_list:
            if modelset.name in name_check_list:
                continue
            if modelset.intermediateScore>=score_list[i]:
                name_check_list.append(modelset.name)
                sorted_modelset_list.append(modelset)

    print("first intermediate score:" , score_list[0] )
    #print("let's see how many sorted models", len(sorted_modelset_list))
    final_modelset_list=sorted_modelset_list[0:top_model_limit]
    return final_modelset_list
