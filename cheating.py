#!/usr/bin/python

import sys
import re
from moss import *

BLACKLIST = ['jquery']

def getprojects():
    return [folder for folder in os.listdir('downloads')]

def getjavascripts(project):
    pattern = re.compile(".*\.js$")

    results = []
    for dirName, subdirList, fileList in os.walk(os.path.join('downloads', project)):
        results.extend([(dirName, f) for f in fileList if pattern.match(f)])
    return results

def filefilter(filename):
    return filename == 'background.js'

def main(userid):
    m = moss(userid)
    m.connect()
    projects = getprojects()[:400]
    fileid = 1
    for p in projects:
        files = getjavascripts(p)
        for path, filename in getjavascripts(p):
            if filefilter(filename):
                m.sendfile(filename, os.path.join(path, filename), p, fileid, 'javascript')
                fileid += 1

    url = m.finish()
    with open('results.txt', 'a') as fd:
        fd.write('%s\n' %url)
    print(url)


if __name__=="__main__":
    # if len(sys.argv) == 2:
    #     userid = sys.argv[1]
    userid = "702393572"
    main(userid)
