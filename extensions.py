#!/usr/bin/python

import os
import requests
import json
import subprocess
from time import sleep

def getextensions(cookie, number):
    headers = {'Cookie': cookie}
    URL = 'https://chrome.google.com/webstore/ajax/item?hl=en-US&gl=US&pv=20170206&mce=atf%2Ceed%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Cctm%2Cac%2Chot%2Cmac%2Cfcf%2Crma%2Cigb%2Cpot%2Cevt&count=200&token={0}%401954920&category=extensions&sortBy=0&container=CHROME&features=5&_reqid=3376862&rt=j'
    count = 0

    results = []
    while count < number:
        r = requests.post(URL.format(count), headers=headers)
        parsed = json.loads(r.text[r.text.find('['):])
        results.extend(((x[0], x[1], x[11]) for x in parsed[0][1][1]))
        count += 200
    return results

def getcrx(extension_id):
    CHROME_VERSION = '54.0.2840.99'
    DOWNLOADS = "downloads"

    if (not os.path.exists("%s/%s" %(DOWNLOADS, extension_id))):
        r = requests.get('https://clients2.google.com/service/update2/crx?response=redirect&prodversion=%s&x=id%%3D%s%%26uc' %(CHROME_VERSION, extension_id), timeout=10)
        with open('extension.crx', 'wb') as fd:
            fd.write(r.content)
        subprocess.call(["unzip", "-o", "extension.crx", "-d", "%s/%s" %(DOWNLOADS, extension_id)])
        print("processed %s" %extension_id)
    else:
        print("skipping...")

def fromfile():
    results = []
    with open("list.csv", 'r') as fd:
        for l in fd.readlines():
            results.append(tuple(l.strip('\n').split(',')))
    return results

def createlist(cookie):
    extensions = getextensions(cookie, 5000)
    with open("list.csv", 'w') as fd:
        for l in extensions:
            fd.write(",".join(l).encode('utf-8'))
            fd.write("\n")

def getall():
    extensions = fromfile()
    count = 0
    for x in extensions:
        count += 1
        print("processing extension %d" %count)
        getcrx(x[0])
        # sleep(0.5)

getall()
