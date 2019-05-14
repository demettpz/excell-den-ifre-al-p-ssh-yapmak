import pandas as pd

import numpy as np

from getpass import getpass

from pandas import ExcelWriter
from pandas import ExcelFile
import xlsxwriter
import glob
import xlrd

from netmiko import ConnectHandler

import time


komut="sh run | i hostname"


excel_file = '12.xlsx'


# net_connect asagidaki formatta da gonderilebilir.
# net_connect = ConnectHandler(device_type='cisco_ios', ip='192.168.11.3', username='seyfi', password='xpass')

'''
cisco_881 = {
'device_type': 'cisco_ios',
'ip': 'x.x.x.x',
'username': 'xuser',
'password': 'xpass',
} 
'''

class netmiko_class:
	def __init__(self, komut, test):
		self.komut = komut
		self.test = test
		#self.enable = enable
		net_connect = ConnectHandler(**test)

#		net_connect = ConnectHandler(device_type='cisco_ios', ip='192.168.11.3', username='seyfi', password='Bltm1983') 

		net_connect.find_prompt()


		net_connect.enable()
		print(net_connect.find_prompt())
		output1 = net_connect.send_command(komut)
		print ("basarili " + output1)
		config_list = ['logging   host 192.168.139.65',
		'archive',
		 'log config',
		  'logging enable',
		  'notify syslog contenttype plaintext',
		 'path tftp://192.168.139.65/$h',
		 'write-memory',
		 'time-period 10080',
		 'end',
		 'write memory']
		net_connect.send_config_set(config_list)

			

print("print sheet names")



excel_data_frame = xlrd.open_workbook(excel_file, on_demand=True)
print (excel_data_frame.sheet_names())

sheet_names_array = excel_data_frame.sheet_names()

all_data = pd.DataFrame()

# sheet_names_array deki her bir eleman icin sheet i oku ve all_data icinde birlestir

for sayfa in sheet_names_array:
	df10 = pd.read_excel(excel_file, sheet_name=sayfa)
	all_data = all_data.append(df10,ignore_index=True, sort=True)


#
all_data_column = all_data.columns
print("Column headings:")
print(all_data_column)
'''
all_data_column arrayi icindeki herhangi bir eleman eger ip_user_pass arrayi icinde ise 
o sutun icindeki satirlardan istediklerini(ornegin o satirdaki Enable sutunundaki sifre) sData  dictionary sine ekle 
''' 
#ip user pass enable lazim 
#ip_user_pass=['Enable', 'External IP','Internal IP-1', 'Internal IP-2', 'Internal IP-3','Password','Username 1 ', 'Username 2']


ip_user_pass=['Internal IP-2']
sessionData = []
for sutun in all_data_column:
	if sutun in ip_user_pass:
		for i in all_data.index:
			enable=all_data['Enable'][i]
			sData = {
				'device_type':"cisco_ios",
				'ip':all_data['Internal IP-2'][i],
				#'ip':all_data['External IP'][i],
				'username':all_data['Username'][i],		
				#'username2':all_data['Username 2'][i],
				'password':all_data['Password'][i],				
				'secret':all_data['Enable'][i]
				
			}
			
			#print (sData)
			#sessionData.append(sData)
			# eger eleman bos degilse dictionary yi nemiko class a gonder.
			if str(all_data['Internal IP-2'][i]) != "nan" :
				try:
					p1 = netmiko_class(komut,sData)
				
				except:
					print (str(all_data['Internal IP-2'][i]) + " olumsuz")
				
				
			'''sData2 = {
				'device_type':"cisco_ios",
				'ip':all_data['External IP'][i],
				'username':all_data['Username 1 '][i],		
				#'username2':all_data['Username 2'][i],
				'password':all_data['Password'][i],				
				'secret':all_data['Enable'][i]
				
			}
			if str(all_data['External IP'][i]) != "nan" :

				try:
					p2 = netmiko_class(komut,sData2)
				
				except:
					print (str(all_data['External IP'][i]) + "ex ip olumsuz")'''

				
			#print(all_data['External IP'][i], all_data['Enable'][i])
			#session_data = all_data['External IP'][i] + all_data['Enable'][i]
			#print (str(all_data['External IP'][i]) + str(all_data['Enable'][i]))
#			print(all_data[sutun][i])


