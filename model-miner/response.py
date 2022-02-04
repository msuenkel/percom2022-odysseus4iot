from model_set import Model_Set


class Response:


    def __init__(self, name, modelSet_list, modelset_limit):
        self.name = name
        self.modelSet_list=modelSet_list
        self.finalResponse=list()
        self.modelset_limit= modelset_limit
        self.top_modelSets=list()
        #self.response_time=response_time

    def __str__(self):
        return f"{self.name} , {len(self.modelSet_list)} , " \
               f"{self.modelset_limit} , {self.top_modelSets}"

    # Instance method
    def return_topModels(self):

        maxScore_list=list()
        maxScore_list.clear()
        bestModelSet_list=list()
        bestModelSet_list.clear()

        print("number of all models", len(self.modelSet_list), self.modelset_limit)

        for i in range(0, self.modelset_limit):
            #print(i)
            maxScore_list.append(0)
            for modelSet in self.modelSet_list:
                if i>0:
                    if modelSet.finalScore<maxScore_list[i-1]:
                        if modelSet.finalScore>maxScore_list[i]:
                            maxScore_list[i]=modelSet.finalScore
                else:
                    if modelSet.finalScore > maxScore_list[i]:
                        maxScore_list[i] = modelSet.finalScore

            print("final score round", i, maxScore_list[i])
            for modelSet in self.modelSet_list:
                if modelSet.finalScore==maxScore_list[i]:
                    bestModelSet_list.append(modelSet)

        print("let's see best models numbers: ", len(bestModelSet_list))
        self.top_modelSets=bestModelSet_list[0:self.modelset_limit]
        #for top_model in self.top_modelSets:
            #print("top model scores : ", top_model.finalScore, top_model.querySharing_level, top_model.avg_accuracy)
        print(self.name, "return topmodels", len(self.top_modelSets), self.top_modelSets)


    def create_response(self):

        for modelSet in self.top_modelSets:
            myResponse={}
            myResponse["Modelset_name"]=modelSet.name
            myResponse["avg_accuracy"] = modelSet.avg_accuracy
            myResponse["query_sharing_level"] = modelSet.querySharing_level
            myResponse["final_score"] = modelSet.finalScore
            myResponse["number_of_models"] = len(modelSet.ml_models)
            model_list=[]
            for model in modelSet.ml_models:
                myModel={}
                myModel["model_id"]=model.id
                myModel["type"] = model.type
                myModel["labels"] = model.labels
                myModel["accuracy"] = model.accuracy
                myModel["sensor_system"] = model.sensor_system
                myModel["preprocessing"] = model.preprocessing
                myModel["window_type"] = str(model.window_type)
                myModel["window_size"] = str(model.window_size)
                myModel["window_stride"] = str(model.window_stride)
                myModel["features"]=model.feature_set
                myModel["size"] = model.model_size
                myModel["algorithm"] = model.algorithm
                model_list.append(myModel)

            myResponse["ml_models"] = model_list
            self.finalResponse.append(myResponse)

        return self.finalResponse






