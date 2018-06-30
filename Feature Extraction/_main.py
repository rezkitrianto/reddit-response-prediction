#!/usr/bin/python

import json
from pprint import pprint
from array import array
from temporal_features import get_temporal_featuers
from redundancy_features import calculate_redundancy
from user_features import getUserFeature
from syntax_features import get_all_syntax_features
from politeness_score import get_politeness_score

def loadData(dir):

    fileName = dir+'actor/t3_1glx04'
    with open(fileName) as f:

        contentJson = f.readlines()
        j = json.loads('{"c": 0, "b": 0, "a": 0}')
        # pprint(j)


    # return data

def extractLibSVMFeature(allData, data, i):  #extract features per-row
    if(data['reply'] == 'None'):
        groundTruth = '0'
    else:
        groundTruth = '1'

    #call length feature
    sentence = data['body'] #create dummy sentence
    words = sentence.split()
    orthogonalFeature = len(words) #done
    orthogonalFeatureLength = 1
    # print "orthogonal Feature :"
    # print orthogonalFeature

    #call temporal feature
    temporalFeature = get_temporal_featuers(data, 3, 1371587693, 1371592791, 1)  #get_temporal_featuers(data, index_data, start_response_time, stop_response_time, top_score_response_index): #get the required data
    temporalFeatureLength = len(temporalFeature)
    # print "temporal Feature"
    # print temporalFeature

    #call syntactic feature
    syntacticFeature = get_all_syntax_features('t3_1glx04', 't1_calggch', 'actor') #question_link, question_name, tag
    syntacticFeatureLength = len(syntacticFeature)
    # print "syntactic feature : "
    # print syntacticFeature

    #call politeness feature
    # politenessFeature = array(0)
    # politenessFeature = get_politeness_score(data) #struktur input data masih salah
    # politenessFeatureLength = len(politenessFeature)

    #call redundancy feature
    # forumFeature = calculate_redundancy(data,allData) #
    # forumFeatureLength = len(forumFeature)
    # print forumFeature

    #call user feature
    userFeature = getUserFeature(data['author']) #done
    userFeatureLength = len(userFeature)

    feature = ''
    i = 1
    feature += groundTruth + ' '

    for j in range(0, orthogonalFeatureLength):
        feature += str(i) + ':' + str(orthogonalFeature) + ' '
        i = i + 1

    for k in range(0, temporalFeatureLength):
        feature += str(i) + ':' + str(temporalFeature[k]) + ' '
        i = i + 1

    # for l in range(0, politenessFeatureLength):
    #     feature += i + ':' + politenessFeature[l] + ' '

    # for m in range(0, forumFeatureLength):
    #     feature += str(i) + ':' + str(forumFeature[m]) + ' '
    #     i = i + 1

    for n in range(0, syntacticFeatureLength):
        feature += str(i) + ':' + str(syntacticFeature[n]) + ' '
        i = i + 1

    for n in range(0, userFeatureLength):
        feature += str(i) + ':' + str(userFeature[n]) + ' '
        i = i + 1

    feature = feature.strip()


    return feature

def callSemanticFeature():
    semanticFeature = array(0)
    return semanticFeature


dir = '../data/'
fileName = dir+'actor/t3_1glx04'
i = 0
allData = []
with open(fileName) as fp:
    for contentJson in fp:
        cjson = ''.join(contentJson)
        cjson.replace("'", "\'")
        eachData = json.loads(cjson)
        allData.append(eachData)

# print allData[2]

with open(fileName) as fp:
    myfile = open('xyz3.txt', 'w')
    for contentJson in fp:
        i = i + 1
        cjson = ''.join(contentJson)
        cjson.replace("'", "\'")
        data = json.loads(cjson)
        # if(i == 1):
        #     # print(data)
        #     feature = extractLibSVMFeature(allData, data, i)
        #     print feature
        #print data
        feature = extractLibSVMFeature(allData, data, i)
        myfile.write("%s\n" % feature)
        print feature
        #For temporal feature
        #get_start_time_of_all_response
        #get_end_time_of_all_response
        #get_top_scored_index

    myfile.close()