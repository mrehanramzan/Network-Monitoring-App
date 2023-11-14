#!/usr/bin/env python3
from ctypes import c_uint32, c_int
from nfstream import NFStreamer
from bcc import BPF
from time import sleep
import ipaddress
import socket, bcc
import tldextract

class backend:
    # enter your device name here
    device = "lo"
    value = 1
    runningDomainList = list()
    blockedDoaminList = list()#["www.facebook.com", "www.youtube.com"]
    totalPacketsDict = dict()
    timelyPacketsList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x = 0

    ipmap = None
    b = bcc.BPF(src_file="apps/home/filter.c")


    def __init__(self):
        fn = self.b.load_func("ipfilter", BPF.XDP)
        self.b.attach_xdp(self.device, fn, 0)
        self.ipmap = self.b["block_ip"]
        print("eBPF has been attached with XDP")

    def get_app_name_from_url(self,url):
        extracted_info = tldextract.extract(url)
        return extracted_info.domain
    
    def dpi_func(self):
        flow_streamer = NFStreamer(source=self.device, statistical_analysis=False, idle_timeout=5, performance_report=0)
        for flow in flow_streamer:
            app_name = self.get_app_name_from_url(flow.requested_server_name)
            if app_name in self.blockedDoaminList and "DNS." not in flow.application_name:
                ip = int(ipaddress.ip_address(flow.dst_ip))
                print("\n>>>> the ip to filter is %s/%u/%s <<<<<\n" %(flow.dst_ip, ip, app_name))
                self.ipmap[c_uint32(ip)] = c_int(self.value)
                
            if app_name not in self.runningDomainList and app_name not in self.blockedDoaminList and len(app_name) != 0:
                self.runningDomainList.append(app_name)

            if app_name in self.totalPacketsDict:
                self.totalPacketsDict[app_name] += flow.bidirectional_packets
            else:
                self.totalPacketsDict[app_name] = flow.bidirectional_packets
                
    def closeXDP_func(self):
        print("Removing XDP HOOK")
        self.b.remove_xdp(self.device, 0)
        print("XDP HOOK removed")

    def unblock_all_func(self):
        self.ipmap.items_delete_batch()
        
    def unblock_func(self, host_name):
        temp = [c_uint32(ipaddress.ip_address(socket.gethostbyname(host_name)))]
        arr = (c_uint32 * len(temp))(*temp)
        
        # print(arr[0])
        # print(type(arr[0]))  

        self.ipmap.items_delete_batch(arr)

    def packet_flow_per_minute(self):
        sleep(1)
        totalPackets = sum(self.totalPacketsDict.values())
        last = totalPackets - self.x
        self.x = totalPackets

        self.timelyPacketsList.insert(0, last)
        self.timelyPacketsList.pop()
        pass
