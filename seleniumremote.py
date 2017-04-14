#!/usr/bin/python

import requests
from selenium import webdriver
from analyzer import getextensions

# Create a driver that can control the browser
# extensions - A list of extension ids
# remote_address - a tuple of the form ("hostname or IP", port#)

def get_crx(extension_id):
    CHROME_VERSION = '54.0.2840.99'

    r = requests.get('https://clients2.google.com/service/update2/crx?response=redirect&prodversion=%s&x=id%%3D%s%%26uc' %(CHROME_VERSION, extension_id))
    with open('%s.crx' %extension_id, 'wb') as fd:
        fd.write(r.content)

class browser:
    def __init__(self, extensions, remote_address):
        chrome_options = webdriver.ChromeOptions()
    #    chrome_options.add_argument('--proxy-server=192.168.1.22:8080')

        for extension_id in extensions:
            get_crx(extension_id)
            chrome_options.add_extension('%s.crx' %extension_id)

        self.driver = webdriver.Remote(
                    command_executor='http://%s:%d/wd/hub' %remote_address,
                    desired_capabilities=chrome_options.to_capabilities())

    def test(self):
        self.driver.get('http://172.17.0.1:8000/test.html')
        print(self.driver.page_source)

if __name__=="__main__":
    all_extensions = getextensions()
    print(all_extensions[0])
    b = browser(all_extensions[0:2], ('localhost', 4444))
    b.test()
