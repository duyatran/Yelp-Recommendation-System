import random
import pandas as pd
from surprise import KNNBasic
from surprise import KNNWithMeans
from surprise import KNNBaseline
from surprise import Dataset
from surprise import Reader
from surprise import evaluate, print_perf

my_seed = 1
random.seed(my_seed)

reader = Reader(line_format='user item rating', sep=',')
train_file = '../output/trainData.txt'
test_file = '../output/testData.txt'
data = Dataset.load_from_folds([(train_file, test_file)], reader)

# list of algorithms used
algo_list = []
algo = KNNBasic()

algo_list.append(algo)

# train and test code for one algorithm
for trainset, testset in data.folds(): 
    algo.train(trainset)                             
    predictions = algo.test(testset)

# Evaluate performances of our algorithm on the dataset.
#perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
print_perf(perf)