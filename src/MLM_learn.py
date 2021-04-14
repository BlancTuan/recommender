import itertools
from os.path import join

from caserec.recommenders.item_recommendation.userknn import UserKNN

from caserec.utils.process_data import ReadFile
from src.process_reducts import process_reduct

# inputFile = "../data/ml-100k/u.data"
inputFile = "../data/jester-data-1/data_learn.data"
test_file = "../data/export/u.test"
train_file = "../data/export/u.train"
output_file = "../results/u.result"

class MLM_learn(UserKNN):
    def __init__(self, cl, dl, alpha = 1):
        self.train_set = ReadFile(inputFile).read()
        self.cl = cl
        self.dl = dl
        self.alpha = alpha
        # super().__init__(inputFile, inputFile, output_file=output_file)
        self.lis_user_covCl = set()
        self.neighbors_user = {}
        self.Label_user = {}
        self.l_user = {}
    # Ham tinh phu dinh
    def calculateTopCoverS(self, set_items):
        coverS = []
        topItem = []


        for i in range(0, len(set_items)):
            combination = list(itertools.combinations(set_items, i + 1))
            for element in combination:
                cover = [user for (user, items) in self.train_set["items_seen_by_user"].items()
                         if
                         set(element).issubset(items)]
                if cover not in coverS and len(cover) > 0:
                    topItem.append(cover)
                coverS.append(cover)
        if self.train_set["users"] not in topItem:
            topItem.append(self.train_set["users"])

        return topItem

    # Ham tim phu cam sinh
    def calculateCoverS(self, set_items):
        cov_user = {}
        CoverItem = []

        # for each user tìm covClu và covDLu dựa trên cover_cl và cover_dl
        for user in self.train_set["users"]:
            cov_user.setdefault(user, set.intersection(*[set(x) for x in set_items if user in x]))

        for user in cov_user:
            if list(cov_user[user]) not in CoverItem:
                CoverItem.append(list(cov_user[user]))

        return CoverItem

    # Ham tinh do tin cay
    def caculatorReliability(self, lu, user):
        user_contains_lu = []
        N_user = {user}
        for cov in self.neighbors_user[user]:
            N_user.update(cov)

        for u in N_user:
            if lu in self.train_set["items_seen_by_user"][u]:
                user_contains_lu.append(u)
        reliability = len(user_contains_lu)/len(self.neighbors_user[user])

        return reliability

    def MLM_learn(self):
        # Tim phu dinh cua CL va DL

        topCL = self.calculateTopCoverS(self.cl)
        topDL = self.calculateTopCoverS(self.dl)

        # Tinh phu cam sinh CL va DL
        CovCl = self.calculateCoverS(topCL)
        CovDl = self.calculateCoverS(topDL)

        for user in self.train_set["users"]:
            neighbors_user_cl = set()
            neighbors_user_dl = set()
            self.neighbors_user.setdefault(user,[])
            self.Label_user[user] = set()
            self.l_user[user] = set()

            # Buoc 5 thuat toan
            # Tim dan lang gieng gan cua user trong CovCl va CovDl
            for neighbors_Cl in CovCl:
                for neighbors_Dl in CovDl:
                    if user in neighbors_Cl and user in neighbors_Dl:
                        self.neighbors_user[user].append(set(neighbors_Cl) & set(neighbors_Dl))

            # Buoc 6 thuat toan

            for cov in self.neighbors_user[user]:
                item_seem_by_cov = set()
                for u in list(cov):
                    # Neu la lay cac muc lan dau
                    if len(item_seem_by_cov) == 0:
                        item_seem_by_cov.update(self.train_set["items_seen_by_user"][u])
                    else:
                        item_seem_by_cov.update(item_seem_by_cov & self.train_set["items_seen_by_user"][u])

                self.Label_user[user].update(item_seem_by_cov)

            # Buoc 7 thuat toan
            # Mai lam
            for lu in self.Label_user[user]:
                if(self.caculatorReliability(lu, user) > self.alpha):
                    self.l_user[user].update(set([lu]))
        # End for tra ve mo hinh phan lop
        return self.l_user


