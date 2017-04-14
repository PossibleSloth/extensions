#!/usr/bin/python

import os
import json

FOLDER = 'downloads'

def getextensions():
    paths = os.listdir(FOLDER)
    return paths

def getpath(extension):
    return os.path.join(FOLDER, extension)

def getmanifest(extension):
    try:
        with open(os.path.join(getpath(extension), 'manifest.json'), 'r') as fd:
            content = fd.read()
            return json.loads(content)
    except ValueError:
        print('error loading manifest for %s' %extension)
        return {}

def scriptmatches():
    results = {}

    for e in getextensions():
        manifest = getmanifest(e)
        if 'content_scripts' in manifest:
            matches = [x['matches'] for x in manifest['content_scripts']]
            unique = []
            for x in matches:
                for y in x:
                    if not y in unique:
                        unique.append(y)

            for url in unique:
                if url in results:
                    results[url] += 1
                else:
                    results[url] = 1
    results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return results

def test():
    results = []

    for e in getextensions():
        manifest = getmanifest(e)
        for k in manifest.keys():
            if not k in results:
                print(k)
                results.append(k)
        if 'sockets' in manifest:
            print(manifest)

if __name__=="__main__":
    test()
