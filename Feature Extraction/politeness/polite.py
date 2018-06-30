import urllib
import urllib2
import sys


def get_politeness(text):
    resp = dict()
    url = "http://politeness.mpi-sws.org/score-politeness"
    data = {
            "Host": "politeness.mpi-sws.org",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Referer": "http://politeness.mpi-sws.org/",
            "Content-Length": "16",
            "Connection": "keep-alive",
            }
    data = {"text":text}
    values = urllib.urlencode(data)
    req = urllib2.Request(url, values)
    response = urllib2.urlopen(req)
    return response
    #resp = response.read()
    '''
    except:
        print 'No response'
        return None
    '''

