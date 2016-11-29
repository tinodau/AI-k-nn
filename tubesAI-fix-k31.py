import csv
import random
import math
import operator
import copy

# GLOBAL VARIABLE
trainingSet = [] # set of training data
testSet     = [] # set of testing data
prediction  = [] # list of result prediction

dataTestSet = []
testAnswer  = []

jawaban     = []

k           = 31  # TOTAL OF NEIGHBORS (best 13 to 21)
trainingFile= 'Train.csv' # cobatraining.csv
testingFile = 'Test.csv'
split       = 1 # BEST 65


def readTrain(training, test):
    """Load Data from given file"""

    with open (trainingFile, 'rb') as csvfile:
        datalist    = csv.reader(csvfile)   #load data from file
        next(datalist, None)
        dataset     = list(datalist)        #put data to var dataset

        for y in range(len(dataset)) :
            inp = []  # put data in line to this variable

            for x in range(1, 12) :
            # x per line is from data #2 to #12 (whitout index)
                inp.append(float(dataset[y][x]))

            if random.random() < split :
                # trainingSet set for 150 lines
                training.append(inp)
            else :
                # testingSet set from line 151 to 200
                test.append(inp)

        print 'Trainingset    = ' + str(len(training))

        # print ('data = {0} \n').format(test)

def readTest(dataTestSet) :
    """ Load Data from testfile """
    with open (testingFile, 'rb') as csvfile:
        dataTestList    = csv.reader(csvfile)
        next(dataTestList, None)
        dataSetTest     = list(dataTestList)
        for y in range(len(dataSetTest)) :
            inp = []

            # print dataSetTest[y]
            for x in range(1, 11) :
                inp.append(float(dataSetTest[y][x]))

            # if random.random() > 0 :
            dataTestSet.append(inp)

            # print dataTestSet[y]
    # print dataTestSet

    print 'Testset        = ' + str(len(dataTestSet)) + '\n'
    return dataTestSet

def normalize(training, test):
    """ Normalize data to [0,1] only (Binary classification) """

    for i in range(len(training)) :
    # NORMALIZING FOR TRAININGSET
        training[i] = (training[i] - min(training)) / (max(training) - min(training))

    for j in range(len(test)) :
    # NORMALIZING FOR TESTSET
        test[j] = (test[j] - min(test)) / (max(test) - min(test))

    # return training, test


def euclidean(training, test, length):
    """ Calculate euclidean distance per line (training) """

    total = 0
    # normalize(training, test)

    for i in range(length):
        # calculate sum for euclidean per line in trainingSet
		total += pow((float(training[i]) - float(test[i])), 2)

    return math.sqrt(total)
    # returning sqrt from sum(i)  above


def getRanking (training, test, k) :
    """ Ranking for nearest node """

    rank    = []                #PUT LIST OF RANK HERE
    lengthX = len(test) - 1     #PUT DATA #1 TO #11 (WHITOUT RESULT Y)

    for x in range(len(training)) :
        # calculate rank per line for train-test
        startrank   = euclidean(test, training[x], lengthX)
        rank.append((training[x], startrank))

    rank.sort(key=operator.itemgetter(1))   #SORTING RANK
    ranking = []                            #PUT CHOOSEN (#1) RANK HERE

    for y in range(k) :
        ranking.append(rank[y][0])
        #CHOOSE RANK NUMBER 1

    return ranking
    #RETURN RANK NUMBER 1

def voting(ranking):
    """ RETURN MOST VOTED - FOR RESULT """

    majorvote    = {}
    # PUT test
    for y in range(len(ranking)) :
    # RANK FROM 1 TO 3
        vote    = ranking[y][-1]
        # RESTART RANK IN LINE (Y) FROM 0

        if vote in majorvote :
            majorvote[vote] +=  1
            #  PLUS 1 IF VOTE IS IN MAJORVOTE
        else :
            majorvote[vote] =   1

    sortingvote = sorted(majorvote.iteritems(), key=operator.itemgetter(1), reverse=True)
    # SORTING MOST VOTED
    return sortingvote[0][0]


# def getResult(training, test, prediction, k):
#     """ RETURN LIST F RESULT """
#
#     for i in range(len(test)) :
#         ranking = getRanking(training, test[i], k)
#         vote  = voting(ranking)
#
#         prediction.append(vote)
#         print str(testSet[i]) + ' ==> ' + str(prediction[i])

    # print # ENTERING SPACE

def getResultTest (trainingnya, dataTestSet,  testAnswer, k) :
    trainingFilenya = readTrain(trainingSet, testSet)
    testFilenya = readTest(dataTestSet)

    # print testFilenya
    # testAnswer.insert(0, "START TESTING")
    for i in range(len(testFilenya)) :
        ranking = getRanking(trainingnya,  testFilenya[i], k)
        vote    = voting(ranking)
        print(i, testFilenya[i])
        testAnswer.append(vote)

    tmp = copy.copy(testFilenya)

    for jawab in range(len(testFilenya)) :
        tmp[jawab].append(testAnswer[jawab])
        jawaban.append(tmp[jawab])

    with open("K-" + str(k) +".csv", "wb") as startTest:
        writer = csv.writer(startTest)
        writer.writerow(["x1", "x2", "x3" , "x4", "x5", "x6", "x7", "x8", "x9", "x10", "y"])
        for row in range(len(testFilenya)) :
            writer.writerow(jawaban[row])
        startTest.close()

def accuration(test, prediction):
    """ RETURN PERSENTAGE OF ACCURATION """

    correct = 0     # SET TOTAL OF CORRECT FROM 0
    for y in range(len(test)) :
    # LISTING LINES
        if test[y][-1] == prediction[y]:
            correct += 1

    # print ('data = {0}').format(prediction)
    print 'Accuration = '+ str((correct / float (len(test))) * 100.0) + '%'
    # print correct
    # RETURN PERSENTAGE OF CORRECT RESULT


def main():
    """ MAIN FUNCTION """
    # readTrain(trainingSet, testSet)                  # READ DATA
    # getResult(trainingSet, testSet, prediction, k)  # GET RESULT

    # readTest(dataTestSet)
    # print readTest(dataTestSet)
    dataTraining = []
    getResultTest(trainingSet, dataTestSet, testAnswer, k)

    # accuration(testSet, prediction)                 # GET ACCURATION

main()
