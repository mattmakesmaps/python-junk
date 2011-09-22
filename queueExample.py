#!/usr/bin/python

import Queue
import urllib2
import threading
import time
import pdb

from sgmllib import SGMLParser

# inherits from SGMLParser
class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        href = [v for k, v in attrs if k=='href']
        if href:
            self.urls.extend(href)

# Threaded URL Grab
class ThreadURL(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            #grab host from queue
            host = self.queue.get()
            url = urllib2.urlopen(host)
            url.read()
            
            print "host: %s, thread: %s" % (host, self.ident)
            #signals the queue job is done
            self.queue.task_done()

start = time.time()
def main():
    # urlopen will download header information, give acces to response code
    webpage = urllib2.urlopen("http://hyperquad.telascience.org/")
    parser = URLLister()
    parser.feed(webpage.read())
    webpage.close()
    parser.close()

    # create empty host array, to house WMS only urls
    hosts = []
    for url in parser.urls:
        if "WMS" in url:
            hosts.append(url)
    
    # create an empty queue
    queue = Queue.Queue()

    #spawn a pool of threads, and pass them queue instance
    for i in range(6):
        t = ThreadURL(queue)
        t.setDaemon(queue)
        t.start()
        #print t.ident

    #populate the queue with data
    for host in hosts:
        queue.put(host)

    #wait on the queue until everything has been processed
    queue.join()
main()
print "Elapsed Time: %s" % (time.time() - start)