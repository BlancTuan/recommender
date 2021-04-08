import itertools
from caserec.recommenders.item_recommendation.userknn import UserKNN

from caserec.utils.process_data import ReadFile
from src.process_reducts import process_reduct

# inputFile = "../data/ml-100k/u.data"
inputFile = "../data/jester-data-1/data.data"
test_file = "../data/export/u.test"
train_file = "../data/export/u.train"
output_file = "../results/u.result"

class MLM_learn(UserKNN):
    def __init__(self):
        self.trainSets = ReadFile(inputFile).read()
        self.cl = {}
        self.dl = {}
        super().__init__(inputFile, inputFile, output_file=output_file)
        self.lis_user_covCl = set()

    # Ham tinh phu dinh
    def calculateTopCoverS(self, set_items):
        coverS = []
        topCl = []


        for i in range(0, len(set_items)):
            combination = list(itertools.combinations(set_items, i + 1))
            for element in combination:
                cover = [user for (user, items) in self.train_set["items_seen_by_user"].items()
                         if
                         set(element).issubset(items)]
                if cover not in coverS and len(cover) > 0:
                    topCl.append(cover)
                coverS.append(cover)
        if self.train_set["users"] not in topCl:
            topCl.append(self.train_set["users"])

        return topCl

    # Ham tim phu cam sinh
    def calculateCoverS(self, set_items):
        cov_user = {}
        # covDLu = {}
        CoverItem = []

        # for i in range(len(cl)):
        #     top += itertools.combinations(cl, i + 1)
        # self.top = len(top)

        # for each user tìm covClu và covDLu dựa trên cover_cl và cover_dl
        for user in self.train_set["users"]:
            cov_user.setdefault(user, set.intersection(*[set(x) for x in set_items if user in x]))
        # for user in self.train_set["users"]:
        #     covDLu.setdefault(user, set.intersection(*[set(x) for x in topDL if user in x]))

        for user in cov_user:
            if list(cov_user[user]) not in CoverItem:
                CoverItem.append(list(cov_user[user]))

        return CoverItem

    def MLM_learn(self):
        # Tinh phu cam sinh
        '''Tam thoi bo
        self.ranking = []
        self.users = self.train_set['users']
        self.items = self.train_set['items']
        for i, item in enumerate(self.items):
            self.item_to_item_id.update({item: i})
            self.item_id_to_item.update({i: item})
        for u, user in enumerate(self.users):
            self.user_to_user_id.update({user: u})
            self.user_id_to_user.update({u: user})
        # read files
        # self.read_files()
        '''
        topCL = self.calculateTopCoverS(self.cl)
        topDL = self.calculateTopCoverS(self.dl)
        CovCl = self.calculateCoverS(topCL)
        CovDl = self.calculateCoverS(topDL)

        for user in self.trainSets["users"]:
            '''Tam thoi bo
            for cov in CovCl:
                self.lis_user_covCl.update(set(cov))
            # NcovCl = UserKNN(train_file, test_file).compute()
            self.init_model()
            for user_id, user in enumerate(self.users):
                neighbors = sorted(range(len(self.su_matrix[user_id])), key=lambda m: -self.su_matrix[user_id][m])
            # Tinh toan nguoi dung tuong tu
            self.predict()
            self.write_ranking()
            '''
            return 1