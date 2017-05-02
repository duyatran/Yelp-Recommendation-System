import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sklearn
from sklearn import tree
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
import csv
import sys


TEST_SIZE = 0.3 # 30% of the input will be used as the testSet
RANDOM_STATE = 0 # random seed

testMap = []


def parseFile(filename):
    dataset = np.loadtxt(filename, delimiter=",",skiprows=1)
    data = dataset[0:, 0:len(dataset[0]) - 1]#split data between attributes and like?
    target = dataset[0:, len(dataset[0]) - 1]
    return data,target

def getTrainAndTestSet(data,target):
    global TEST_SIZE
    global RANDOM_STATE
    global testMap
    data, target = sklearn.utils.shuffle(data, target,
                                       random_state = RANDOM_STATE)
    with open('test.csv', 'wt') as test_output, open('train.csv', 'wt') as train_output:
        testWriter = csv.writer(test_output,delimiter=',')
        trainWriter = csv.writer(train_output, delimiter=',')
        test_size = int(TEST_SIZE * len(data))
        trainData = data[:-test_size]
        trainData = trainData[0:,1:len(trainData[0]) - 1]#exclude the first column which is businessID
        trainTarget = target[:-test_size]
        testData = data[-test_size:]
        testMap = testData[0:, 0]#testMap records the name of businessID
        testData = testData[0:,1:len(testData[0]) - 1]
        testTarget = target[-test_size:]
        #index = 0 #write files out
        # for data in trainData:
        #     temp = []
        #     for entry in data:
        #         temp.append(entry)
        #     temp.append(trainTarget[index])
        #     index += 1
        #     trainWriter.writerow((temp))
        # index = 0
        # for data in testData:
        #     temp = []
        #     for entry in data:
        #         temp.append(entry)
        #     temp.append(testTarget[index])
        #     index += 1
        #     testWriter.writerow((temp))


    return trainData,trainTarget,testData,testTarget

def decisionTree(trainData,trainTarget):
    clf = tree.DecisionTreeClassifier()
    clf.fit(trainData, trainTarget)
    return clf

def linearRegression(trainData,trainTarget):
    clf = LinearRegression()
    clf.fit(trainData,trainTarget)
    #clf.score(trainData,trainTarget)
    return clf

def naiveBayes(trainData,trainTarget):
    clf = GaussianNB()
    clf.fit(trainData,trainTarget)
    return clf

def logisticRegression(trainData,trainTarget):
    clf = LogisticRegression()
    clf.fit(trainData,trainTarget)
    return clf


def testOnTestSet(clf,testData,testTarget):
    correct = 0
    fail = 0
    result = []
    global testMap
    for index in xrange(len(testData)):
        # print testData[index].reshape(-1,len(testData[index]))
        prediction = clf.predict(testData[index].reshape(-1,len(testData[index])))
        # print prediction,testTarget[index]
        if prediction == testTarget[index]:
            correct += 1
            result.append(int(testMap[index]))
        else:
            fail += 1
    print "correct rate is",(correct*1.0)/(correct+fail)*100,"%"
    return result




if __name__ == "__main__":
    fileName = sys.argv[1]
    data,target = parseFile(fileName)
    # data, target = parseFile("input.csv")
    trainData, trainTarget, testData, testTarget = getTrainAndTestSet(data,target)
    clf = decisionTree(trainData,trainTarget)
    # linearRegression(trainData,trainTarget)
    clf2 = logisticRegression(trainData,trainTarget)
    # clf3 = linearRegression(trainData,trainTarget)
    clf4 = naiveBayes(trainData,trainTarget)
    print clf4.score(testData, testTarget)
    # print "for decision tree train", testOnTestSet(clf, trainData, trainTarget)
    print "for decision tree", testOnTestSet(clf,testData,testTarget)
    print "for logistic regression",testOnTestSet(clf2,testData,testTarget)
    # print "for logistic regression train", testOnTestSet(clf2, trainData, trainTarget)
    print "for naive bayes", testOnTestSet(clf4, testData, testTarget)
    # print "for naive bayes train", testOnTestSet(clf4, trainData, trainTarget)
    # print testMap




