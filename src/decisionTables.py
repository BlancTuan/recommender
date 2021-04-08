from caserec.utils.process_data import ReadFile

from processData import processData as prData


class coverLatticeDecisionTables:
    def __init__(self, inputFile, inputTrainFile, coldStartThreshold = 30):
        self.inputFile = inputFile
        self.inputTrainFile = inputTrainFile
        self.coldStartThreshold = coldStartThreshold
        self.trainSets = ReadFile(self.inputFile).read()
        self.cold_start_users = prData.findColdStartUser(self)
        self.reduct_users = []
        self.reduct_item = []

    # Trả về danh sách các mục không được đánh giá của người dùng khời đầu nguội
    def itemUnobserved(self, userId):
        # Danh sách mục không được đánh giá
        itemUnobserved = []
        for i in self.cold_start_users:
            if i == userId:
                itemUnobserved =  self.trainSets["items_unobserved"][i]
                break;
        self.itemUnobserved = itemUnobserved
        return self.itemUnobserved

    # Thuật toán tìm dàn điều kiện
    def findingConditionCover(self, userId):
        return 1

    # Thuật toán Reduct_Finding rút gọn dàn điều kiện
    def reductFinding(self):
        return 1

    def check(self):
        for i in self.cold_start_users:
            print(i)