from math import *

from Tools.scripts.make_ctype import values
from caserec.utils.process_data import ReadFile
from caserec.recommenders.item_recommendation.userknn import UserKNN

inputFile = "../data/jester-data-1/data_test.data"

class MLM_classifier(UserKNN):
    def __init__(self, Classification, u_recommender, train_set_user_learn):
        self.item_to_item_id = {}
        self.item_id_to_item = {}
        self.user_to_user_id = {}
        self.user_id_to_user = {}
        self.train_set_test = ReadFile(inputFile).read()
        self.Classification = Classification
        self.u_recommender = u_recommender
        self.train_set = train_set_user_learn
        self.users = self.train_set['users']
        self.items = set(self.train_set['items'])

    def MLM_classifier(self):
        similar = []
        lable_user_test = {}

        self.users.append(self.u_recommender)
        self.items.update(self.train_set_test['items_seen_by_user'][self.u_recommender])
        self.train_set['feedback'].setdefault(self.u_recommender,self.train_set_test['feedback'][self.u_recommender])
        for i, item in enumerate(self.items):
            self.item_to_item_id.update({item: i})
            self.item_id_to_item.update({i: item})
        for u, user in enumerate(self.users):
            self.user_to_user_id.update({user: u})
            self.user_id_to_user.update({u: user})

        self.create_matrix()

        for u, user in enumerate(self.users):
            feedbackUserTest = list(self.matrix[len(self.users)-1])
            feedbackA = list(self.matrix[u])
            similar.append(self.euclid_distance(feedbackUserTest, feedbackA))

        similar.remove(0.0)
        user_id = similar.index(min(similar))

        user = self.users[user_id]
        lable_user_test.setdefault(user, self.Classification[user])

        return lable_user_test

    def euclid_distance(self, x, y):
        return sqrt(sum(pow(a-b,2) for a,b in zip(x,y)))
