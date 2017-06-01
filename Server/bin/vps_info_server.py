#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
import json
import requests
import time
import select
import json
from socket import *


API_CONFIG_JSON_PATH = "/opt/etc/api_config.json"

class vps_info:
    def __init__(self):
        self.veid = ""
        self.api_key = ""
        self.__load_config()


    def __load_config(self):
        fd = open(API_CONFIG_JSON_PATH)
        data = json.load(fd)
        self.veid = data["veid"]
        self.api_key = data["api_key"]
        self.port = int(data["port"])
        fd.close()
        

    def handle_msg(self, msg, socket):
        if msg == "GetDataCounter":
            self.GetDataCounter(socket)
        else:
            pass

    def GetDataCounter(self, socket):
        print "GetDataCounter"
        r =  requests.get(url='https://api.64clouds.com/v1/getLiveServiceInfo?veid=%s&api_key=%s'%(self.veid, self.api_key) )
        print "GetDataCounter"
        data = json.loads(r.text)
        request_list = []
        plan_monthly_data = data["plan_monthly_data"]
        data_counter = data["data_counter"]
        data_next_reset = data["data_next_reset"]
        plan_monthly_data = float(float(plan_monthly_data)/float(1024*1024*1024))
        data_counter = float(float(data_counter)/float(1024*1024*1024))
        #print plan_monthly_data
        #print data_counter
        remain = plan_monthly_data - data_counter
        ret_msg = " MONTHLY DATA : %.2f GB \n USED : %.2f GB \n REMAIN : %.2f GB \n EXPIRATION DATE : %s\n"%(plan_monthly_data, data_counter, remain, time.ctime(data_next_reset))
        print ret_msg
        socket.send(ret_msg)
        #print type(request_list[0])
        #request_msg = ','.join(request_list)
        #print request_msg

    def get_ip_by_card_name(self, name):
        return os.popen("ifconfig %s | grep 'inet addr' | awk '{print $2}' | awk -F ':' '{printf $2}'"%name).read().strip('\n')

    def run(self):
        ip = self.get_ip_by_card_name('venet0:0')
        port = self.port
        print "ip:  ", ip
        print "port:", port
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((ip, port))
        sock.listen(20)
        listen_sock_list = []
        listen_sock_list.append(sock)
        while True:
            readable,writeable,exceptional = select.select(listen_sock_list,[],[])
            for s in readable:
                if sock == s:
                    client,addr=sock.accept()
                    listen_sock_list.append(client)
                    print "accept"
                    print client
                    print addr
                    continue
                else:
                    try:
                        sRecvBuff = s.recv(1024)
                        if not sRecvBuff:
                            s.close()
                            listen_sock_list.remove(s)
                            print "remove"
                            continue
                        else:
                            print sRecvBuff
                            self.handle_msg(sRecvBuff, s)
                    except:
                        print "error"
                        s.close()
                        listen_sock_list.remove(s)


if __name__ == "__main__":
    vps_info_server = vps_info()
    vps_info_server.run()
