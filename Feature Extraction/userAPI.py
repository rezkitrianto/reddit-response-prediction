import time
import praw

reddit_client = praw.Reddit(user_agent='my amazing cake day bot')

def get_my_cake_day(username):
    redditor = reddit_client.get_redditor(username)
    return time.strftime("%D", time.gmtime(redditor.created_utc))


get_my_cake_day('test')