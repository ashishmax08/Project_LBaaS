import requests
import json
from lb_base_class import lb_base
from auth import credentials as cred

class ServerResource(lb_base):
	
	def __init__(self):
		self.max_real_server_index = 0
		lb_base.__init__(self)


	def _ip_check(self,ip):		
		# check if server ip already exists
		url = 'https://'+lb_base.lb_ip+'/config/SlbNewCfgEnhRealServerTable'
		response = requests.get(url,auth = (cred['username'],cred['password']), verify = False)

		if response.status_code == 200:
			data = response.json()['SlbNewCfgEnhRealServerTable']
			# adding ip v4 address
			if len(data) > 0:

				ip_addr = list(map(lambda x: x['IpAddr'],data))
				# adding ip v6 address
				ip_addr.extend(list(map(lambda x: x['Ipv6Addr'],filter(lambda x: x['Ipv6Addr'] != None,data))))
				# finding max index of real servers present in LB
				self.max_real_server_index = max(map(lambda x: int(x['Index']),data))

				if ip in ip_addr:
					return {'status':False,'message':'IP Already Present !!','status_code':200}
				else:
					return {'status':True,'message':'Ok','status_code':200}
			else:
				return {'status':True,'message':'Ok','status_code':200}

		else:
			return {'status':False,'message':'Transitional Error','status_code':response.status_code}



	def create_real_server(self,ip_addr,ip_version='v4',name='Created From API'):
		
		if self._ip_check(ip_addr)['status']:
			
			headers = {
						'content-type': "application/json",
						'cache-control': "no-cache",
						}
			if ip_version == 'v4':
				payload_for_api = "{\n\t\t\t\"IpAddr\": \""+ip_addr+"\",\n\t\t\t\"State\": 2,\n\t\t\t\"Type\": 1,\n\t\t\t\"Name\": \""+name+"\",\n\t\t\t\"IpVer\": 1}"
			# elif ip_version == 'v6':
			# 	payload_for_api = {
			# 						"IpAddr": "0.0.0.0",
			# 						"State": 2,
			# 						"Type": 1,
			# 						"Name": name,
			# 						"IpVer": 2,
			# 						"Ipv6Addr": ip_addr									
			# 						}

			index = self.max_real_server_index + 1
			url = 'https://'+lb_base.lb_ip+'/config/SlbNewCfgEnhRealServerTable/'+str(index)
			

			response = requests.request('POST',url,auth = (cred['username'],cred['password']),
										data=payload_for_api,headers=headers,verify = False)
			response_data = response.json()
			if response.status_code == 200:
				if response_data['status'] == 'ok':
					return {'status':True,'message':'Ok','server_index':index,'status_code':200}
				elif response_data['status'] == 'err':
					return {'status':False,'server_error':False,'message':response_data['message'],'status_code':200}

			else:
				return {'status':False,'server_error':True,'message':response.text,'status_code':response.status_code}

		else:
			return {'status':False,'message':'IP Already Present !!','status_code':200}


	def create_server_group(self,name='Group Created From API'):
		headers = {
						'content-type': "application/json",
						'cache-control': "no-cache",
						}
		index = 0

		# for finding max server group index
		url = "https://"+lb_base.lb_ip+"/config/SlbNewCfgEnhGroupTable"
		response = requests.get(url,auth = (cred['username'],cred['password']),verify = False)

		if response.status_code == 200:
			data = response.json()['SlbNewCfgEnhGroupTable']
			if len(data) > 0:
				index = max(map(lambda x: int(x['Index']),data)) + 1
			else:
				index = 1

		if index > 0:
			# default slb metric round robin, health check tcp	
			payload =   "{\n \t\"Metric\":1,\n \t\"HealthCheckLayer\":2,\n \t\"Name\":\""+name+"\",\n \t\"Type\":0\n }"

			url_1 = url + "/"+ str(index)
			response = requests.request('POST',url_1,auth = (cred['username'],cred['password']),data=payload,headers=headers, verify = False)

			if response.status_code == 200:
				response_data = response.json()
				
				if response_data['status'] == 'ok':
					return {'status':True,'message':'Ok','group_index':index,'status_code':200}

				elif response_data['status'] == 'err':
					return {'status':False,'message':response_data['message'],'status_code':200,'group_index':None}

			else:
				return {'status':False,'server_error':True,'message':response.text,'status_code':response.status_code,'group_index':None}
		else:
			return {'status':False,'server_error':True,'message':'Unable to find Index','group_index':None}


	def update_server_group(self,server_index,group_index):
		# we will add real server to the group
		headers = {
						'content-type': "application/json",
						'cache-control': "no-cache",
						}
		url = "https://"+lb_base.lb_ip+"/config/SlbNewCfgEnhGroupTable/"+str(group_index)
		payload = "{\n \t\"AddServer\":"+str(server_index)+"\n }"

		response = requests.request('PUT',url,auth = (cred['username'],cred['password']),data=payload,headers=headers,verify=False)
		if response.status_code == 200:
			return {'status':True,'message':'Ok','status_code':200}
		else:
			return {'status':False,'message':response.text,'status_code':response.status_code}