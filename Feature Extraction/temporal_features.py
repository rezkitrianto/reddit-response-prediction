# computes the temporal features
# start_time : start time of the iama (time of the first question)
# end_time : end time of the iama (time of the last question)
# length : top level questions asked in the iama
def get_temporal_featuers(comment, comment_index, start_time, end_time, length):

    q_time = long(comment['created_utc'])  # asking time of the question
    # print start_time
    # print end_time
    # print q_time
    time_feature_1 = (1.0 * (float(q_time) - float(start_time)))/(float(end_time) - float(start_time))
    time_feature_2 = float(comment_index)/length
    return [time_feature_1, time_feature_2]