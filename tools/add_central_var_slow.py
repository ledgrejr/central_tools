#!/usr/bin/env python3

import argparse
import datetime
import json
import tempfile
import requests
import yaml

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

pre_check_dict = {}
post_check_dict = {}

def get_variables (central_info,serial):
    s = requests.Session()

    retries = Retry(total=5,
    backoff_factor=1,
    status_forcelist=[ 502, 503, 504 ])

    access_token = central_info['token']['access_token']
    base_url = central_info['base_url']
    api_function_url = base_url + "configuration/v1/devices/{0}/template_variables".format(serial)
    qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
    }

    qparams = {
      "device_serial": serial,
    }

    response = s.request("GET", api_function_url, headers=qheaders, params=qparams)
    if "error" in response.json():
      print(response.text)
      exit()
      return "{'ERROR'}"
    else:
      new_variable_dict = {}
    new_variable_dict[serial] = response.json()['data']['variables']
    return new_variable_dict


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


def p_check(central, fname):

  p_check_dict = {}

  f = open(fname,"r")
  content = f.readlines()
  for line in content:
    print("Getting variables for ",line.strip())
    return_dict = get_variables (central,line.strip())
    p_check_dict.update(return_dict)
  f.close()
  return(p_check_dict)

parser = argparse.ArgumentParser()
parser.add_argument('--token', \
                     required=True, \
                     help='Central Tools user ID to use for API access')
parser.add_argument('--url', \
                     default = 'https://apigw-thdnaas.central.arubanetworks.com/')
parser.add_argument('--custID', \
                     required=True)
parser.add_argument('--infile', \
                     help='Input file containing the serials of target devices. This prempts group selection via CLI.')
parser.add_argument('--variable', \
                     required=True, \
                     help='Variable to create')
parser.add_argument('--value', \
                     default = 'dummy', \
                     help='Value to assign to variable')
args = parser.parse_args()
new_var = args.variable
new_value = args.value
custID = args.custID
token = args.token
url = args.url

#for debug 
central_info = {'base_url': url, 'customer_id': custID, 'token': {'access_token': token}}

ssl_verify=True
    
data_dict = []

print("Running pre-check. This is going to take some time.")
print("You might want to go see all of the LOTR movies.....")
pre_check_dict = p_check(central_info, args.infile)

pre_check_fname = "pre_check." + args.infile 
with open(pre_check_fname, 'w') as file:
#     file.write(json.dumps(pre_check_dict))
     file.write(yaml.dump(pre_check_dict, default_flow_style=False))
print("----------------------------------------------------")
print("Pre-check results written to file ",pre_check_fname)
print("----------------------------------------------------")

if args.infile is not None:
  print("Load the input file: ",args.infile)
  f = open(args.infile,"r")
  content = f.readlines()

  my_json = json.dumps(pre_check_dict)
  
  for line in content:
     serial = line.strip()
     print("Serial #:",serial)
     macaddr = pre_check_dict[serial]['_sys_lan_mac']
     list1 = [{'macaddr': macaddr, 'serial': serial}]
     data_dict.extend(list1)
   
else:
  print("You must supply an input file consisting of device serials (one per line) to run this tool.....")
  exit()

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
      tfile = tempfile.NamedTemporaryFile(mode="w+",delete=True)
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
tfile = tempfile.NamedTemporaryFile(mode="w+",delete=True)
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
print("Adding/updating variable",new_var," to supplied list of serials in ",args.infile) 
  
print("With value               : ",new_value)

print("Running post-check. You know those LOTR movies, go watch them again")
print("and I will be done when you get back....I hope")
post_check_dict = p_check(central_info, args.infile)

post_check_fname = "post_check." + args.infile 
with open(post_check_fname, 'w') as file:
     file.write(json.dumps(post_check_dict))
print("----------------------------------------------------")
print("Post-check results written to file ",post_check_fname)
print("----------------------------------------------------")


