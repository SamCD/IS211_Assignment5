#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Server Simulation"""

import csv
import urllib2
import Queue
import argparse



class Server(object):
    """Test server for simulation"""

    
    def __init__(self):
        self.current_task = None
        self.time_elapsed = 0
        self.time_remaining = 0


    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
        if self.time_remaining <= 0:
            self.current_task = None


    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False


    def start_next(self,new_task,time):
        self.current_task = new_task
        self.time_remaining = time


class Request(object):
    """Simulates requests for the server"""

    
    def __init__(self, time,length):
        self.timestamp = time
        self.length = length


    def get_stamp(self):
        return self.timestamp


    def get_length(self):
        return self.length


    def wait_time(self, current_time):
        return current_time - self.timestamp


def simulateOneServer(testfile):

    server = Server()
    req_queue = Queue.Queue()
    waiting_times = []
    for request in testfile:
        task = Request(int(request[0]),int(request[2]))
        lapse = int(request[0]) - server.time_elapsed
        if lapse:
            for i in range(lapse + 1):
                server.tick()
        req_queue.put(task)
        if (not server.busy()) and (not req_queue.empty()):
            next_task = req_queue.get()
            
            waiting_times.append(next_task.wait_time(server.time_elapsed))
            server.start_next(next_task,next_task.length)
        server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining."
            %(average_wait, req_queue.qsize()))


def simulateManyServers(testfile):

    servlist = [ [] for i in range(args.servers) ]
    while testfile:
        for i in range(servlist):
            servlist[i].insert(0,testfile.next())
    for i in range(servlist):
        simulateOneServer(servlist[i])

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--servers')
    args = parser.parse_args()
    datafile = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'
    req = urllib2.Request(datafile)
    dldata = urllib2.urlopen(req)
    testfile = csv.reader(dldata)
    if args.servers:
        simulateOneServer(testfile)
    else:
        simulateManyServers(testfile)
