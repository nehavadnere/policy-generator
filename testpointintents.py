#!/usr/bin/python

import sys
import os
from random import randrange
import requests
import json
import codecs
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from PolicyLib import PolicyHandler 
#from pymongo import MongoClient 

import pdb

#ONOS_IP = "127.0.0.1"
ONOS_IP = "localhost"
count  = 0


def main(argv):
    #pdb.set_trace()
    print('Format: python intentscript.py <number of intents> <host range begining> <host range end>')
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Number of intents:', str(sys.argv[1]))
    print('Host range beginning :', str(sys.argv[2]))
    print('Host range ending: :', str(sys.argv[3]))
    print('Test to run(number): :', str(sys.argv[4]))
    num = sys.argv[1]
    range1 = sys.argv[2]
    range2 = sys.argv[3]
    range2 = sys.argv[3]
    test_num = sys.argv[4]    
    rules = []

    # Enter a mode for testing. For manual mode, ONOS and mininet configurations are not needed.
    # It will just create simulated flow rules for testing.
    # For onos mode, controller and mininet should be in working condition and flows are generated
    # automatically through ONOS intents using REST APIs.
    mode = "manual"
    # mode = "onos"

    #PolicyHandler().comparePort(1,1)

    if int(test_num) == 1:
        #PD1
        PD1(num,range1,range2)
    elif int(test_num) == 2:
        PD2(num,range1,range2)
    elif int(test_num) == 3:
        PD3(num,range1,range2)
    elif int(test_num == 4):
        generateIntents_k1(num, range1, range2)
    elif test_num == 5:
        generateIntents_k2_mac(num, range1, range2)
    elif test_num == 6:
        generateIntents_k3_mac(num, range1, range2)
    elif test_num == 7:
        generateIntents_k4_ip(num, range1, range2)
    elif test_num == 8:
        generateIntents_k5_ip(num, range1, range2)
    elif test_num == 9:
        generateIntents_k6_ip(num, range1, range2)
    elif test_num == 10:
        generateIntents_k8_tcpPort(num, range1, range2)
    elif test_num == 11:
        generateIntents_k7_tcpPort(num, range1, range2)
    elif test_num == 12:
        generateIntents_k9_rev(num, range1, range2)
    elif test_num == 12:
        generateIntents_fwd(num, range1, range2)
    elif int(test_num) == 13:
        generateIntents_routing(num, range1, range2)
    elif int(test_num) == 14:
        generateIntents_acl(num, range1, range2)
    elif int(test_num) == 15:
        EMEC_focused(num,range1, range2, rules, mode)
    elif int(test_num) == 16:
        SUBEC_focused(num,range1, range2, rules, mode)
    elif int(test_num) == 17:
        OLEC_focused(num,range1, range2, rules, mode)
    elif int(test_num) == 18:
        #generateIntents_k8_tcpPort_proto(num, range1, range2, "onos", 80)
        generateIntentPortVariations(num, range1, range2, "onos")
    elif int(test_num) == 19:
        generateIntents_k8_tcpPort(num, range1, range2, onos)
    else:
        print("Enter a test number betwen 1-17")
    opf = {}
    opf["rules"] = rules
    print("RULES ==> ",opf)
    writeFileJson(opf, "Parsed-test-manual.json", "")
    #PolicyHandler().flowPolicyCheckAll_waterfall(opf)

def writeFileJson(content, filename, outputPath):
        with open(filename, "w", encoding='utf-8') as write_file:
            write_file.write(json.dumps(content,ensure_ascii=True, indent=4))

def writeFile(self, content, filename, outputPath):
        filefull = outputPath + os.path.sep + filename
        file1 = open(filefull,"a+")
        file1.write(content)
        file1.close()

#def generateIntents_proto(num, count, rules, mode, proto):
#    filename = "connectivity_"+num+"hosts.txt"
#    outfile = open(filename,"a+")
#    for i in range(1,int(num)+1):
#        for j in range(1,int(num)+1):
#            if i!=j:
#                #REST API
#                # ONOS mode
            
def generateIntents_k1_complete(num, count, rules, mode):
    #range1_new = int(range1)
    #range2_new = int(range2)
    content1 = ""
    filename = "connectivity_"+num+"hosts.txt"
    outfile = open(filename,"a+")
    for i in range(1,int(num)+1):
        #range1_new = int(range1)        
        for j in range(1,int(num)+1):
            if i!=j:
                #REST API
                # ONOS mode
                if mode == "onos":
                    URL = "http://{}:8181/onos/v1/intents".format(ONOS_IP)
                    AUTH = ('onos','rocks')
                    HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
                    with codecs.open('resources/example7.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)                    
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
                    #time.sleep(2)
                    #print r.content,i,j

                #Create manual tests:
                if mode == "manual":
                    with codecs.open('resources/example7-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                        content1 = "Rule " +str(count)+ ":: "+ "Host " +str(i)+ "-> Host " +str(j)+ ", ingress=" +str(jsonfile['deviceId'])+ ":" +str(jsonfile['criteria'][0]['port'])+ ", egress=" +str(jsonfile['deviceId'])+ ":" +str(jsonfile['instruction'][0]['port']) + "\n"
                        outfile.write(content1)
            #range1_new = int(range1_new) + j
        #range2_new = int(range2_new) + i
#        with open("outfile.txt", "a+") as outfile:
#            outfile.write(content1)
    outfile.close()

def generateIntents_k1(num, range1, range2):
    for i in range(int(num)):
        #details = generateDetails(range1,range2)    

        #REST API
        URL = "http://{}:8181/onos/v1/intents".format(ONOS_IP)
        AUTH = ('onos','rocks')
        HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
        #r = requests.get(url = URL, auth = AUTH)
        #data_out = r.json()
        #intents = data_out["intents"]
        #print "------------------"
        #print intents
        #print "------------------"
        #print r.encoding
        #print "------------------"
        #print r.content
        #print "------------------"
        #print r.text
        #print "------------------"
        with codecs.open('resources/example7.json', "r", encoding="utf-8") as newrule:
            jsonfile = json.load(newrule)
            jsonfile['ingressPoint']['port'] = str(range1)
            jsonfile['egressPoint']['port'] = str(range2)
        #print newrule.encoding
        #with open("resources/example4.json", "w") as newrule:
        #   json.dump(jsonfile, newrule)
        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
        print(r.content)
        range1 = int(range1) + 1
        range2 = int(range2) -1

def generateDetails(range1, range2):
    #src = randrange(int(range1),int(range2))
    #dst = randrange(int(range1),int(range2))
    src = int(range1)
    dst = int(range2)
    src_hex = hex(src)[2:]
    dst_hex = hex(dst)[2:]
    lens = len(src_hex)
    lend = len(dst_hex)

    if (lens < 2 and lend < 2):
       src_full = '00:00:00:00:00:0{}'.format(src_hex)
       dst_full = '00:00:00:00:00:0{}'.format(dst_hex)
    elif (lens < 2 and lend >= 2):
       src_full = '00:00:00:00:00:0{}'.format(src_hex)
       dst_full = '00:00:00:00:00:{}'.format(dst_hex)
    elif (lend < 2 and lens >= 2):
       dst_full = '00:00:00:00:00:0{}'.format(dst_hex)
       src_full = '00:00:00:00:00:{}'.format(src_hex)
    else : 
       src_full = '00:00:00:00:00:{}'.format(src_hex)
       dst_full = '00:00:00:00:00:{}'.format(dst_hex)
    ipsrc = '10.0.0.{}/32'.format(src)
    ipdst = '10.0.0.{}/32'.format(dst)

    data = {'src_full' : src_full, 
            'dst_full' : dst_full,
            'ipsrc' : ipsrc,
            'ipdst' : ipdst,
            'tcpsrc' : src,
            'tcpdst' : dst,
            'udpsrc' : src,
            'udpdst' : dst,
            'vlanid' : src}
    return data
       
def generateIntents_k2_mac(num, range1, range2):
    for i in range(int(num)):
        details = generateDetails(range1,range2)    
        #REST API
        URL = "http://172.17.0.2:8181/onos/v1/intents"
        AUTH = ('onos','rocks')
        HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
        with codecs.open('resources/example8.json', "r", encoding="utf-8") as newrule:
            jsonfile = json.load(newrule)
            jsonfile['ingressPoint']['port'] = str(range1)
            jsonfile['egressPoint']['port'] = str(range2)
            jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
        print(r.content)
        range1 = int(range1) + 1
        range2 = int(range2) -1

def generateIntents_k3_mac(num, range1, range2):
    for i in range(int(num)):
        details = generateDetails(range1,range2)    
        #REST API
        URL = "http://172.17.0.2:8181/onos/v1/intents"
        AUTH = ('onos','rocks')
        HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
        with codecs.open('resources/example9.json', "r", encoding="utf-8") as newrule:
            jsonfile = json.load(newrule)
            jsonfile['ingressPoint']['port'] = str(range1)
            jsonfile['egressPoint']['port'] = str(range2)
            jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
            jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
        print(r.content)
        range1 = int(range1) + 1
        range2 = int(range2) -1

def generateIntents_k4_ip(num, range1, range2):
    for i in range(int(num)):
        details = generateDetails(range1,range2)    
        #REST API
        URL = "http://172.17.0.2:8181/onos/v1/intents"
        AUTH = ('onos','rocks')
        HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
        with codecs.open('resources/example10.json', "r", encoding="utf-8") as newrule:
            jsonfile = json.load(newrule)
            jsonfile['ingressPoint']['port'] = str(range1)
            jsonfile['egressPoint']['port'] = str(range2)
            jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
            jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
            jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
        print(r.content)
        range1 = int(range1) + 1
        range2 = int(range2) -1

def generateIntents_k5_ip(num, range1, range2):
    for i in range(int(num)):
        details = generateDetails(range1,range2)    
        #REST API
        URL = "http://172.17.0.2:8181/onos/v1/intents"
        AUTH = ('onos','rocks')
        HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
        with codecs.open('resources/example11.json', "r", encoding="utf-8") as newrule:
            jsonfile = json.load(newrule)
            jsonfile['ingressPoint']['port'] = str(range1)
            jsonfile['egressPoint']['port'] = str(range2)
            jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
            jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
            jsonfile['selector']['criteria'][2]['ip'] = details['ipdst']
        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
        print(r.content)
        range1 = int(range1) + 1
        range2 = int(range2) -1

def generateIntents_k6_ip(num, range1, range2):
    for i in range(int(num)):
        details = generateDetails(range1,range2)    
        #REST API
        URL = "http://172.17.0.2:8181/onos/v1/intents"
        AUTH = ('onos','rocks')
        HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
        with codecs.open('resources/example12.json', "r", encoding="utf-8") as newrule:
            jsonfile = json.load(newrule)
            jsonfile['ingressPoint']['port'] = str(range1)
            jsonfile['egressPoint']['port'] = str(range2)
            jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
            jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
            jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
            jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
        print(r.content)
        range1 = int(range1) + 1
        range2 = int(range2) -1

def generateIntents_k7_tcpPort(num, range1, range2):
    for i in range(int(num)):
        details = generateDetails(range1,range2)    
        #REST API
        URL = "http://172.17.0.2:8181/onos/v1/intents"
        AUTH = ('onos','rocks')
        HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
        with codecs.open('resources/example13.json', "r", encoding="utf-8") as newrule:
            jsonfile = json.load(newrule)
            jsonfile['ingressPoint']['port'] = str(range1)
            jsonfile['egressPoint']['port'] = str(range2)
            jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
            jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
            jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
            jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
            jsonfile['selector']['criteria'][4]['tcpPort'] = details['tcpsrc']
        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
        print(r.content)
        range1 = int(range1) + 1
        range2 = int(range2) -1

def generateIntentPortVariations(num, range1, range2, mode):
    portMap = [
                    {
                        'proto':80,
                        'name':'html',
                        'l4':'tcp'
                    },
                    {
                        'proto':1433,
                        'name':'sql',
                        'l4':'udp'
                    },                    
                    {
                        'proto':143,
                        'name':'imap',
                        'l4':'tcp'
                    }
                ]            
    count = 0
    for i in range(len(portMap)):
        proto = portMap[i]['proto']
        l4 = portMap[i]['l4']
        count = generateIntents_k8_tcpPort_proto(num, range1, range2, mode, proto, l4,count)



def generateIntents_k8_tcpPort_proto(num, range1, range2, mode, proto, l4, count):
    content1 = ""
    filename = "topo1_network1_"+num+"hosts.txt"
    outfile = open(filename,"a+")
    for i in range(1,int(num)+1):
        for j in range(1,int(num)+1):
            if i!=j:
                details = generateDetails(i,j)    
                #REST API
                if mode == "onos":
                    URL = "http://{}:8181/onos/v1/intents".format(ONOS_IP)
                    #URL = "http://localhost:8181/onos/v1/intents"
                    AUTH = ('onos','rocks')
                    HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
                    if l4=="tcp":
                        with codecs.open('resources/example14.json', "r", encoding="utf-8") as newrule:
                            jsonfile = json.load(newrule)
                            jsonfile['ingressPoint']['port'] = str(i)
                            jsonfile['egressPoint']['port'] = str(j)
                            jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                            jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                            jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                            jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                            jsonfile['selector']['criteria'][4]['tcpPort'] = proto
                            jsonfile['selector']['criteria'][5]['tcpPort'] = proto
                        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
                        print(r.content)
                        count += 1
                        content1 = "Rule " +str(count)+ ":: "+ "Host " +str(i)+ "-> Host " +str(j)
                        content1 = content1 + ", ingress=" +str(jsonfile['ingressPoint']['device'])+ ":" +str(jsonfile['ingressPoint']['port'])
                        content1 = content1 +", egress=" +str(jsonfile['egressPoint']['device'])+ ":" +str(jsonfile['egressPoint']['port'])
                        content1 = content1 + ", src_mac=" +details['src_full']
                        content1 = content1 + ", dst_mac=" +details['dst_full']
                        content1 = content1 + ", src_ip=" +details['ipsrc']
                        content1 = content1 + ", dst_ip=" +details['ipdst']
                        content1 = content1 + ", src_tcp=" +str(jsonfile['selector']['criteria'][4]['tcpPort'])

                        content1 = content1 + ", dst_tcp=" +str(jsonfile['selector']['criteria'][5]['tcpPort'])
                        content1 = content1 + "\n"
                        outfile.write(content1)
                        #range1 = int(range1) + 1
                        #range2 = int(range2) -1
                    if l4=="udp":
                        with codecs.open('resources/example45.json', "r", encoding="utf-8") as newrule:
                            jsonfile = json.load(newrule)
                            jsonfile['ingressPoint']['port'] = str(i)
                            jsonfile['egressPoint']['port'] = str(j)
                            jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                            jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                            jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                            jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                            jsonfile['selector']['criteria'][4]['udpPort'] = proto
                            jsonfile['selector']['criteria'][5]['udpPort'] = proto
                        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
                        print(r.content)
                        count += 1
                        content1 = "Rule " +str(count)+ ":: "+ "Host " +str(i)+ "-> Host " +str(j)
                        content1 = content1 + ", ingress=" +str(jsonfile['ingressPoint']['device'])+ ":" +str(jsonfile['ingressPoint']['port'])
                        content1 = content1 +", egress=" +str(jsonfile['egressPoint']['device'])+ ":" +str(jsonfile['egressPoint']['port'])
                        content1 = content1 + ", src_mac=" +details['src_full']
                        content1 = content1 + ", dst_mac=" +details['dst_full']
                        content1 = content1 + ", src_ip=" +details['ipsrc']
                        content1 = content1 + ", dst_ip=" +details['ipdst']
                        content1 = content1 + ", src_udp=" +str(jsonfile['selector']['criteria'][4]['udpPort'])

                        content1 = content1 + ", dst_udp=" +str(jsonfile['selector']['criteria'][5]['udpPort'])
                        content1 = content1 + "\n"
                        outfile.write(content1)
                        #range1 = int(range1) + 1
                        #range2 = int(range2) -1

    outfile.close()
    return count

def generateIntents_k8_tcpPort(num, range1, range2, mode):
    for i in range(1,int(num)+1):
        for j in range(1,int(num)+1):
            if i!=j:
                details = generateDetails(i,j)    
                #REST API
                if mode == "onos":
                    URL = "http://{}:8181/onos/v1/intents".format(ONOS_IP)
                    AUTH = ('onos','rocks')
                    HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
                    with codecs.open('resources/example14.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(range1)
                        jsonfile['egressPoint']['port'] = str(range2)
                        jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                        jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                        jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][4]['tcpPort'] = details['tcpsrc']
                        jsonfile['selector']['criteria'][5]['tcpPort'] = details['tcpdst']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
                    print(r.content)
                    #range1 = int(range1) + 1
                    #range2 = int(range2) -1

def generateIntents_k9_rev(num, range1, range2):
    for i in range(int(num)):
        details = generateDetails(range1,range2)    
        #REST API
        URL = "http://172.17.0.2:8181/onos/v1/intents"
        AUTH = ('onos','rocks')
        HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
        with codecs.open('resources/example14.json', "r", encoding="utf-8") as newrule:
            jsonfile = json.load(newrule)
            jsonfile['ingressPoint']['port'] = str(range1)
            jsonfile['egressPoint']['port'] = str(range2)
            jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
            jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
            jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
            jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
            jsonfile['selector']['criteria'][4]['tcpPort'] = details['tcpdst']
            jsonfile['selector']['criteria'][5]['tcpPort'] = details['tcpsrc']
        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
        print(r.content)
        range1 = int(range1) + 1
        range2 = int(range2) -1

def generateIntents_routing(num, range1, range2):
    for i in range(int(num)):
        details = generateDetails(range1,range2)    
        #REST API
        URL = "http://172.17.0.2:8181/onos/v1/intents"
        AUTH = ('onos','rocks')
        HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
        with codecs.open('resources/example15.json', "r", encoding="utf-8") as newrule:
            jsonfile = json.load(newrule)
            jsonfile['ingressPoint']['port'] = str(range1)
            jsonfile['egressPoint']['port'] = str(range2)
            jsonfile['selector']['criteria'][0]['ip'] = details['ipdst']
        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
        print(r.content)
        range1 = int(range1) + 1
        range2 = int(range2) -1
    
def generateIntents_ip_complete(num, count, rules, mode):
    #range1_new = int(range1)
    #range2_new = int(range2)
    for i in range(1, int(num)):
        #range1_new = int(range1)
        for j in range(1, int(num)):
            details = generateDetails(i,j)    
            #REST API
            URL = "http://172.17.0.2:8181/onos/v1/intents"
            AUTH = ('onos','rocks')
            HEADERS = {'content-type': 'application/json', 'Access':'application/json'}

            #Ip, Is
            # ONOS
            if mode == "onos":
                with codecs.open('resources/example43.json', "r", encoding="utf-8") as newrule:
                    jsonfile = json.load(newrule)
                    jsonfile['ingressPoint']['port'] = str(i)
                    jsonfile['egressPoint']['port'] = str(j)
                    jsonfile['selector']['criteria'][0]['ip'] = details['ipsrc']
                r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
                print(r.content,i,j)

            if mode == "manual":
                with codecs.open('resources/example43-manual.json', "r", encoding="utf-8") as newrule:
                    jsonfile = json.load(newrule)
                    jsonfile['criteria'][0]['port'] = i
                    jsonfile['instruction'][0]['port'] = str(j)
                    jsonfile['criteria'][1]['ip'] = details['ipsrc']
                    jsonfile['id'] = str('{:017x}'.format(count+1))
                    count += 1
                    print(json.dumps(jsonfile))
                    rules.append(jsonfile)
                
            #Ip, Id
            if mode == "onos":
                with codecs.open('resources/example15.json', "r", encoding="utf-8") as newrule:
                    jsonfile = json.load(newrule)
                    jsonfile['ingressPoint']['port'] = str(i)
                    jsonfile['egressPoint']['port'] = str(j)
                    jsonfile['selector']['criteria'][0]['ip'] = details['ipdst']
                r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
                print(r.content,i,j)
            
            if mode == "manual":
                with codecs.open('resources/example15-manual.json', "r", encoding="utf-8") as newrule:
                    jsonfile = json.load(newrule)
                    jsonfile['criteria'][0]['port'] = i
                    jsonfile['instruction'][0]['port'] = str(j)
                    jsonfile['criteria'][1]['ip'] = details['ipdst']
                    jsonfile['id'] = str('{:017x}'.format(count+1))
                    count += 1
                    print(json.dumps(jsonfile))
                    rules.append(jsonfile)
                
            #Ip, Is,  Id
            if mode == "onos":
                with codecs.open('resources/example44.json', "r", encoding="utf-8") as newrule:
                    jsonfile = json.load(newrule)
                    jsonfile['ingressPoint']['port'] = str(i)
                    jsonfile['egressPoint']['port'] = str(j)
                    jsonfile['selector']['criteria'][0]['ip'] = details['ipsrc']
                    jsonfile['selector']['criteria'][1]['ip'] = details['ipdst']
                r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
                print(r.content,i,j)
            
            if mode == "manual":
                with codecs.open('resources/example44-manual.json', "r", encoding="utf-8") as newrule:
                    jsonfile = json.load(newrule)
                    jsonfile['criteria'][0]['port'] = i
                    jsonfile['instruction'][0]['port'] = str(j)
                    jsonfile['criteria'][1]['ip'] = details['ipsrc']
                    jsonfile['criteria'][2]['ip'] = details['ipdst']
                    jsonfile['id'] = str('{:017x}'.format(count+1))
                    count += 1
                    print(json.dumps(jsonfile))
                    rules.append(jsonfile)
                
            #Ip, Is,  Id
            #range1_new = range1_new + j
        #range2_new = range2_new + i


def generateIntents_fwd(num, range1, range2):
    for i in range(int(num)):
        details = generateDetails(range1,range2)    
        #REST API
        URL = "http://172.17.0.2:8181/onos/v1/intents"
        AUTH = ('onos','rocks')
        HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
        with codecs.open('resources/example7.json', "r", encoding="utf-8") as newrule:
            jsonfile = json.load(newrule)
            jsonfile['ingressPoint']['port'] = str(range1)
            jsonfile['egressPoint']['port'] = str(range2)
        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
        range1 = int(range1) + 1
        range2 = int(range2) -1

def generateIntents_acl(num, range1, range2):
    for i in range(int(num)):
        details = generateDetails(range1,range2)    
        #REST API
        URL = "http://172.17.0.2:8181/onos/v1/intents"
        AUTH = ('onos','rocks')
        HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
        with codecs.open('resources/example17.json', "r", encoding="utf-8") as newrule:
            jsonfile = json.load(newrule)
            jsonfile['ingressPoint']['port'] = str(range1)
            jsonfile['egressPoint']['port'] = str(range2)
            jsonfile['selector']['criteria'][0]['ip'] = details['ipsrc']
            jsonfile['selector']['criteria'][1]['ip'] = details['ipdst']
            jsonfile['selector']['criteria'][2]['tcpPort'] = details['tcpsrc']
            jsonfile['selector']['criteria'][3]['tcpPort'] = details['tcpdst']
        r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
        range1 = int(range1) + 1
        range2 = int(range2) -1

def generateIntents_SUBEC_focused(num, count, rules, mode):
    #pdb.set_trace()
    #range1_new = int(range1)
    #range2_new = int(range2)
    for i in range(1,int(num)):
        #range1_new = int(range1)
        for j in range(1,int(num)):
            if i != j:
                details = generateDetails(i,j)    
                #REST API
                URL = "http://172.17.0.2:8181/onos/v1/intents"
                AUTH = ('onos','rocks')
                HEADERS = {'content-type': 'application/json', 'Access':'application/json'}
                #postJson(URL,AUTH,HEADERS,details)

                #ip, v
                if mode == "onos":
                    with codecs.open('resources/example18.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        #jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        #jsonfile['selector']['criteria'][4]['tcpPort'] = details['tcpsrc']
                        #jsonfile['selector']['criteria'][5]['tcpPort'] = details['tcpdst']
                    #r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
                    #print(r.content)
           
                # Create manual tests
                if mode == "manual":
                    with codecs.open('resources/example18-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['vlanid'] = details['vlanid']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, v
                #with codecs.open('resources/example18.json', "r", encoding="utf-8") as newrule:
                #    jsonfile = json.load(newrule)
                #    jsonfile['ingressPoint']['port'] = str(i)
                #    jsonfile['egressPoint']['port'] = str(j)
                #    #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                #    #jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                #    #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                #    #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                #    jsonfile['selector']['criteria'][0]['tcpPort'] = details['tcpsrc']
                #r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS) 
                
                #ip, Ps(tcp)
                if mode == "onos":
                    with codecs.open('resources/example19.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        #jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][0]['tcpPort'] = details['tcpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)

                if mode == "manual":
                    with codecs.open('resources/example19-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['tcpPort'] = details['tcpsrc']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Pd(tcp)
                if mode == "onos":
                    with codecs.open('resources/example20.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        #jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][0]['tcpPort'] = details['tcpdst']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example20-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['tcpPort'] = details['tcpdst']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Ps(udp)
                if mode == "onos":
                    with codecs.open('resources/example21.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        #jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][0]['udpPort'] = details['udpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example21-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['udpPort'] = details['udpsrc']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Pd(udp)
                if mode == "onos":
                    with codecs.open('resources/example22.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        #jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][0]['udpPort'] = details['udpdst']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example22-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['udpPort'] = details['udpdst']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Ed(tcp)
                if mode == "onos":
                    with codecs.open('resources/example23.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][0]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        #jsonfile['selector']['criteria'][0]['tcpPort'] = details['tcpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example23-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['dst_full']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, v, Es
                if mode == "onos":
                    with codecs.open('resources/example24.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        jsonfile['selector']['criteria'][1]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        #jsonfile['selector']['criteria'][0]['tcpPort'] = details['tcpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example24-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['src_full']
                        jsonfile['criteria'][2]['vlanid'] = details['vlanid']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Es, Ps(tcp)
                if mode == "onos":
                    with codecs.open('resources/example25.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][1]['tcpPort'] = details['tcpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example25-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['src_full']
                        jsonfile['criteria'][2]['tcpPort'] = details['tcpsrc']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Es, Pd(tcp)
                if mode == "onos":
                    with codecs.open('resources/example26.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][1]['tcpPort'] = details['tcpdst']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example26-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][2]['mac'] = details['src_full']
                        jsonfile['criteria'][1]['tcpPort'] = details['tcpdst']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Es, Ps(udp)
                if mode == "onos":
                    with codecs.open('resources/example27.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][1]['udpPort'] = details['udpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example27-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][2]['mac'] = details['src_full']
                        jsonfile['criteria'][1]['udpPort'] = details['udpsrc']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Es, Ps(udp)
                if mode == "onos":
                    with codecs.open('resources/example28.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][1]['udpPort'] = details['udpdst']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example28-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['src_full']
                        jsonfile['criteria'][2]['udpPort'] = details['udpdst']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Ed, v
                if mode == "onos":
                    with codecs.open('resources/example29.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        jsonfile['selector']['criteria'][1]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][0]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        #jsonfile['selector']['criteria'][1]['udpPort'] = details['udpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example29-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][2]['mac'] = details['dst_full']
                        jsonfile['criteria'][1]['vlanid'] = details['vlanid']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Ed, Ps(tcp)
                if mode == "onos":
                    with codecs.open('resources/example30.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][0]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][1]['tcpPort'] = details['tcpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example30-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['dst_full']
                        jsonfile['criteria'][2]['tcpPort'] = details['tcpsrc']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Ed, Pd(tcp)
                if mode == "onos":
                    with codecs.open('resources/example31.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][0]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][1]['tcpPort'] = details['tcpdst']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example31-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['dst_full']
                        jsonfile['criteria'][2]['tcpPort'] = details['tcpdst']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Ed, Ps(udp)
                if mode == "onos":
                    with codecs.open('resources/example32.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][0]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][1]['udpPort'] = details['udpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example32-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['dst_full']
                        jsonfile['criteria'][2]['udpPort'] = details['udpsrc']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Ed, Pd(udp)
                if mode == "onos":
                    with codecs.open('resources/example33.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][0]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][1]['udpPort'] = details['udpdst']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example33-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['dst_full']
                        jsonfile['criteria'][2]['udpPort'] = details['udpdst']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Ps(tcp), v
                if mode == "onos":
                    with codecs.open('resources/example34.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        jsonfile['selector']['criteria'][1]['vlanid'] = details['vlanid']
                        #jsonfile['selector']['criteria'][0]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][0]['tcpPort'] = details['tcpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example34-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['tcpPort'] = details['tcpsrc']
                        jsonfile['criteria'][2]['vlanid'] = details['vlanid']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Pd(tcp), Ps(tcp)
                if mode == "onos":
                    with codecs.open('resources/example35.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        #jsonfile['selector']['criteria'][0]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][0]['tcpPort'] = details['tcpdst']
                        jsonfile['selector']['criteria'][1]['tcpPort'] = details['tcpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example35-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['tcpPort'] = details['tcpdst']
                        jsonfile['criteria'][2]['tcpPort'] = details['tcpsrc']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Pd(udp), Ps(tcp)
                if mode == "onos":
                    with codecs.open('resources/example36.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][0]['vlanid'] = details['vlanid']
                        #jsonfile['selector']['criteria'][0]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][0]['udpPort'] = details['udpdst']
                        jsonfile['selector']['criteria'][1]['tcpPort'] = details['tcpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example36-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['udpPort'] = details['udpdst']
                        jsonfile['criteria'][2]['tcpPort'] = details['tcpsrc']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Pd(tcp), v
                if mode == "onos":
                    with codecs.open('resources/example37.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        jsonfile['selector']['criteria'][1]['vlanid'] = details['vlanid']
                        #jsonfile['selector']['criteria'][0]['mac'] = details['dst_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        jsonfile['selector']['criteria'][0]['tcpPort'] = details['tcpdst']
                        #jsonfile['selector']['criteria'][1]['tcpPort'] = details['tcpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example37-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['tcpPort'] = details['tcpdst']
                        jsonfile['criteria'][2]['vlanid'] = details['vlanid']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Es, Ed, v
                if mode == "onos":
                    with codecs.open('resources/example38.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        jsonfile['selector']['criteria'][2]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                        jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        #jsonfile['selector']['criteria'][0]['udpPort'] = details['udpdst']
                        #jsonfile['selector']['criteria'][1]['tcpPort'] = details['tcpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example38-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['src_full']
                        jsonfile['criteria'][2]['mac'] = details['dst_full']
                        jsonfile['criteria'][3]['vlanid'] = details['vlanid']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Es, Ed, Ps(tcp)
                if mode == "onos":
                    with codecs.open('resources/example39.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][2]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                        jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        #jsonfile['selector']['criteria'][0]['udpPort'] = details['udpdst']
                        jsonfile['selector']['criteria'][2]['tcpPort'] = details['tcpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example39-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['src_full']
                        jsonfile['criteria'][2]['mac'] = details['dst_full']
                        jsonfile['criteria'][3]['tcpPort'] = details['tcpsrc']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)
                
                #ip, Es, Ed, Ps(udp)
                if mode == "onos":
                    with codecs.open('resources/example40.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][2]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                        jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        #jsonfile['selector']['criteria'][0]['udpPort'] = details['udpdst']
                        jsonfile['selector']['criteria'][2]['udpPort'] = details['udpsrc']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example40-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['src_full']
                        jsonfile['criteria'][2]['mac'] = details['dst_full']
                        jsonfile['criteria'][3]['udpPort'] = details['udpsrc']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)

                #ip, Es, Ed, Pd(tcp)
                if mode == "onos":
                    with codecs.open('resources/example41.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][2]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                        jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        #jsonfile['selector']['criteria'][0]['udpPort'] = details['udpdst']
                        jsonfile['selector']['criteria'][2]['tcpPort'] = details['tcpdst']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)
                
                if mode == "manual":
                    with codecs.open('resources/example41-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['src_full']
                        jsonfile['criteria'][2]['mac'] = details['dst_full']
                        jsonfile['criteria'][3]['tcpPort'] = details['tcpdst']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)

                #ip, Es, Ed, Pd(udp)
                if mode == "onos":
                    with codecs.open('resources/example42.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['ingressPoint']['port'] = str(i)
                        jsonfile['egressPoint']['port'] = str(j)
                        #jsonfile['selector']['criteria'][2]['vlanid'] = details['vlanid']
                        jsonfile['selector']['criteria'][1]['mac'] = details['dst_full']
                        jsonfile['selector']['criteria'][0]['mac'] = details['src_full']
                        #jsonfile['selector']['criteria'][2]['ip'] = details['ipsrc']
                        #jsonfile['selector']['criteria'][3]['ip'] = details['ipdst']
                        #jsonfile['selector']['criteria'][0]['udpPort'] = details['udpdst']
                        jsonfile['selector']['criteria'][2]['udpPort'] = details['udpdst']
                    r = requests.post(url = URL, auth = AUTH, data = json.dumps(jsonfile), headers = HEADERS)

                if mode == "manual":
                    with codecs.open('resources/example42-manual.json', "r", encoding="utf-8") as newrule:
                        jsonfile = json.load(newrule)
                        jsonfile['criteria'][0]['port'] = i
                        jsonfile['instruction'][0]['port'] = str(j)
                        jsonfile['criteria'][1]['mac'] = details['src_full']
                        jsonfile['criteria'][2]['mac'] = details['dst_full']
                        jsonfile['criteria'][3]['udpPort'] = details['udpdst']
                        jsonfile['id'] = str('{:017x}'.format(count+1))
                        count += 1
                        print(json.dumps(jsonfile))
                        rules.append(jsonfile)

            #range1_new = int(range1_new) + j
        #range2_new = int(range2_new) +i

def EMEC_focused(num, range1, range2, rules, mode):
    generateIntents_k1_complete(num, count, rules, mode)

def SUBEC_focused(num, range1, range2, rules, mode):
    generateIntents_SUBEC_focused(num, count, rules, mode)

def OLEC_focused(num, range1, range2, rules, mode):
    generateIntents_ip_complete(num, count, rules, mode)

def PD1(num,range1,range2):
    generateIntents_k1(num, range1, range2)
    generateIntents_k2_mac(num, range1, range2)
    generateIntents_k3_mac(num, range1, range2)
    generateIntents_k4_ip(num, range1, range2)
    generateIntents_k5_ip(num, range1, range2)
    generateIntents_k6_ip(num, range1, range2)
    generateIntents_k8_tcpPort(num, range1, range2)
    generateIntents_k7_tcpPort(num, range1, range2)
    generateIntents_k9_rev(num, range1, range2)
    generateIntents_fwd(num, range1, range2)
    generateIntents_routing(num, range1, range2)
    generateIntents_acl(num, range1, range2)

#Stanford topo
def PD2(num,range1,range2):
    generateIntents_k8_tcpPort(num, range1, range2)
    generateIntents_k9_rev(num, range1, range2)
    generateIntents_k1(num, range1, range2)
    generateIntents_k2_mac(num, range1, range2)
    generateIntents_k3_mac(num, range1, range2)
    generateIntents_k3_mac(num, range1, range2)
    generateIntents_k4_ip(num, range1, range2)
    generateIntents_k8_tcpPort(num, range1, range2)
    generateIntents_k5_ip(num, range1, range2)
    generateIntents_k6_ip(num, range1, range2)
    generateIntents_k7_tcpPort(num, range1, range2)
    generateIntents_k3_mac(num, range1, range2)
    generateIntents_fwd(num, range1, range2)
    generateIntents_routing(num, range1, range2)
    generateIntents_acl(num, range1, range2)

def PD3(num,range1,range2):
    for i in range(10):
        PD1(num,range1,range2)

def PD4(num,range1,range2):
    for i in range(10):
        PD2(num,range1,range2)

def PD_ACL(num,range1,range2):
    for i in range(10):
        generateIntents_acl(num,range1,range2)

def PD_fwd(num,range1,range2):
    for i in range(10):
        generateIntents_fwd(num,range1,range2)

def PD_routing(num,range1,range2):
    for i in range(10):
        generateIntents_routing(num,range1,range2)

if __name__ == "__main__":
     main(sys.argv[1:])
         #main()
