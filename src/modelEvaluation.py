from caserec.evaluation.item_recommendation import ItemRecommendationEvaluation

predictions_file = '../results/u.result'
test_file = '../'

class modelEvaluation():
    def __init__(self, recommen):
        self.recommen = recommen

    ItemRecommendationEvaluation().evaluate_with_files(predictions_file, test_file)

