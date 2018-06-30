import requests
import json

def getUserFeature(username):
    # r = requests.get('https://www.reddit.com/user/'+username+'/about.json', headers={'User-agent': 'Chrome'})
    r = requests.get('https://www.reddit.com/user/' + username + '/about.json', headers={'User-agent': username})
    if not r:
		return [0,0]
    userData = json.loads(r.text)
    # print userData
    if not userData:
        return [0,0]
    elif(userData.has_key("error")):
        return [0,0]
    elif (userData['data'].has_key("is_suspended")):
        return [0,0]
    else:
        return [userData['data']['link_karma'], userData['data']['comment_karma']]
