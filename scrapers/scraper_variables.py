#!/usr/bin/env python3

import argparse
import datetime
import mysql.connector
import json
import requests
import copy
import re
from pycentral.base import ArubaCentralBase
from pycentral.configuration import Variables
from central_test_mysql import test_central

def get_variables (central,serial):
    v = Variables()
    new_variable_dict = {}

    response = v.get_template_variables(central,serial)
    
    new_variable_dict[serial] = response['msg']['data']['variables']
#    print(new_variable_dict)
    return new_variable_dict

def get_all_variables (central,loop_limit=0):
    """ Return a full list of variables for all devices """
    print ("Getting Variables - Will Take Some time")
    # set initial vars
    limit =20 
    v = Variables()
    full_variable_dict = {}

    # loop through call to get groups appending groups to full group list
    # stop when response is empty
    counter = 0
    need_more =  True

    while need_more:
        response = v.get_all_template_variables(central,offset=counter,limit=limit)
#        print(response)
        if (response['code'] == 200):
          if response['msg'] != {}:
              full_variable_dict.update(response['msg'])
          elif response['msg'] == {}:
              need_more = False
              break
          else:
              print("ERROR")
              need_more = False
              print(response)
              break
          counter = counter + limit
          print(counter,"Response: ",response['code'])
        elif (response['code'] == 500):
           print("Internal error...trying again")
        else: 
           print(response)

#exit the function after loop_limit runs...for testing 
        if (loop_limit != 0):
          if (loop_limit <= counter):
            need_more = False
    return full_variable_dict

#----------------------------------
# MAIN()
#----------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--userID', \
                    default = 'scraper', \
                    help='Central Tools user ID to use for API access')
args = parser.parse_args()
userID = args.userID
print("Accessing API as " + userID)
central_info = test_central(userID)
print("--------------")
print(central_info)
print("--------------")

ssl_verify=True
# set Central data
central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
    
# get all device variables - this call takes some time
data_dict = get_all_variables (central)
#for testing, uncomment the next line and comment the above line
#data_dict = get_variables (central,'CNMDKD50Q1')
#print(data_dict)
cnx = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')
cursor = cnx.cursor()
# iterate all the nested dictionaries with keys
for i in data_dict:
  # display
    serial = i 
#    print(serial)
#    print(data_dict[i])
    for j in data_dict[i]:
      variable_name = j
      if (j == "description"):
         print("*************************")
         print("INTERNAL SERVER ERROR ")
         print(serial)
         print(data_dict[i])
         print("*************************")
      else: 
        if (isinstance(data_dict[i][j],str)):
#          print("is string")
          value = re.sub(r'\\$','',data_dict[i][j])
        else:
#          print("is snot tring")
          value = data_dict[i][j]
        if (value == "'"):
          value = "\"\""
      

        queryU1 = "INSERT INTO central_tools.variables (variable_name,customer_id,value,serial,last_refreshed) VALUES ('{0}','{1}','{2}','{3}',now())".format(variable_name,central_info['customer_id'],value,serial)
        query = queryU1 + " ON DUPLICATE KEY UPDATE  value = '{0}', last_refreshed = now()".format(value)

#        print(query)

        cursor.execute(query)
        cnx.commit()
      
# remove any old variables over 7 days old
#      query = "DELETE FROM central_tools.variables WHERE last_refreshed < now() - INTERVAL 7 day"
#      cursor.execute(query)
#      cnx.commit()
       
cursor.close()
cnx.close()
