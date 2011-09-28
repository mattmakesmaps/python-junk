#!/usr/bin/python

import Queue
import time
import csv
import threading
import urllib2
import sys
from geopy import geocoders

# Threaded Geocoder Class
class ThreadGeocode(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue

    # What's the deal with stuff? Lets do some stuff.
    # Here are instructions that each thread will execute.
    def run(self):
        while True:
            # grab from the queue
            row = self.queue.get()
            try:
                place, (lat, lng) = g.geocode(str(row[3] + " " + row[4] + " " + row[5] + " " + row[6]))
                writer.writerow((row[0],row[1],lat,lng))
                print "%s: %.5f, %.5f, Thread: %s" % (place, lat, lng, self.ident)
            except:
                print "THREADING ERROR:", sys.exc_info()[0]
            # Signal a task is done, and lower the queue count
            self.queue.task_done()

# Setup File Locations
workspace = "./data"
siteSource = "landfills.csv"
siteGeocoded = "landfills_geocoded.csv"

# Geocoding
g = geocoders.Google()
fSource = open(workspace + "/" + siteSource, 'rb')
fGeocoded = open(workspace + "/" + siteGeocoded, 'wb')

# Start Timer
start = time.time()

# Create a queue
queue = Queue.Queue()

for i in range(15):
    t = ThreadGeocode(queue)
    t.daemon = True
    t.start()

try:
    reader = csv.reader(fSource)
    writer = csv.writer(fGeocoded)
    i = 0
    for row in reader:
        # Write column names to output file
        if i == 0:
            writer.writerow((row[0],row[1],"lat","lng"))
            i = i+1
        else:
            # Add an item into the queue
            queue.put(row)
    # Once all tasks are done, unblock
    queue.join()

except:
    print "MAIN ERROR:", sys.exc_info()[0]

finally:
    fSource.close()
    fGeocoded.close()
    print "elapsed time: %s" % (time.time() - start)
