#!/usr/bin/python

import sys
from random import randrange
import requests
import json
import codecs
from pymongo import MongoClient 

import time
import pdb

def main(argv):
	print 'Format: python intents.py <path to network.json> <path to mission.json>'
	print 'Number of arguments:', len(sys.argv), 'arguments.'
	network_file = sys.argv[1]
	mission_file = sys.argv[2]

	populateData(network_file, mission_file)

def populateData(network_file, mission_file):
	dataset = []
	#Get data from network and mission
	with codecs.open(network_file, "r", encoding="utf-8") as network:
		nw = json.load(network)
		loki = nw["$loki"]
		for hosts in nw["hosts"]:
			host = hosts.get("display_name")
			id_nw = hosts.get("id")
	#network.close()
		
	with codecs.open(mission_file, "r", encoding="utf-8") as mission:
		mi = json.load(mission)
		for req in mi["missionRequirements"]:
			mi_src = req.get("src")
			mi_id = req.get("id")
			mi_dst = req.get("dst")		

			# Get the network info of the specifed hosts in mission requirements	
			mi_src_short = mi_src.rpartition('.')[2]
			mi_dst_short = mi_dst.rpartition('.')[2]
			for hosts in nw["hosts"]:
				host = hosts.get("display_name")
				if (mi_src_short == host):
					src_host_id = hosts.get("id")
				if (mi_dst_short == host):
					dst_host_id = hosts.get("id")
						
			data = {
			'src_host_id' : src_host_id,
			'dst_host_id' : dst_host_id,
			'mi_id' : mi_id,
			'loki_id' : loki}
			dataset.append(data)
			generateIntent(src_host_id,dst_host_id,mi_id,loki)
	#generateIntent(src_host_id,dst_host_id,mi_id,loki)

def generateIntent(src_host_id,dst_host_id,mi_id,loki):
	#REST API
	URL = "http://localhost:8181/onos/v1/intents"
	AUTH = ('onos','rocks')
	HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
	r = requests.get(url = URL, auth = AUTH)
	data_out = r.json()
	intents = data_out["intents"]
	#print "------------------"
	#print intents


	print("Generate Intent")
	with codecs.open('resources/example6.json', "r", encoding="utf-8") as newrule:
		jsonfile = json.load(newrule)
		jsonfile['one'] = src_host_id
		jsonfile['two'] = dst_host_id
	print newrule.encoding
	with open("resources/example6.json", "w") as newrule:
		json.dump(jsonfile, newrule)
	#cursor = IntentStore.find()
	#for record in cursor:
	#	print(record)
	r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
	print "******************" 
	LOCATION = r.headers["Location"]
	print("location = ",LOCATION)
	
	#r = requests.get(url = LOCATION, auth = AUTH)
	#data_out = r.json()
	#print data_out
	#id1 = data_out["id"]

	id1 = LOCATION.rpartition("/")[2]
	#pdb.set_trace()
	id1_hex = hex(int(id1))
	URL_flows = "http://localhost:8181/onos/v1/intents/relatedflows/org.onosproject.cli/{}".format(id1_hex)
	time.sleep(1)
	r = requests.get(url = URL_flows, auth = AUTH)
	data_out = r.json()
	print(data_out)
	
	#URL_flows = "http://localhost:8181/onos/v1/intents/relatedflows/org.onosproject.cli/80"
	#time.sleep(1)
	#r = requests.get(url = URL_flows, auth = AUTH)
	#data_out = r.json()
	#print(data_out)

	data_out["mi_id"] = "md{}_m{}_i{}".format(loki,mi_id,id1)
	with open("resources/out.json", "w") as newrule:
		json.dump(data_out, newrule)

        URL_WS="http://localhost:5000/api/intents"
        HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
	r = requests.post(url = URL_WS, data = json.dumps(data_out), headers = HEADERS)
        print r.text
	
if __name__ == "__main__":
	 main(sys.argv[1:])
