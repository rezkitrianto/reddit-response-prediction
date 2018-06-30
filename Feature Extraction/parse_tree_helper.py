import xml
import xml.dom.minidom


ROOT_DIRECTORY = "../data/XML-dumps/"


def get_xml_file(link_id, name, tag):
    # example : tag : actor ; link_id : t3_1glx04  name : t1_calgfwf.xml
    # filepath = ROOT_DIRECTORY + "/" + tag + "_xml" + tag + "_" + \
    #     link_id + "/" + name + ".xml"
    filepath = ROOT_DIRECTORY + "" + tag + "_xml/" + tag + "_" + \
        link_id + "/" + name + ".xml"
    # print filepath
    filepath.replace("//", "/")
    try:
        f = open(filepath, 'r')
        xmldata = f.read()
        return xmldata
    except Exception, e:
        print "Can't open", e, link_id, name
        return None


def xml_parse_coref_result(xmldata):
    try:
        xmldoc = xml.dom.minidom.parseString(xmldata.encode('utf-8'))
        sentences = xmldoc.getElementsByTagName('sentences')[0]
        return sentences
    except Exception, e:
        print "error: ", e
        return None


def get_dependency_and_tokenlist(link_id, name, tag):
    sentences = xml_parse_coref_result(get_xml_file(link_id, name, tag))
    if sentences is None:
        return None, None
    dependencies = []
    tokens = []

    for i in sentences.getElementsByTagName('sentence'):
        # extracting basic-dependency for all sentences
        dependencies.append(i.getElementsByTagName('dependencies')[0])
        tokens.append(i.getElementsByTagName('tokens')[0])

    dependencies_list = []
    for sd in dependencies:
        dep_list = sd.getElementsByTagName('dep')

        ret_list = []
        for dep in dep_list:
            dep_type = dep.getAttribute('type')
            dependent_data = dep.getElementsByTagName('dependent')[0]
            dependent_id = int(dependent_data.getAttribute('idx'))
            dependent = str(dependent_data.firstChild.data)
            # print dependent,"==>",dependent_id, "==>",dep_type
            governor_data = dep.getElementsByTagName('governor')[0]
            governor_id = int(governor_data.getAttribute("idx"))
            governor = str(governor_data.firstChild.data)
            # print governor,"-->" , governor_id
            #ret = str(dep_type) + "(" + governor + "-" + str(governor_id) + ", " + dependent + "-" + str(dependent_id) + ")"
            ret_list.append((dep_type, (governor, governor_id), (dependent, dependent_id)))
        dependencies_list.append(ret_list)
    return dependencies_list, tokens


def calculate_depth(adj_list, start_node):
    depth = 0
    if(start_node not in adj_list):return 0
    for node in adj_list[start_node]:
        depth=max(depth, calculate_depth(adj_list,node) + 1 )
    return depth


def create_adjacency_list(dep_graph):
    adj_list = {}
    for i in dep_graph:
        if i[1][1] not in adj_list:
            adj_list[i[1][1]] = [i[2][1]]
        else:
            adj_list[i[1][1]].append(i[2][1])
    return adj_list


def depth_of_dependency_tree(link_id, name, tag):
    dependencies_list, tokens = get_dependency_and_tokenlist(link_id, name, tag)
    depth_list = []
    if dependencies_list is None:
        return depth_list
    for dep_graph in dependencies_list:
        adj_list = create_adjacency_list(dep_graph)
        d = calculate_depth(adj_list, 0)  # assuming root node is always zero
        # print "depth : ",d
        depth_list.append(d)
    # print "dependency list ", depth_list
    return depth_list



def get_verb_phrase_indices(token_list):
    allowed_vp = set(['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])
    vp_indices = []
    for token in token_list:
        pos = token.getElementsByTagName('POS')
        if str(pos[0].firstChild.nodeValue) in allowed_vp:
            vp_indices.append(int(str(token.getAttribute('id'))))
    return vp_indices



# returns [[dephts of VPs in sentence 1], [depths of VPs in sentence2]..]
def depth_of_verb_phrase(link_id, name, tag):
    dependencies_list, tokens = get_dependency_and_tokenlist(link_id, name, tag)
    if tokens is None or dependencies_list is None:
        return [[]]
    assert len(tokens) == len(dependencies_list)
    ret_list = []
    for i in range(len(dependencies_list)):
        depth_verb_phrases = []
        adj_list = create_adjacency_list(dependencies_list[i])
        verb_phrases_indices = get_verb_phrase_indices(
            tokens[i].getElementsByTagName('token'))
        for j in verb_phrases_indices:
            depth_verb_phrases.append(calculate_depth(adj_list, j))
        ret_list.append(depth_verb_phrases)
    # print "Verb Phrase list", ret_list
    return ret_list
