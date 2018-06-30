import re
from util import convert

# it computes the extended version of jaccard similarity as explained in
# section 4.3 of the paper
# glove_pairwise is the pre-computed 20 nearest neighbours for each word
def match(comment1, comment2): #def match(glove_pairwise, comment1, comment2):
    dirGlovePairwise = '../data/util/'
    preTrainedGlovePairwise = dirGlovePairwise+'glove_pairwise.pickle'
    glove_pairwise = []
    with open(preTrainedGlovePairwise) as fp:
        glove_pairwise.append(fp)

    list1 = re.findall(r"[\w']+", comment1)
    list2 = re.findall(r"[\w']+", comment2)
    modified_list2 = set([word for word in list2 if word in glove_pairwise])
    modified_list1 = set([word for word in list1 if word in glove_pairwise])
    # print modified_list1
    # print modified_list2
    if len(modified_list1) == 0 or len(modified_list2) == 0:
        return 0.0
    intersection = 0.0

    for i in modified_list1:
        for j in modified_list2:
            if j in glove_pairwise[i] or i == j:
                intersection += 0.5
                break

    for i in modified_list2:
        for j in modified_list1:
            if j in glove_pairwise[i] or i == j:
                intersection += 0.5
                break
    union = len(modified_list2) + len(modified_list1) - intersection
    return intersection/union

# for a given 'question' it estimates redundancy of the question by checking
# the maximum of similarity score among all the questions previously asked
def calculate_redundancy(question, questions):
    f = 0.0
    for i in questions:
        # print f
        f = max(match(convert(question['body']), convert(i['body'])), f)
        # f = max(match(convert(question['body']), convert(i['body'])), f)
    return [f]
