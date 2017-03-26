#!/usr/bin/env python
import collections
import operator
import re
import requests
import json
import unicodedata
from subprocess import Popen, PIPE
import time
import networkx as nx
from sys import exit
file = open("logs.txt", "r")
data = file.read()
global currentNode
global flowCount 
global inPort 
global outPort 
#currentNode = switch[]
flowCount = 1
inPort = "1"
outPort = "3"
global staticFlowURL
global deviceInfo 
global response
global jData
staticFlowURL = "http://192.168.56.101:8080/wm/staticflowpusher/json"
deviceInfo = "http://192.168.56.101:8080/wm/device/"
portSwitch = "http://192.168.56.101:8080/wm/core/switch/all/port/json"
#global ip2 
#global ip1
#global deviceMAC
#ip2 = "10.0.0.4"
#ip1 = "10.0.0.1"

def find():
	global max1
	global max2
	global ip1	
	global ip2	
	dictionary = {}
	ip=re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[^0-9]",data)

	for checkip in ip:

    		if checkip in dictionary:
        		dictionary[checkip] += 1
    		else:
        		dictionary[checkip]=1

	#print(dictionary)
	max1 = max(dictionary, key=dictionary.get)
        ip = dictionary[max1]
	#print ("Source ip is ",max1)
	print ("dictionary ",dictionary)
	sorted1 = sorted(dictionary,key=dictionary.__getitem__, reverse=True)
	#sorted2 = sorted(sorted1, key=operator.itemgetter(1), reverse=True)
	print ("sorted1 ",sorted1)
        #print ("sorted2 ",sorted2)
	#print sorted2[3]
   	ik = sorted1[1]
	print ("ip1 ",ik[:-1])
	ip1 = ik[:-1]
        ik1 = sorted1[0]
	print ("ip2 ",ik1[:-1])
        ip2 = ik1[:-1]

def deviceInformation(data):
	global switch
	global hostPorts
	global deviceMAC
	#global ip1
	#global ip2
	global deviceAttachment
	switchDPID = ""
	for i in data: 
		if(i['ipv4']):
			ip = i['ipv4'][0].encode('ascii','ignore')
			mac = i['mac'][0].encode('ascii','ignore')
			deviceMAC[ip] = mac
			
			for j in i['attachmentPoint']:
				for key in j:
					#print ("ATTACHEment Point ",key)
					temp = key.encode('ascii','ignore')
					#print ("TEMP ",temp)	
					if(temp=="switchDPID"):
						switchDPID = j[key].encode('ascii','ignore')
						#print ("switchDPID ",switchDPID)
						switch[ip] = switchDPID
					elif(temp=="port"):
						portNumber = j[key]
						switchShort = switchDPID.split(":")[7]
						hostPorts[ip+ "::" + switchShort] = str(portNumber)
	#print ("SWItCH with attachment point ",switch)
	#print ("MAC address ",deviceMAC)



def flowRule(currentNode, flowCount, inPort, outPort, staticFlowURL):	
      	#print ("MAC address of 10.0.0.1 ",deviceMAC[ip1])
	#print ("MAC address ",deviceMAC)
	flow = {
		'switch':"" + currentNode,
	    "name":"flow" + str(flowCount),
	    "cookie":"0",
	    "priority":"32768",
	    "in_port":inPort,
		"eth_type": "0x0800",
		"ipv4_src": ip1,
		"ipv4_dst": ip2,
		"eth_src": deviceMAC[ip1],
		"eth_dst": deviceMAC[ip2],
	    "active":"true",
	    "actions":" "+ "drop"
	}
        print flow
	jsonData = json.dumps(flow)

	cmd = "curl -X POST -d \'" + jsonData + "\' " + staticFlowURL

	systemCommand(cmd)

	flowCount = flowCount + 1

	flow = {
		'switch':"" + currentNode,
	    "name":"flow" + str(flowCount),
	    "cookie":"0",
	    "priority":"32768",
	    "in_port":outPort,
		"eth_type": "0x0800",
		"ipv4_src": ip1,
		"ipv4_dst": ip2,
		"eth_src": deviceMAC[ip1],
		"eth_dst": deviceMAC[ip2],
	    "active":"true",
	    "actions":" "+ "drop"
	}

	jsonData = json.dumps(flow)

	cmd = "curl -X POST -d \'" + jsonData + "\' " + staticFlowURL
        print jsonData  
	#systemCommand(cmd)

def systemCommand(cmd):
	terminalProcess = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
	terminalOutput, stderr = terminalProcess.communicate()
	print "\n***", terminalOutput, "\n"

if __name__ == '__main__':
	deviceMAC = {}	
	switch = {}
	hostPorts = {}
	deviceAttachment = {}
	sorted1 = {}
	sorted2 = {}
	response = requests.get(deviceInfo)
	ks = {}
	if(response.ok):
		jData = json.loads(response.content)
		deviceInformation(jData)
	#print ("switch ",switch)
       
	#print ("currentNode ",currentNode)
	find()
	currentNode = switch[ip2]
	flowRule(currentNode, flowCount, inPort, outPort, staticFlowURL)
	










