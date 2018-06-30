#!/usr/bin/python

import json
from pprint import pprint
from array import array
from temporal_features import get_temporal_featuers
from redundancy_features import calculate_redundancy
from user_features import getUserFeature
from syntax_features import get_all_syntax_features
from politeness_score import get_politeness_score
from os import listdir
from os.path import isfile, join
import operator
import time


def extractLibSVMFeature(topic, allData, data, temporalParameters):  # extract features per-row
    if (data['reply'] == 'None'):
        groundTruth = '0'
    else:
        groundTruth = '1'

    # call length feature
    sentence = data['body']  # create dummy sentence
    words = sentence.split()
    orthogonalFeature = len(words)  # done
    orthogonalFeatureLength = 1
    # print "orthogonal Feature :"
    # print orthogonalFeature

    # call temporal feature
    # temporalParameters = [k, firstTime, lastTime, index, eachData[index]['createdutc'])
    temporalFeature = get_temporal_featuers(data, temporalParameters[0], temporalParameters[1], temporalParameters[2],temporalParameters[3])  # get_temporal_featuers(data, index_data, start_response_time, stop_response_time, top_score_response_index): #get the required data
    # temporalParameters = [k, firstTime, lastTime, index, allData[index]['created_utc']]
    temporalFeatureLength = len(temporalFeature)
    # print "temporal Feature"
    # print temporalFeature

    # call syntactic feature
    syntacticFeature = get_all_syntax_features(data["parent_id"], data["name"], topic)  # question_link : per-quesiton-link, question_name : data["name"], tag : per topic
    syntacticFeatureLength = len(syntacticFeature)
    # print "syntactic feature : "
    # print syntacticFeature

    # call politeness feature
    # politenessFeature = array(0)
    politenessFeature = get_politeness_score(data) #struktur input data masih salah
    politenessFeatureLength = len(politenessFeature)
    # print "Politeness Feature"
    # print politenessFeatureLength
    # print politenessFeature

    # call redundancy feature
    forumFeature = calculate_redundancy(data,allData) #
    forumFeatureLength = len(forumFeature)
    # print "forum feature : "
    #
    # print forumFeature

    # call user feature
    userFeature = getUserFeature(data['author'])  # done
    userFeatureLength = len(userFeature)

    feature = ''
    i = 1
    feature += groundTruth + ' '

    for m in range(0, forumFeatureLength):
        feature += str(i) + ':' + str(forumFeature[m]) + ' '
        i = i + 1

    for j in range(0, orthogonalFeatureLength):
        feature += str(i) + ':' + str(orthogonalFeature) + ' '
        i = i + 1

    for k in range(0, temporalFeatureLength):
        feature += str(i) + ':' + str(temporalFeature[k]) + ' '
        i = i + 1

    for n in range(0, syntacticFeatureLength):
        feature += str(i) + ':' + str(syntacticFeature[n]) + ' '
        i = i + 1

    for n in range(0, userFeatureLength):
        feature += str(i) + ':' + str(userFeature[n]) + ' '
        i = i + 1

    for l in range(0, politenessFeatureLength):
        feature += str(i) + ':' + str(politenessFeature[l]) + ' '

    feature = feature.strip()

    return feature


# topics = ['actor', 'author', 'director', 'politics']
topics = ['actor']

dir = '../data/'  # fixed
for i in range(0, len(topics)):
    mypath = dir + topics[i]
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    for j in range(0, len(onlyfiles)):
        fileName = dir + topics[i] + "/" + onlyfiles[j]
        print fileName
        k = 0
        allData = []
        allTime = []
        allScore = []
        with open(fileName) as fp:
            for contentJson in fp:
                cjson = ''.join(contentJson)
                cjson.replace("'", "\'")
                eachData = json.loads(cjson)
                # write all data in a file to calculate the forum factor
                allData.append(eachData)
                allTime.append(eachData['created_utc'])  # for the start time, using the smallest value of utc time; vice versa; for the end time, using the largest value of the utc time
                allScore.append(eachData['score'])

                # get the start time of all response

        with open(fileName) as fp:
            outputFileName = topics[i] + '5.txt'
            myfile = open(outputFileName, 'a')
            for contentJson in fp:
                k = k + 1
                cjson = ''.join(contentJson)
                cjson.replace("'", "\'")
                data = json.loads(cjson)

                lastTime = max(allTime)
                firstTime = min(allTime)

                index, value = max(enumerate(allScore), key=operator.itemgetter(1))
                # print allData[index]['created_utc']
                temporalParameters = [k, firstTime, lastTime, index+1, allData[index]['created_utc']]
                feature = extractLibSVMFeature(topics[i], allData, data, temporalParameters)
                myfile.write("%s\n" % feature)
                print feature
                time.sleep(0.5)

            myfile.close()