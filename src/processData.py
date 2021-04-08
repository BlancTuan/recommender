from random import random

from caserec.recommenders.item_recommendation.base_item_recommendation import BaseItemRecommendation
from caserec.utils.process_data import ReadFile
from caserec.utils.process_data import WriteFile
import random
import os.path
from os import path

inputFile = "data/ml-100k/u.data"
outTestFile = "data/export/u.test"
outTrainFile = "data/export/u.train"
class processData(object):
    def __init__(self, inputFile, outTestFile, outTrainFile, coldStartThreshold=30):
        self.inputFile = inputFile
        self.outTestFile = outTestFile
        self.outTrainFile = outTrainFile
        self.trainSets = ReadFile(self.inputFile).read()
        self.coldStartThreshold = coldStartThreshold
        self.coldStartUser = self.findColdStartUser()
        self.dataTest = []
        self.dataTrain = []

    #Tim nguoi dung khoi dau nguoi
    def findColdStartUser(self):
        cold_start_user = []
        for i in self.trainSets["items_seen_by_user"]:
            # so luong rating tren phim < nguong khoi dau nguoi
            if len(self.trainSets["items_seen_by_user"][i]) < self.coldStartThreshold:
                cold_start_user.append(i)
                print("Nguoi dung", i, "khoi dau nguoi")
        return cold_start_user

    #Tien xu ly du lieu
    def processData(self):
        self.train_data = []
        self.test_data = []
        for i in self.trainSets["users"]:
            # Neu nguoi dung i la khoi dau nguoi
            if i in self.coldStartUser:
            #Random 20% danh gia cua nguoi dung khoi dau nguoi
                testData = random.choices(list(self.trainSets["items_seen_by_user"][i]),
                                          k = int(len(self.trainSets["items_seen_by_user"][i]) * 0.2))
                for u in self.trainSets["feedback"][i]:
                    if u in testData:
                        self.test_data.append([i, u, self.trainSets["feedback"][i][u]])
                    else:
                        self.train_data.append([i, u, self.trainSets["feedback"][i][u]])
            else:
                for u in self.trainSets["feedback"][i]:
                    self.train_data.append([i, u, self.trainSets["feedback"][i][u]])

    def export_data(self):
        self.processData()
        WriteFile(self.outTestFile, self.test_data).write()
        WriteFile(self.outTrainFile, self.train_data).write()