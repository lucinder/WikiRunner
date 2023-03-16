import requests
import sys
import time
from bs4 import BeautifulSoup
startingPage= "https://en.wikipedia.org/wiki/" + sys.argv[1]
targetPage="https://en.wikipedia.org/wiki/" + sys.argv[2]
# print("Starting url: " + startingPage)
queue = []
alreadyRead = []
numReads = 0
queue.append([startingPage,"run args"])
print("Starting from page " + startingPage)
startTime = time.perf_counter()
while queue: # queue not empty
    entry = queue.pop(0)
    url = entry[0]
    # print("Currently reading " + url)
    alreadyRead.append(url)
    r = requests.get(url)
    # check if our response is valid (200)
    if r.status_code == 200:
        numReads += 1
        if(url == targetPage):
            endTime = time.perf_counter()
            result = int((endTime-startTime)*(10**3))/(10**3)
            print("Reached page " + targetPage)
            print("Destination page found in " + str(numReads) + " links and " + str(result) +" seconds!")
            break
        soup = BeautifulSoup(r.content, 'html.parser')
        # print("Traced page " + soup.title.text + " from " + entry[1]) 
        for link in soup.find_all('a',href=True):
            if "http" in link['href']: # ignore external links
                continue
            newurl = "https://en.wikipedia.org" + link['href']
            if "/wiki/" in newurl and not(
            newurl == "https://en.wikipedia.org/wiki/Main_Page" or
            'Wikipedia:' in newurl or
            'Special:' in newurl or
            'Portal:' in newurl or
            'Help:' in newurl or
            newurl in alreadyRead or
            newurl in queue):
                queue.append([newurl,soup.title.text])
    else:
        continue