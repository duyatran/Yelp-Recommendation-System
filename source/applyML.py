import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import sklearn
from sklearn import tree
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import csv
import sys
import macros as m
from numpy import array


TEST_SIZE = 0.3 # 30% of the input will be used as the testSet
RANDOM_STATE = 0 # random seed

testMap = []


def parseFile(filename):
    dataset = np.loadtxt(filename, delimiter=",",skiprows=1)
    data = dataset[0:, 0:len(dataset[0]) - 1]#split data between attributes and like?
    target = dataset[0:, len(dataset[0]) - 1]
    return data,target

def getTrainAndTestSet(data,target):#for my own test purpose, n
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
    pred = []
    for index in xrange(len(testData)):
        # print testData[index].reshape(-1,len(testData[index]))
        prediction = clf.predict(testData[index].reshape(-1,len(testData[index])))
        pred.append(prediction)
        # print prediction,testTarget[index]
        if prediction == testTarget[index]:
            correct += 1
            # result.append(int(testMap[index]))
        else:
            fail += 1
    return pred,(correct*1.0)/(correct+fail)*100

def parsePotentials(filename):
    dataset = np.loadtxt(filename, delimiter=",",skiprows=1)
    data = dataset[0:, 0:len(dataset[0])]
    return data

def getPotentialRecommendation(clf,data,busName):
    result = []
    for index in xrange(len(data)):
        prediction = clf.predict(data[index].reshape(-1,len(data[index])))
        if prediction == 1:
            result.append(str(busName[index]))
    return result

def run(user_fname):
    with open(user_fname, 'rb') as users:
        content = users.readlines()
        content = [x.strip() for x in content]
        with open(m.out_dir_results+"/original_accuracy.csv", 'wt') as output, open(m.out_dir_results+"/original_precision_recall.csv",'wt') as precOutput:
            writer = csv.writer(output, delimiter=',')
            precWriter = csv.writer(precOutput,delimiter=',')
            writer.writerow(('username', 'Decision Tree', 'Logistic Regression', 'Naive Bayes','MAX'))
            precWriter.writerow(('username','DT_precision','DT_recall','LR_precision','LR_recall','NB_precision','NB_recall'))
            print "check"
            for user in content:
                trainData,trainTarget = parseFile(m.out_dir_original+"/att_cat_"+user+"_train.txt")
                testData,testTarget = parseFile(m.out_dir_original+"/att_cat_"+user+"_test.txt")
                clfDT = decisionTree(trainData,trainTarget)
                clfLR = logisticRegression(trainData,trainTarget)
                clfNB = naiveBayes(trainData,trainTarget)
                print "finished running models for the user ()"+user
                predDT,DTAccur = testOnTestSet(clfDT,testData,testTarget)
                predLR,LRfAccur = testOnTestSet(clfLR, testData, testTarget)
                predNB,NBAccur = testOnTestSet(clfNB, testData, testTarget)

                DTprec = precision_score(predDT,testTarget)
                LRprec = precision_score(predLR, testTarget)
                NBprec = precision_score(predNB, testTarget)

                DTrecall = recall_score(predDT, testTarget)
                LRrecall = recall_score(predLR, testTarget)
                NBrecall = recall_score(predNB, testTarget)

                writer.writerow((user,DTAccur,LRfAccur,NBAccur,max(DTAccur,LRfAccur,NBAccur)))
                precWriter.writerow((user,DTprec,DTrecall,LRprec,LRrecall,NBprec,NBrecall))
                print "finished writing "+user+" into accuracy and precision_recall files"
                maxAccur = max(DTAccur,LRfAccur,NBAccur)
                finalCLF = None
                if DTAccur == maxAccur:
                    finalCLF = clfDT
                elif LRfAccur == maxAccur:
                    finalCLF = clfLR
                else:
                    finalCLF = clfNB
                with open(m.out_dir_results+"/original_result_"+user+".txt",'wt') as recomOutput, open(m.out_dir_potential+"/pot_bus_"+user+".txt",'rd') as potentials:
                    recomWriter = csv.DictWriter(recomOutput, ['bus_id'])
                    recomWriter.writeheader()
                    potentialReader = csv.reader(potentials, delimiter=',')
                    potentialReader.next()
                    for row in potentialReader:
                        # prediction = finalCLF.predict(row[1:].reshape(-1,len(row[1:])))
                        data = [int(x) for x in row[1:]]
                        npData = array(data)
                        prediction = finalCLF.predict(npData.reshape(-1,len(npData)))
                        if prediction == 1:
                            recomWriter.writerow({'bus_id':str(row[0])})
                    # dataset = np.genfromtxt(m.out_dir_potential+"/pot_bus_"+user+".txt", delimiter=",")
                    # data = dataset[1:, 1:len(dataset[0])]
                    # busNames = dataset[1:,0]
                    # result = getPotentialRecommendation(finalCLF,data,busNames)
                    # for bus in result:
                    #     recomWriter.writerow((bus))
                print "finished writing "+user+"\'s recommendation list"


if __name__ == "__main__":
    pass
    # fileName = sys.argv[1]
    # data,target = parseFile(fileName)
    # trainData, trainTarget, testData, testTarget = getTrainAndTestSet(data,target)
    # #potentials = parsePotentials()
    #
    # clf = decisionTree(trainData,trainTarget)
    # clf2 = logisticRegression(trainData,trainTarget)
    # clf4 = naiveBayes(trainData,trainTarget)
    #
    # DTRecomList,DTpred,DTCorrect = testOnTestSet(clf,testData,testTarget)
    # LRRecomList,LRpred,LRCorrect = testOnTestSet(clf2, testData, testTarget)
    # NBRecomList,NBpred,NBCorrect = testOnTestSet(clf4, testData, testTarget)
    #
    # print "recall for LR ",recall_score(LRpred,testTarget)
    # print "precision for LR ",precision_score(LRpred,testTarget)
    # print "for decision tree the correct rate is ", DTCorrect
    # print "for logistic regression the correct rate is", LRCorrect
    # print "for naive bayes the correct rate is ", NBCorrect
    # print "for logistic regression train", testOnTestSet(clf2, trainData, trainTarget)
    # print "for naive bayes train", testOnTestSet(clf4, trainData, trainTarget)
    # print testMap




