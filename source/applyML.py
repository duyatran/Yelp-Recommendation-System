import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sklearn
from sklearn import tree
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression


TEST_SIZE = 0.3 # 30% of the input will be used as the testSet
RANDOM_STATE = 0 # random seed

def parseFile(filename):
    dataset = np.loadtxt(filename, delimiter=",")
    data = dataset[:, 0:len(dataset[0]) - 1]
    target = dataset[:, len(dataset[0]) - 1]
    return data,target

def getTrainAndTestSet(data,target):
    global TEST_SIZE
    global RANDOM_STATE
    data, target = sklearn.utils.shuffle(data, target,
                                       random_state = RANDOM_STATE)
    test_size = int(TEST_SIZE * len(data))
    trainData = data[:-test_size]
    trainTarget = target[:-test_size]
    testData = data[-test_size:]
    testTarget = target[-test_size:]

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


def logisticRegression(trainData,trainTarget):
    clf = LogisticRegression()
    clf.fit(trainData,trainTarget)
    return clf


def testOnTestSet(clf,testData,testTarget):
    correct = 0
    fail = 0
    for index in xrange(len(testData)):
        print testData[index].reshape(-1,len(testData[index]))
        prediction = clf.predict(testData[index].reshape(-1,len(testData[index])))
        print prediction,testTarget[index]
        if prediction == testTarget[index]:
            correct += 1
        else:
            fail += 1

    print "correct rate is",(correct*1.0)/(correct+fail)*100,"%"



if __name__ == "__main__":
    data,target = parseFile("input.csv")
    trainData, trainTarget, testData, testTarget = getTrainAndTestSet(data,target)
    clf = decisionTree(trainData,trainTarget)
    linearRegression(trainData,trainTarget)
    clf2 = logisticRegression(trainData,trainTarget)
    clf3 = linearRegression(trainData,trainTarget)
    testOnTestSet(clf2,testData,testTarget)



