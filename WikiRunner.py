import requests
import sys
import time
from bs4 import BeautifulSoup
startingPage = "https://en.wikipedia.org/wiki/"
targetPage = "https://en.wikipedia.org/wiki/" 
log = 0
mode = 0 # default bfs
traces = []

def flushTraces():
    fileOut = open('WikiRunnerOutput.txt','w') # set up our output file
    fileOut.writelines(traces)
    fileOut.close()

def bfs(startingPage, targetPage, log, mode): # LIFO (queue)
    numReads = 0
    queue = []
    queue.append([startingPage,"run args"])
    traces.append("Starting from page " + startingPage + "\n")
    print("Starting from page " + startingPage)
    alreadyRead = {}
    startTime = time.perf_counter()
    while queue: # queue not empty
        entry = queue.pop() # pop from end of list
        url = entry[0]
        # print("Currently reading " + url)
        alreadyRead[url] = 1
        r = requests.get(url)
        # check if our response is valid (200)
        if r.status_code == 200:
            numReads += 1
            if(url == targetPage):
                endTime = time.perf_counter()
                resultTime = int((endTime-startTime)*(10**3))/(10**3)
                result = "Destination page found in " + str(numReads) + " links and " + str(resultTime) +" seconds!"
                traces.append("Reached page " + targetPage + "\n")
                print("Reached page " + targetPage)
                traces.append(result)
                print(result)
                break
            soup = BeautifulSoup(r.content, 'html.parser')
            traces.append("Traced page " + soup.title.text + " from " + entry[1] + "\n")
            if(log):
                print("Traced page " + soup.title.text + " from " + entry[1]) 
            for link in soup.find_all('a',href=True):
                if "http" in link['href']: # ignore external links
                    continue
                newurl = "https://en.wikipedia.org" + link['href']
                if not badflag(newurl, alreadyRead, queue):
                    queue.insert(0,[newurl,soup.title.text]) # push to start of list
        else:
            continue
    flushTraces()

def dfs(startingPage, targetPage, log, mode): # FIFO (stack)
    numReads = 0
    queue = []
    queue.append([startingPage,"run args"])
    traces.append("Starting from page " + startingPage + "\n")
    print("Starting from page " + startingPage)
    alreadyRead = {}
    startTime = time.perf_counter()
    while queue: # queue not empty
        entry = queue.pop(0) # pop from start of list
        url = entry[0]
        # print("Currently reading " + url)
        alreadyRead[url] = 1
        r = requests.get(url)
        # check if our response is valid (200)
        if r.status_code == 200:
            numReads += 1
            if(url == targetPage):
                endTime = time.perf_counter()
                resultTime = int((endTime-startTime)*(10**3))/(10**3)
                result = "Destination page found in " + str(numReads) + " links and " + str(resultTime) +" seconds!"
                traces.append("Reached page " + targetPage + "\n")
                print("Reached page " + targetPage)
                traces.append(result)
                print(result)
            soup = BeautifulSoup(r.content, 'html.parser')
            traces.append("Traced page " + soup.title.text + " from " + entry[1] + "\n")
            if(log):
                print("Traced page " + soup.title.text + " from " + entry[1]) 
            for link in soup.find_all('a',href=True):
                if "http" in link['href']: # ignore external links
                    continue
                newurl = "https://en.wikipedia.org" + link['href']
                if not badflag(newurl, alreadyRead, queue):
                    queue.insert(0,[newurl,soup.title.text]) # push to start of list
        else:
            continue
    flushTraces()

def badflag(newurl, read, queue):
    return not ("/wiki/" in newurl) or newurl == "https://en.wikipedia.org/wiki/Main_Page" or 'User:' in newurl or 'User_talk:' in newurl or 'Template:' in newurl or 'Template_talk:' in newurl or 'Talk:' in newurl or 'Category:' in newurl or 'File:' in newurl or 'Wikipedia:' in newurl or 'Special:' in newurl or 'Portal:' in newurl or 'Help:' in newurl or newurl in read or newurl in queue

#main area
if(len(sys.argv) < 2):
    print("Error: Missing source page!")
    sys.exit(0)
startingPage += sys.argv[1]
if(len(sys.argv) < 3):
    print("Error: Missing destination page!")
    sys.exit(0)
targetPage += sys.argv[2]
# print("Starting url: " + startingPage)
if(len(sys.argv) > 3):
    if(sys.argv[3] == "dfs"):
        mode = 1
    elif(sys.argv[3] == "1"):
        log = 1 # in case the user expunges the third argument but wants the fourth
if(len(sys.argv) > 4):
    log = sys.argv[4]
if(mode == 1):
    dfs(startingPage, targetPage, log, mode)
else:
    bfs(startingPage, targetPage, log, mode)