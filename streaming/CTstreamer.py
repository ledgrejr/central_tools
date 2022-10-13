#!/usr/bin/env python3
# MIT License
#
# Portions Copyright (c) 2019 Aruba, a Hewlett Packard Enterprise company
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import datetime
import mysql.connector
import time
import json
import ssl
import websocket
import requests
import socket
import _thread
import sys
import os
import atexit
import signal
from signal import SIGTERM
from enum import Enum
from proto import streaming_pb2
from proto import monitoring_pb2
from pprint import pprint
from google.protobuf.json_format import MessageToDict
import google.protobuf.message
import google.protobuf
import base64


# -- generic daemon base class ------------------------------------------ #

class daemon_base:
	"""A generic daemon base class.
	
	Usage: subclass this class and override the run() method.
	"""
	def __init__(self, pidfile, workpath='/'):
		"""Constructor.

		We need the pidfile for the atexit cleanup method.
		The workpath is the path the daemon will operate
		in. Normally this is the root directory, but can be some
		data directory too, just make sure it exists.
		"""
		self.pidfile = pidfile
		self.workpath = workpath
	
	def perror(self, msg, err):
		"""Print error message and exit. (helper method)
		"""
		msg = msg + '\n'
		sys.stderr.write(msg.format(err))
		sys.exit(1)

	def daemonize(self):
		"""Deamonize calss process. (UNIX double fork mechanism).
		"""
		if not os.path.isdir(self.workpath):
			self.perror('workpath does not exist!', '')

		try: # exit first parent process
			pid = os.fork() 
			if pid > 0: sys.exit(0) 
		except OSError as err:
			self.perror('fork #1 failed: {0}', err)
	
		# decouple from parent environment
		try: os.chdir(self.workpath)
		except OSError as err:
			self.perror('path change failed: {0}', err)

		os.setsid() 
		os.umask(0) 
	
		try: # exit from second parent
			pid = os.fork() 
			if pid > 0: sys.exit(0) 
		except OSError as err:
			self.perror('fork #2 failed: {0}', err)
	
		# redirect standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = open(os.devnull, 'r')
		so = open(os.devnull, 'a+')
#		so = open("/tmp/CTstreamer.txt", 'a+')
#		se = open(os.devnull, 'a+')
		se = open("/tmp/CTstreamer.error", 'a+')
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
	
		# write pidfile
		atexit.register(os.remove, self.pidfile)
		pid = str(os.getpid())
		with open(self.pidfile,'w+') as f:
			f.write(pid + '\n')
		self.run()
	
	def run(self):
		"""Worker method.
		
		It will be called after the process has been daemonized
		by start() or restart(). You'll have to overwrite this
		method with the daemon program logic.
		"""
		while True:
			time.sleep(1)

# -- daemon control class ----------------------------------------------- #

class daemon_ctl:
	"""Control class for a daemon.

	Usage:
	>>>	dc = daemon_ctl(daemon_base, '/tmp/foo.pid')
	>>>	dc.start()

	This class is the control wrapper for the above (daemon_base)
	class. It adds start/stop/restart functionality for it withouth
	creating a new daemon every time.
	"""
	def __init__(self, daemon, pidfile, workdir='/'):
		"""Constructor.

		@param daemon: daemon class (not instance)
		@param pidfile: daemon pid file
		@param workdir: daemon working directory
		"""
		self.daemon = daemon
		self.pidfile = pidfile
		self.workdir = workdir
	
	def start(self):
		"""Start the daemon.
		"""
		try: # check for pidfile to see if the daemon already runs
			with open(self.pidfile, 'r') as pf:
				pid = int(pf.read().strip())
		except IOError: pid = None
	
		if pid:
			message = "pidfile {0} already exist. " + \
					"Daemon already running?\n"
			sys.stderr.write(message.format(self.pidfile))
			sys.exit(1)
		
		# Start the daemon
		d = self.daemon(self.pidfile, self.workdir)
		d.daemonize()

	def stop(self):
		"""Stop the daemon.

		This is purely based on the pidfile / process control
		and does not reference the daemon class directly.
		"""
		try: # get the pid from the pidfile
			with open(self.pidfile,'r') as pf:
				pid = int(pf.read().strip())
		except IOError: pid = None
	
		if not pid:
			message = "pidfile {0} does not exist. " + \
					"Daemon not running?\n"
			sys.stderr.write(message.format(self.pidfile))
			return # not an error in a restart

		try: # try killing the daemon process	
			while 1:
				os.kill(pid, signal.SIGTERM)
				time.sleep(0.1)
		except OSError as err:
			e = str(err.args)
			if e.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print (str(err.args))
				sys.exit(1)

	def restart(self):
		"""Restart the daemon.
		"""
		self.stop()
		self.start()


msgProcessed = {} 

class monitoring_data_elements(Enum):
	STATE_CONTROLLER = 1
	STATE_SWITCH = 2
	STATE_SWARM = 3
	STATE_AP = 4
	STATE_VAP = 5
	STATE_RADIO = 6
	STATE_INTERFACE = 7
	STATE_NETWORK = 8
	STATE_TUNNEL = 9
	STATE_WIRELESSCLIENT = 10
	STATE_WIREDCLIENT = 11
	STATE_UPLINK = 12
	STAT_DEVICE = 13
	STAT_RADIO = 14
	STAT_VAP = 15
	STAT_INTERFACE = 16
	STAT_CLIENT = 17
	STAT_TUNNEL = 18
	STAT_MODEM = 19
	STAT_ROLE = 20
	STAT_VLAN = 21
	STAT_SSID = 22
	STAT_IPPROBE = 23
	STAT_UPLINK = 24
	STAT_UPLINKWAN = 25
	STAT_UPLINKIPPROBE = 26
	EVENTS_WIDS = 27
	EVENTS_ROGUE = 28
	STATS_UPLINK_SPEEDTEST = 29
	DEVICE_NEIGHBOURS = 30
	NOTIFICATIONS = 31
	SWITCH_STACK = 32
	STATE_IKE_TUNNEL = 33
	SWITCH_VLAN = 34
	STATE_VLAN = 35
	STATE_VSX = 36

def unpackIP(packedIP):
    address=base64.b64decode(packedIP)
    strIP = str(address[0]) + "." + str(address[1]) + "." + str(address[2]) + "." + str(address[3])
    return(strIP)

def unpackMAC(packedMAC):
    address=base64.b64decode(packedMAC)
    strMAC = '{:02x}'.format(address[0]) + ":" + '{:02x}'.format(address[1]) + ":" + '{:02x}'.format(address[2]) + ":" + '{:02x}'.format(address[3]) + ":" + '{:02x}'.format(address[4]) + ":" + '{:02x}'.format(address[5])
    return(strMAC)

def processInterfaceMsg(customer_id, dict_obj):

  int_speed_lkup = { 'SPEED_AUTO':'AUTO', 'SPEED_INVALID': 'INVALID','SPEED_10':'10','SPEED_100':'100','SPEED_1000':'1000','SPEED_10000':'10000','SPEED_2500':'2500'}
  has_Poe_lkup = { 'SUPPORTED' : 1, "NOT_SUPPORTED":0 }
  vlan_mode_lkup = { 'ACCESS':0,'NATIVE_UNTAGGED' : 1}

  for i in dict_obj['interfaces']:
    if 'INTERFACE' in msgProcessed:
      msgProcessed['INTERFACE'] = msgProcessed['INTERFACE'] + 1 
    else:
      msgProcessed['INTERFACE'] = 1
    serial = i['deviceId']
    if 'name' in i:
      port_number = i['name']
    else:
      port_number = ""
    port = i['portNumber']
    status = i['status']
    if 'duplexMode' in i:
      duplex_mode = i['duplexMode']
    else:
      duplex_mode = ""
    macaddr = unpackMAC(i['macaddr']['addr'])
    type = i['type']
    if type != 'BRIDGE':
      if 'mode' in i:
        mode = i['mode']
      else:
        mode = ""
      if 'hasPoe' in i:
        has_poe = has_Poe_lkup[i['hasPoe']]
      else:
        has_pos = 0
      trusted = i['trusted']
      intf_state_down_reason = i['stateDownReason']
      vlan_mode = vlan_mode_lkup[i['vlanMode']]
    else:
      mode = ''
      has_poe = 0
      trusted = 0
      intf_state_down_reason = ""
      vlan_mode = 0;
    oper_state = i['operState']
    admin_state = i['adminState']
    if 'speed' in i:
      speed = int_speed_lkup[i['speed']]
    else:
      speed = 'NA'
    if 'allowedVlan' in i:
      allowed_vlan = i['allowedVlan']
    else:
      allowed_vlan = '[]'

    cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
    cursor = cnx.cursor()

    queryU1 = "INSERT INTO central_tools.ports ( \
                serial, \
                macaddr, \
                port_number, \
                status, \
                duplex_mode, \
                type, \
                mode, \
                has_poe, \
                trusted, \
                intf_state_down_reason, \
                vlan_mode, \
                oper_state, \
                admin_state, \
                speed, \
                allowed_vlan, \
                port, \
                customer_id, \
                last_refreshed) \
                VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}',{7},{8},'{9}',{10},'{11}','{12}','{13}','{14}',{15},'{16}', \
                 now())".format( \
                serial, \
                macaddr, \
                port_number, \
                status, \
                duplex_mode, \
                type, \
                mode, \
                has_poe, \
                trusted, \
                intf_state_down_reason, \
                vlan_mode, \
                oper_state, \
                admin_state, \
                speed, \
                allowed_vlan, \
                port, \
                customer_id)
                               
    query = queryU1 + "ON DUPLICATE KEY UPDATE \
                serial = '{0}', \
                macaddr = '{1}', \
                port_number = '{2}', \
                status = '{3}', \
                duplex_mode = '{4}', \
                type = '{5}', \
                mode = '{6}', \
                has_poe = {7}, \
                trusted = {8}, \
                intf_state_down_reason = '{9}', \
                vlan_mode = {10}, \
                oper_state = '{11}', \
                admin_state = '{12}', \
                speed = '{13}', \
                allowed_vlan = '{14}', \
                port = {15}, \
                customer_id = '{16}', \
                last_refreshed = now()".format( \
                serial, \
                macaddr, \
                port_number, \
                status, \
                duplex_mode, \
                type, \
                mode, \
                has_poe, \
                trusted, \
                intf_state_down_reason, \
                vlan_mode, \
                oper_state, \
                admin_state, \
                speed, \
                allowed_vlan, \
                port, \
                customer_id)

#    print("QUERY ------------------------")
#    print(query)
#    print("QUERY ------------------------")

    cursor.execute(query)
    cnx.commit()

def processAPMsg(customer_id, dict_obj):

  boolean_lkup = { 'FALSE' : 0, "TRUE":1 }

  for i in dict_obj['aps']:
    if 'AP' in msgProcessed:
      msgProcessed['AP'] = msgProcessed['AP'] + 1
    else:
      msgProcessed['AP'] = 1
    serial = i['serial']
    if 'name' in i:
     name = i['name']
    else:
      name = ""
    macaddr = unpackMAC(i['macaddr']['addr'])
    swarm_id = i['clusterId']
    status = i['status']
    if 'ipAddress' in i:
      ip_address = unpackIP(i['ipAddress']['addr'])
    else:
      ip_address = ""
    model = i['model']
    mesh_role = i['meshRole']
    if 'mode' in i:
      mode = i['mode']
    else:
      mode = ""
    swarm_master = i['swarmMaster']
    modem_connected = i['modemConnected']
    if 'uplinkType' in i:
      uplink_type = i['uplinkType']
    else:
      uplink_type = ""
     
    firmware_version = i['firmwareVersion']
    
    cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
    cursor = cnx.cursor()

    queryU1 = "INSERT INTO central_tools.aps ( \
                serial, \
                name, \
                macaddr, \
                swarm_id, \
                status, \
                ip_address, \
                model, \
                mesh_role, \
                mode, \
                swarm_master, \
                modem_connected, \
                uplink_type, \
                firmware_version, \
                customer_id, \
                last_refreshed) \
                VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},'{11}','{12}','{13}', \
                 now())".format( \
                serial, \
                name, \
                macaddr, \
                swarm_id, \
                status, \
                ip_address, \
                model, \
                mesh_role, \
                mode, \
                swarm_master, \
                modem_connected, \
                uplink_type, \
                firmware_version, \
                customer_id)
                               
    query = queryU1 + "ON DUPLICATE KEY UPDATE \
                serial = '{0}', \
                name = '{1}', \
                macaddr = '{2}', \
                swarm_id = '{3}', \
                status = '{4}', \
                ip_address = '{5}', \
                model = '{6}', \
                mesh_role = '{7}', \
                mode = '{8}', \
                swarm_master = {9}, \
                modem_connected = {10}, \
                uplink_type = '{11}', \
                firmware_version = '{12}', \
                customer_id = '{13}', \
                last_refreshed = now()".format( \
                serial, \
                name, \
                macaddr, \
                swarm_id, \
                status, \
                ip_address, \
                model, \
                mesh_role, \
                mode, \
                swarm_master, \
                modem_connected, \
                uplink_type, \
                firmware_version, \
                customer_id)


#    print("QUERY ------------------------")
#    print(query)
#    print("QUERY ------------------------")

    cursor.execute(query)
    cnx.commit()


def processSwitchMsg(customer_id, dict_obj):
  for i in dict_obj['switches']:
    if 'SWITCH' in msgProcessed:
      msgProcessed['SWITCH'] = msgProcessed['SWITCH'] + 1
    else:
      msgProcessed['SWITCH'] = 1
    serial = i['serial']
    macaddr = unpackMAC(i['macaddr']['addr'])
    name = i['name']
    model = i['model']
    status = i['status']
    firmware_version = i['firmwareVersion']
    device_mode = i['deviceMode']
    if 'powerSupplies' in i:
      powerSupplies = i['powerSupplies']
    else:
      powerSupplies = '{}'
    stack_id = i['stackId']
    stack_member_id = i['stackMemberId']
    stackMemberRole = i['stackMemberRole']

    if i['stackMemberRole'] == 'COMMANDER':
      if 'ipAddress' in i:
        ip_address = unpackIP(i['ipAddress']['addr'])
      else:
        ip_address = ""
      if 'publicIpAddress' in i:
        public_ip_address = unpackIP(i['publicIpAddress']['addr'])
      else:
        public_ip_addres = ""
    else:
      ip_address = ""
      public_ip_address = ""
    cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
    cursor = cnx.cursor()
   
    queryU1 = "INSERT INTO central_tools.switches ( \
                serial, \
                name, \
                macaddr, \
                model, \
                status, \
                public_ip_address, \
                ip_address, \
                firmware_version, \
                device_mode, \
                stack_id, \
                customer_id, \
                last_refreshed) \
                VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}', \
                 now())".format( \
                serial, \
                name, \
                macaddr, \
                model, \
                status, \
                public_ip_address, \
                ip_address, \
                firmware_version, \
                device_mode, \
                stack_id, \
                customer_id)

    query = queryU1 + "ON DUPLICATE KEY UPDATE \
                serial = '{0}', \
                name = '{1}', \
                macaddr = '{2}', \
                model = '{3}', \
                status = '{4}', \
                public_ip_address = '{5}', \
                ip_address = '{6}', \
                firmware_version = '{7}', \
                device_mode = '{8}', \
                stack_id = '{9}', \
                customer_id = '{10}', \
		last_refreshed = now()".format( \
                serial, \
                name, \
                macaddr, \
                model, \
                status, \
                public_ip_address, \
                ip_address, \
                firmware_version, \
                device_mode, \
                stack_id, \
                customer_id)

#    print("------------------------")
#    print(query)
#    print("------------------------")

    cursor.execute(query)
    cnx.commit()


def on_message(ws, message):
    # Decode Message in Serialized protobuffer
    stream_data = streaming_pb2.MsgProto()
    stream_data.ParseFromString(message)
    # Based on the topic import compiled proto file and decode 'data' field
    monitoring_data = monitoring_pb2.MonitoringInformation()
    monitoring_data.ParseFromString(stream_data.data)
    dict_obj = MessageToDict(monitoring_data)

#    print(msgProcessed)

#    if set(monitoring_data.data_elements).issubset((2,4,5,7,32,36)):
    if set(monitoring_data.data_elements).issubset((2,4,7)):
      customer_id = str(stream_data.customer_id)
#      print("Data Elements : ")
#      for i in monitoring_data.data_elements:
#       print("------",monitoring_data_elements(i))
      if 4 in monitoring_data.data_elements:
#         print("processed AP message....")
         processAPMsg(customer_id,dict_obj)
      if 5 in monitoring_data.data_elements:
         for i in dict_obj['vaps']:
           print("VAPs :",i)
           print(i['deviceId'])
      if 2 in monitoring_data.data_elements:
#         print("processed switch message....")
         processSwitchMsg(customer_id,dict_obj)
      if 7 in monitoring_data.data_elements:
#         print("processed interface message....")
         processInterfaceMsg(customer_id,dict_obj)
      if 32 in monitoring_data.data_elements:
         for i in dict_obj['switchStacks']:
           print("Switch Stacks :", i)
      if 36 in monitoring_data.data_elements:
         for i in dict_obj['vsx']:
           print(i['serial'])
           print("VSX :",i)

def on_error(ws, error):
    print("ERROR:",error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        print("Start Streaming Data!")
    _thread.start_new_thread(run, ())

def validate_refresh_token(hostname, oldtok):
    """
    This function is to validate WebSocket Key. A HTTP request to Aruba Central
    is made to validate and fetch the current WebSocket key.
    Input:
        hostname: Base URL from Endpoint in Streaming API page of Aruba Central.
        oldtok: Streaming API WebSocket Key.
    Returns:
        token (str): The function returns the unexpired token. It might be same
                     as the provided token if its unexpired.
        None: If unable to fetch the token
    """
    url = "https://{}/streaming/token/validate".format(hostname)
    headers = { "Authorization" : oldtok }
    print("Validating wss key....\n")
    try:
      res = requests.get(url, headers=headers)
      print(res)
      if res.status_code == 200:
#        print("new token : {}".format(res.json()["token"]))
        return res.json()["token"]
        return None
    except Exception as err:
        print("Unable to validate/refresh WSS key ...")
        return None

def startStream():
    # URL for WebSocket Connection from Streaming API page
    hostname = "app-thdnaas.central.arubanetworks.com"
    username = "michael.gresham@hpe.com"
    token = "eyJhbGciOiJIUzI1NiIsInR5cGUiOiJqd3QifQ.eyJjdXN0b21lcl9pZCI6ImQ1OTNiNjhkMmEyMjRmYjRiNzZjZTdiNTcyMjg5Njc4IiwiY3JlYXRpb25fZGF0ZSI6MTY2NDIzNjkzMn0.PIQfiwGg3EKxc3wgIDdIz2IdNvXKsTPuh_FX0g0Pu6A"
    url = "wss://{}/streaming/api".format(hostname)

    token = validate_refresh_token(hostname,token)

    # Construct Header for WebSocket Connection
    header = {}
    # Central User email
    header["UserName"] = username
    # WebSocket Key from Streaming API Page
    header["Authorization"] = token
    # Subscription TOPIC for Streaming API
    # (audit|apprf|location|monitoring|presence|security)
    header["Topic"] = "monitoring"
    # Create WebSocket connection
#    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url=url,
                                header=header,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
#    ws.run_forever()
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

class myDaemon(daemon_base):
    def run(self):
      startStream()

class myDaemonCTL(daemon_ctl):
    def status(self):
      try: # check for pidfile to see if the daemon already runs
        with open(self.pidfile, 'r') as pf:
          pid = int(pf.read().strip())
      except IOError: pid = None
	
      if pid:
        print("CTstreamer daemon is running")
      else:
        print("CTstreamer daemon is not running")
        


if __name__ == "__main__":
        usage = 'Missing parameter, usage of test logic:\n' + \
                        ' % python3 CTstreamer.py start|restart|stop\n'
        if len(sys.argv) < 2:
                sys.stderr.write(usage)
                sys.exit(2)

        pidfile = '/tmp/CTstreamer.pid'
        dc = myDaemonCTL(myDaemon, pidfile)

        if sys.argv[1] == 'start':
          dc.start()
        elif sys.argv[1] == 'stop':
          dc.stop()
        elif sys.argv[1] == 'restart':
          dc.restart()
        elif sys.argv[1] == 'status':
          dc.status()
        elif sys.argv[1] == 'standalone':
          startStream()
