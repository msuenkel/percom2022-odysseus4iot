import json

class Model_Set:

    #min_accuracy=0
    #avg_accuracy=0


    def __init__(self, name):
        self.name = name
        self.ml_models=list()
        self.model_ids = list()
        self.model_labels = dict()
        self.query_sharing_level = 0
        self.completeness = 0
        self.overall_size = 0
        self.model_numbers = 0
        self.min_accuracy=0
        self.avg_accuracy=0
        self.querySharing_level=0
        self.finalScore=0
        self.intermediateScore = 0


    def __str__(self):
        return f"{self.name}, {self.model_ids}, {self.model_labels}, {self.overall_size}, {self.model_numbers}, {self.finalScore}"

    def add_model(self, model):
        self.ml_models.append(model)
        self.model_numbers=self.model_numbers+1
        #if model.accuracy<self.min_accuracy:
            #self.min_accuracy=model.accuracy
        if self.model_numbers>1:
            self.avg_accuracy=round((self.avg_accuracy+model.accuracy)/2, 4)
        else: self.avg_accuracy=model.accuracy
        self.model_ids.append(model.id)
        self.model_ids.sort()
        for label in model.labels:
            if label in self.model_labels.keys():
                if self.model_labels[label]<model.accuracy:
                    self.model_labels[label]=model.accuracy
            else: self.model_labels[label]=model.accuracy
        self.overall_size=self.overall_size+model.model_size

    def return_modelID_string(self):
        self.model_ids.sort()
        str_of_ids=""
        for id in self.model_ids:
            str_of_ids=str_of_ids+str(id)
        #id_list=map(str, id_list)
        #string_ints = [str(int) for int in id_list]
        #str_of_ids = "".join(id_list)
        return str_of_ids


    def define_querySharing_level(self):
        self.querySharing_level=0
        i=0
        firstModel=self.ml_models[i]
        sensor_system_check=0
        preprocessing_check=0
        segmentation_check=0
        feature_check=0
        querySharing_level=0

        for i in range(1, len(self.ml_models)):
            model=self.ml_models[i]
            if firstModel.sensor_system!=model.sensor_system:
                sensor_system_check=1
            elif firstModel.preprocessing!=model.preprocessing:
                preprocessing_check=1
            elif (firstModel.window_type!=model.window_type) or (firstModel.window_size!=model.window_size) or (firstModel.window_stride!=model.window_stride):
                segmentation_check=1
            elif firstModel.feature_set!=model.feature_set:
                feature_check=1

        if sensor_system_check==0:
            querySharing_level=querySharing_level+1
            if preprocessing_check==0:
                querySharing_level=querySharing_level+1
                if segmentation_check==0:
                    querySharing_level=querySharing_level+1
                    if feature_check==0:
                        querySharing_level = querySharing_level + 1

        querySharing_level=querySharing_level*4+80
        self.querySharing_level=round(querySharing_level/100, 4)

    def define_finalScore(self, accuracy_factor):
        self.finalScore=0
        querySharing_factor=1-accuracy_factor
        self.finalScore=self.avg_accuracy*accuracy_factor+querySharing_factor*self.querySharing_level
        self.finalScore=round(self.finalScore, 4)


    def define_intermediate_score(self, accuracy_factor):
        i = 0
        querySharing_level = 0
        self.intermediateScore=0
        firstModel = self.ml_models[i]
        sensor_system_check = 0
        preprocessing_check = 0
        segmentation_check = 0
        feature_check = 0

        for i in range(1, len(self.ml_models)):
            model = self.ml_models[i]
            if firstModel.sensor_system != model.sensor_system:
                sensor_system_check = 1
            elif firstModel.preprocessing != model.preprocessing:
                preprocessing_check = 1
            elif (firstModel.window_type != model.window_type) or (firstModel.window_size != model.window_size) or (
                    firstModel.window_stride != model.window_stride):
                segmentation_check = 1
            elif firstModel.feature_set != model.feature_set:
                feature_check = 1

        if sensor_system_check == 0:
            querySharing_level = querySharing_level + 1
            if preprocessing_check == 0:
                querySharing_level = querySharing_level + 1
                if segmentation_check == 0:
                    querySharing_level = querySharing_level + 1
                    if feature_check == 0:
                        querySharing_level = querySharing_level + 1

        querySharing_level = querySharing_level *4+80
        querySharing_level = round(querySharing_level / 100, 4)
        #querySharing_level = round(querySharing_level / 3, 2)
        querySharing_factor = 1 - accuracy_factor
        self.intermediateScore = self.avg_accuracy * accuracy_factor + querySharing_factor *querySharing_level






class ML_Model:

    def __init__(self, model_id, model_type, labels, accuracy, sensor_system , frequency,
                 window_type, window_size, window_stride, feature_set, model_size, algorithm):
        self.id = model_id
        self.type=model_type
        self.labels=labels
        self.accuracy=accuracy
        self.sensor_system=sensor_system
        self.frequency=frequency
        self.window_type=window_type
        self.window_size=window_size
        self.window_stride=window_stride
        self.feature_set= feature_set
        self.model_size=model_size
        self.algorithm=algorithm
        self.preprocessing=""

    def __str__(self):
        return f"{self.id} , {self.type}, {self.labels}, {self.accuracy}, {self.sensor_system}, {self.frequency}, " \
               f" {self.window_type}, {self.window_size}, {self.window_stride}, " \
               f" {self.model_size}, {self.algorithm}"

    def set_preprocessing(self):
        feature_string=json.dumps(self.feature_set)
        accMagnitude="accMag"
        gyrMagnitude="gyrMag"
        if accMagnitude in feature_string:
            self.preprocessing=self.preprocessing+accMagnitude+"_"
        if gyrMagnitude in feature_string:
            self.preprocessing = self.preprocessing + gyrMagnitude + "_"

        self.preprocessing = self.preprocessing[:-1]



