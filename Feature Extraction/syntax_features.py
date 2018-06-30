import numpy as np
from parse_tree_helper import depth_of_dependency_tree
from parse_tree_helper import depth_of_verb_phrase



# the tree is of the following structure
# input = [[dephts of VPs in sentence 1], [depths of VPs in sentence2]..]
def get_vp_parse_tree_features(tree):
    if is_all_empty(tree):
        return [0 for i in range(9)]
    appended_version = [j for k in tree for j in k]
    features = []
    features.append(len(appended_version))
    features.append(max(appended_version))
    features.append(min(appended_version))
    features.append(np.mean(appended_version))
    max_len = max([len(e) for e in tree])
    min_len = min([len(e) for e in tree])
    avg_len = np.mean([len(e) for e in tree])
    avg_max = np.mean([max(e) for e in tree if len(e) > 0])
    avg_min = np.mean([min(e) for e in tree if len(e) > 0])
    features.append(max_len)
    features.append(min_len)
    features.append(avg_len)
    features.append(avg_max)
    features.append(avg_min)
    return features


# input = [[dephts of VPs in sentence 1], [depths of VPs in sentence2]..]
def is_all_empty(l):
    for i in l:
        if len(i) > 0:
            return False
    return True


# tree is a list of the depths of different sentences
def get_parse_tree_features(tree):
    if len(tree) == 0:
        return [0 for i in range(4)]
    features = []
    # num of sentences
    features.append(len(tree))
    # depth of the deepest sentence
    features.append(max(tree))
    # depth of the most shallow tree
    features.append(min(tree))
    # mean depth of sentences
    features.append(np.mean(tree))

    return features


# it computes some features based on the ratio of the properties of parse tree
# of the entire sentence with just the parse tree of the verb phrase
def get_ratio_featuers(parse_tree, vp_tree):
    ratio = []
    features = []
    try:
        assert len(parse_tree) == len(vp_tree)
        for i in range(len(vp_tree)):
            if len(vp_tree[i]) == 0 or parse_tree[i] == 0:
                ratio.append(0.0)
            else:
                ratio.append(max(vp_tree[i])/float(parse_tree[i]))
        if len(ratio) == 0:
            return [0.0 for i in range(3)]
        features.append(max(ratio))
        features.append(min(ratio))
        features.append(np.mean(ratio))
        return features
    except Exception, e:
        print e
        return [0.0 for i in range(3)]


# it requires a question instead of just the text
# as the parse trees are stored based on question name
# and link_id
def get_all_syntax_features(question_link, question_name, tag):
    dep_parse_tree = depth_of_dependency_tree(question_link,
                                           question_name, tag)
    vp_parse_tree = depth_of_verb_phrase(question_link,
                                   question_name, tag)
    # print dep_parse_tree
    # print vp_parse_tree
    # print dep_parse_tree, vp_parse_tree
    features = []
    parse_tree_features = get_parse_tree_features(dep_parse_tree)
    vp_parse_tree_features = get_vp_parse_tree_features(vp_parse_tree)
    ratio_features = get_ratio_featuers(dep_parse_tree, vp_parse_tree)
    features.append(parse_tree_features)
    features.append(vp_parse_tree_features)
    features.append(ratio_features)
    ret_list = []

    # print features
    for i in features:
        for j in i:
            ret_list.append(j)
    return ret_list

def get_all_syntax_features2(question_link, question_name, tag):
    print 'a'
    return [0]