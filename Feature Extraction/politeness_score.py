from politeness.polite_inquiry import get_politeness

def get_politeness_score(comment):
    return [get_politeness(comment['body'])]
