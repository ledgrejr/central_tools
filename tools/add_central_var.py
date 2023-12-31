#!/usr/bin/env python3

import argparse
import datetime
import mysql.connector
import json
import tempfile
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import re
import time 

from pycentral.base import ArubaCentralBase
#from pycentral.configuration import Groups
from central_test_mysql import test_central

def sqlescape(string):
   if (string == None):
     return ""
   else:
     clean_str = string.translate(string.maketrans({
            "\0": "\\0",
            "\r": "\\r",
            "\x08": "\\b",
            "\x09": "\\t",
            "\x1a": "\\z",
            "\n": "\\n",
            "\r": "\\r",
            "\"": "",
            "'": "''",
            "\\": "\\\\",
            "%": "\\%"
        }))
     return clean_str

def sqlboolean(bool_val):
   return(int(bool_val == True))

def set_variable (central_info, fname):

#**********************************
#make API call to add the variables
#**********************************
  access_token = central_info['token']['access_token']
  base_url = central_info['base_url']
  api_url = base_url + "/configuration/v1/devices/template_variables"
  print(fname.name)

# do not put 'Content-Type': 'application/json' in the headers.  It will cause form data errors
  qheaders={
        "Authorization": "Bearer " + access_token,
           }
  qparams={}
  qpayload={}
  qfiles = {'variables':open(fname.name,'rb')}

# call the API and send the template file to the group
  response = requests.request("PATCH", api_url, params=qparams, headers=qheaders, data=qpayload, files=qfiles)
#  print("----------------")
#  print(response)
#  print("----------------")
  if (response.status_code == 200):   
     print("Successfully created/updated variable")
  elif (response.status_code == 401): # authentication timed out
          print("Access token expired.  Re-authenticating and retrying")
  elif (response.status_code == 500):
          print("Internal server error")
  return(response)

def get_macaddr (central,serial):

    cnx2 = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
    cursor2 = cnx2.cursor()

    query = "SELECT macaddr,serial,model,device_type FROM central_tools.devices \
             WHERE serial = '{0}' AND customer_id = '{1}'".format(serial,central['customer_id']); 
    cursor2.execute(query)
    row_headers=[x[0] for x in cursor2.description] #this will extract row headers
#    print(query)
    rv = cursor2.fetchall()
#    print(rv)
    dict_data=[]
    for result in rv:
      row_result = dict(zip(row_headers,result))
      print(row_result)
      dict_data.append(row_result)

#      print("====================")
#      print(dict_data)
#      print("====================")

    cursor2.close()
    cnx2.close()
    return dict_data

def get_cid_inventory (central,type,group):

    cnx2 = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
    cursor2 = cnx2.cursor()

    if (group == 'ALL'):
      query = "SELECT macaddr,serial,model,device_type \
            FROM central_tools.devices\
            WHERE device_type = '{0}' AND\
            customer_id = '{1}'".format(type,central['customer_id']); 
    else:
      query = "SELECT macaddr,serial,model,device_type \
            FROM central_tools.devices\
            WHERE device_type = '{0}' AND\
            customer_id = '{1}' AND\
            group_name  = '{2}'".format(type,central['customer_id'],group); 

    cursor2.execute(query)
    row_headers=[x[0] for x in cursor2.description] #this will extract row headers
#    print(query)
    rv = cursor2.fetchall()
    dict_data=[]
    for result in rv:
      row_result = dict(zip(row_headers,result))
      print(row_result)
      dict_data.append(row_result)

#      print("====================")
#      print(dict_data)
#      print("====================")

    cursor2.close()
    cnx2.close()
    return dict_data

parser = argparse.ArgumentParser()
parser.add_argument('--dev_type', \
                     default = 'ALL', \
                     help='Options are: switch, all_ap, all_controllers, vgw, cap, others. Default is ALL device types.')
parser.add_argument('--userID', \
                     default = 'scraper', \
                     help='Central Tools user ID to use for API access')
parser.add_argument('--group', \
                     help='Group in which to create/update the variable')
parser.add_argument('--infile', \
                     help='Input file containing the serials of target devices. This prempts group selection via CLI.')
parser.add_argument('--variable', \
                     required=True, \
                     help='Variable to create')
parser.add_argument('--value', \
                     default = 'dummy', \
                     help='Value to assign to variable')
args = parser.parse_args()
dev_type = args.dev_type
group = args.group
new_var = args.variable
new_value = args.value
userID = args.userID

print("Accessing API as " + userID)
central_info = test_central(userID)
print("--------------")
print(central_info)
print("--------------")

ssl_verify=True
# set Central data
central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
    
data_dict = []
if args.infile is not None:
  print("Load the input file: ",args.infile)
  f = open(args.infile,"r")
  content = f.readlines()

  for line in content:
     print("Serial #:",line)
     list1 = get_macaddr(central_info,line.strip())
     print("************")
     print(list1)
     print("************")
     data_dict.extend(list1)
   
else:
  if args.group is None:
    print("You must either define a group or supply an input file to run this tool.....")
    exit()

  else:
    if dev_type == "switch":
      data_dict = get_cid_inventory(central_info,"SWITCH",group)
    if dev_type == "all_ap":
      data_dict = get_cid_inventory(central_info,"AP",group)
    if dev_type == "ALL":
      list1 = get_cid_inventory(central_info,"SWITCH",group)
#      print("list1 :",list1)
#      print("dict   :",dict)
      data_dict.extend(list1)
      list1 = get_cid_inventory(central_info,"AP",group)
      data_dict.extend(list1)

count = 0
count_batches = 1

temp_dict = {}
for x in data_dict:
   line = {}
   line['_sys_serial'] = x['serial']
   line['_sys_lan_mac'] = x['macaddr']
   line[new_var] = new_value
   temp_dict[x['serial']] = line

   count = count + 1
   if count == 1000:
#      print(temp_dict)
      print("STOP, Hammer time")
      tfile = tempfile.NamedTemporaryFile(mode="w+",delete=False)
      json.dump(temp_dict, tfile)
      tfile.flush()
      response = set_variable(central_info,tfile)
      if (response.status_code == 401): # authentication timed out
          central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
          response = set_variable(central_info,tfile)
      elif (response.status_code == 500):
          print("Internal server error. Exiting")
          exit()
      temp_dict = {}
      print(tfile.name)
      print("Total devices in file: ",count)   
      count_batches = count_batches + 1
      count = 1

# clean up any remaining records
tfile = tempfile.NamedTemporaryFile(mode="w+",delete=False)
#print(temp_dict)
json.dump(temp_dict, tfile)
tfile.flush()
response = set_variable(central_info,tfile)
if (response.status_code == 401): # authentication timed out
    central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
    response = set_variable(central_info,tfile)
elif (response.status_code == 500):
    print("Internal server error. Exiting")
    exit()

print("Total devices: ",count*count_batches)   
if args.group is not None:
  print("Adding/updating variable",new_var," to group",group)
else:
  print("Adding/updating variable",new_var," to supplied list of serials in ",args.infile) 
  
print("With value               : ",new_value)



