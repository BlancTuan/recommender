from processData import processData
from src.decisionTables import coverLatticeDecisionTables
from caserec.utils.process_data import ReadFile
from src.process_reducts import process_reduct
from src.MLM_learn import MLM_learn
import time
import random

# inputFile = "../data/ml-100k/u.data"
checkFile = "E:/khoaLuan/SRC/improvedCBCF/improvedCBCF/data/data_check.txt"
inputFile = "../data/jester-data-1/data.data"
outTestFile = "../data/export/u.test"
outTrainFile = "../data/export/u.train"



start_time = time.time()

class recommender:
    def __init__(self):
        # self.trainset = icbcfPrediction(train_file=in_file,test_file=train_file,cold_start_user_threshold=30,output_file=output_file,k_neighbors=60,ratio_threshold=0.9).compute()
        self.trainSets = ReadFile(checkFile).read()
    def result(self):
        # cov(self.trainset).process_reduct_finding()
        # cov(self.trainset).fitting_finding()
        # recommender = process_reduct(self.trainSets).process_finding()
        reducts = process_reduct(self.trainSets).process_finding()

        recommender = MLM_learn().MLM_learn()

        print(recommender)
        # process_reduct(self.trainset).process_fitting_finding()
        print("--- %s seconds ---" % (time.time() - start_time))
recommender = recommender()
recommender.result()


# test = processData(inputFile, outTestFile, outTrainFile)
# test.findColdStartUser()
# test.export_data()
# test2 = coverLatticeDecisionTables(inputFile, outTrainFile)
# test2.check()