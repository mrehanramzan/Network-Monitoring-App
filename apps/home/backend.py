#!/usr/bin/env python3
from nfstream import NFStreamer
from time import sleep
import socket
import tldextract
import subprocess

class backend:
    # enter your device name here
    device = "lo"
    value = 1
    runningDomainList = list()
    blockedDomainList = list()#["www.facebook.com", "www.youtube.com"]
    totalPacketsDict = dict()
    timelyPacketsList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x = 0

    ipset_type = "hash:ip"
    ipset_name = "blocked_ip"

    def __init__(self):
        pass

    def get_app_name_from_url(self,url):
        extracted_info = tldextract.extract(url)
        return extracted_info.domain
    
    def dpi_func(self):
        flow_streamer = NFStreamer(source=self.device, statistical_analysis=False, idle_timeout=2, performance_report=0)
        for flow in flow_streamer:
            #app_name = self.get_app_name_from_url(flow.requested_server_name)
            app_name = flow.requested_server_name
            if app_name not in self.runningDomainList and app_name not in self.blockedDomainList and len(app_name) != 0:
                self.runningDomainList.append(app_name)

            if app_name in self.totalPacketsDict:
                self.totalPacketsDict[app_name] += flow.bidirectional_packets
            else:
                self.totalPacketsDict[app_name] = flow.bidirectional_packets
                

        
    
    def packet_flow_per_minute(self):
        sleep(1)
        totalPackets = sum(self.totalPacketsDict.values())
        last = totalPackets - self.x
        self.x = totalPackets

        self.timelyPacketsList.insert(0, last)
        self.timelyPacketsList.pop()
        pass    