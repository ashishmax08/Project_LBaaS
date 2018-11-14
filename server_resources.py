import requests
import json
from lb_base_class import lb_base
from auth import credentials as cred

class Server_Resource(object,lb_base):
	self.max_real_server_index = 0
	def __init__(self):
		pass


	def _ip_check(self):		
		# check if server ip already exists
		url = 'https://'+self.lb_ip+'/config/SlbNewCfgEnhRealServerTable'
		response = requests.get(url,auth = (cred['username'],cred['password']), verify = False)

		if response.status_code == 200:
			data = response.json()['SlbNewCfgEnhRealServerTable']
			# adding ip v4 address
			ip_addr = list(map(lambda x: x['IpAddr'],data))
			# adding ip v6 address
			ip_addr.extend(list(map(lambda x: x['Ipv6Addr'],filter(lambda x: x['Ipv6Addr'] != None,data))))
			# finding max index of real servers present in LB
			self.max_real_server_index = max(map(lambda x: int(x['Index']),data))

			if self.ip_addr in ip_addr:
				return {'status':False,'message':'IP Already Present !!','status_code':200}
			else:
				return {'status':True,'message':'Ok','status_code':200}

		else:
			return {'status':False,'message':'Transitional Error','status_code':response.status_code}



	def create_real_server(self,ip_addr,ip_version,name):
		
		if ip_check()['status']:
			headers = {
	    				'content-type': "application/json",
	    				'cache-control': "no-cache",
	    				}
	    	if ip_version == 'v4':
		    	payload_for_api = {
									"IpAddr": ip_addr,
									"State": 2,
									"Type": 1,
									"Name": name,
									"IpVer": 1,									
									}
			elif ip_version == 'v6':
				payload_for_api = {
									"IpAddr": "0.0.0.0",
									"State": 2,
									"Type": 1,
									"Name": name,
									"IpVer": 2,
									"Ipv6Addr": ip_addr									
									}

			index = self.max_real_server_index + 1
			url = 'https://'+self.lb_ip+'/config/SlbNewCfgEnhRealServerTable/'+str(index)

			response = requests.request('POST',url,auth = (cred['username'],cred['password']),
										data=json.dumps(payload_for_api),verify = False)
			response_data = response.json()
			if response.status_code == 200:
				if response_data['status'] == 'ok':
					return {'status':True,'message':'Ok','server_index':index,'status_code':200}
				elif response_data['status'] == 'err':
					return {'status':False,'server_error':False,'message':response_data['message'],'status_code':200}

			else:
				return {'status':False,'server_error':True,'message':'Server Error','status_code':response.status_code}

		else:
			return {'status':False,'message':'IP Already Present !!','status_code':200}


	def create_server_group(self,name):

		index = 0

		# for finding max server group index
		url = "https://"+self.lb_ip+"/config/SlbNewCfgEnhGroupTable"
		response = requests.get(url,auth = (cred['username'],cred['password']),verify = False)

		if response.status_code == 200:
			data = response.json()['SlbNewCfgEnhGroupTable']
			index = max(map(lambda x: int(x['Index']),data)) + 1

		if index > 0:
			# default slb metric round robin, health check tcp	
			payload =  {							
							"Metric":1,
							"HealthCheckLayer":2,
							"Name":name,
							"Type":0
						}

			url_1 = url + "/"+ str(index)
			response = requests.request('POST',url_1,auth = (cred['username'],cred['password']), verify = False)

			if response.status_code == 200:
				response_data = response.json()
				
				if response_data['status'] == 'ok':
					return {'status':True,'message':'Ok','group_index':index,'status_code':200}

				elif response_data['status'] == 'err':
					return {'status':False,'message':response_data['message'],'status_code':200}

			else:
				return {'status':False,'server_error':True,'message':'Server Error','status_code':response.status_code}


	def update_server_group(self,server_index,group_index):
		# we will add real server to the group
		
		url = "https://"+self.lb_ip+"/config/SlbNewCfgEnhGroupTable/"+str(group_index)
		payload = {"AddServer":str(server_index)}

		response = requests.request('PUT',url,auth = (cred['username'],cred['password']),verify=False)
		if response.status_code == 200:
			return {'status':True,'message':'Ok','status_code':200}
		else:
			return {'status':False,'message':'Server Add Failed','status_code':200}



