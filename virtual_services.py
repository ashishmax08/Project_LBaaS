import requests
import json
from lb_base_class import lb_base
from auth import credentials as cred



class VirtualServer(lb_base):
	def __init__(self):
		lb_base.__init__(self)

	def create_virtual_server(self,ip_addr,name="VirtualServer Createc From API"):
		index = 1
		headers = {
				'content-type': "application/json",
				'cache-control': "no-cache",
				}
		# find max index
		url = "https://"+lb_base.lb_ip+"/config/SlbNewCfgEnhVirtServerTable"
		response = requests.get(url,auth = (cred['username'],cred['password']),verify = False)
		if response.status_code == 200:
			data = response.json()['SlbNewCfgEnhVirtServerTable']
			if len(data) > 0:
				index = max(map(lambda x: int(x['VirtServerIndex']),data)) + 1


		url_1 = "https://"+lb_base.lb_ip+"/config/SlbNewCfgEnhVirtServerTable/"+str(index)
		payload = "{\n\t\"VirtServerIpAddress\":\""+ip_addr+"\",\n\t\"VirtServerState\":2,\n\t\"VirtServerVname\":\""+name+"\",\n\t\"VirtServerIpVer\":1,\n\t\"VirtServerRtSrcMac\":1\n}"

		response =requests.request('POST',url_1,auth = (cred['username'],cred['password']),data = payload,verify = False)

		if response.status_code == 200:
			return {'status':True,'server_error':False,'message':response.text,'vserver_index':index,'status_code':200}
		else:
			return {'status':False,'server_error':True,'message':response.text,'vserver_index':None,'status_code':response.status_code}


	def create_virtual_service(self,vport,rport,vindex,rindex,**kwargs):
		headers = {
				'content-type': "application/json",
				'cache-control': "no-cache",
				}
		result = {'first':{},'fifth':{},'seventh':{}}

		request = {}
		
		# setting values
		result['first']['VirtPort'] = vport
		result['first']['RealPort'] = rport
		# defult delayed binding set to enabled
		result['first']['DBind'] = 1
		# default persistency mode is set to clientIP
		result['first']['PBind'] = 2
		# defaul redirection is set to group
		result['fifth']['Action'] = 1
		result['fifth']['ServApplicationType'] = 6
		result['seventh']['RealGroup'] = rindex
		# default persistency time out is set to 10 minutes
		result['seventh']['PersistentTimeOut'] = 10
		result['seventh']['ProxyIpMode'] = 4

		url = 'https://'+lb_base.lb_ip+'/config/SlbNewCfgEnhVirtServicesTable/'+str(vindex)
		response = requests.get(url,auth = (cred['username'],cred['password']),verify = False)
		if response.status_code == 200:
			data = response.json()['SlbNewCfgEnhVirtServicesTable']
			if len(data) > 0:
				part_index = max(map(lambda x: int(x['Index']),data)) + 1
			else: part_index = 1

		if kwargs.has_key('dbind'):
			result = self.delay_bind(kwargs['dbind'],result)
		if kwargs.has_key('pbind'):
			persist_bind(kwargs['pbind'])
		if kwargs.has_key('action'):
			action(kwargs['action'])

		# --------------pushing configurations to LB------------


		url = 'https://'+lb_base.lb_ip+'/config/SlbNewCfgEnhVirtServicesTable/'+str(vindex)+'/'+str(part_index)
		url_5 = 'https://'+lb_base.lb_ip+'/config/SlbNewCfgEnhVirtServicesFifthPartTable/'+str(vindex)+'/'+str(part_index)
		url_7 = 'https://'+lb_base.lb_ip+'/config/SlbNewCfgEnhVirtServicesSeventhPartTable/'+str(vindex)+'/'+str(part_index)

		# dynamically building json data according to the updated as per result
		
		payload = "{"
		payload_5 = "{"
		payload_7 = "{"
		
		for k,v in result['first'].items():
			payload += "\n\t\""+k+"\":"+str(v)+","
		payload += "}"
		
		for k,v in result['fifth'].items():
			payload_5 += "\n\t\""+k+"\":"+str(v)+","
		payload_5 += "}"
		

		for k,v in result['seventh'].items():
			payload_7 += "\n\t\""+k+"\":"+str(v)+","
		payload_7 += "}"
		

		
		try:
			response = requests.request('POST',url,auth = (cred['username'],cred['password']),data = payload ,headers = headers,verify = False)
			response_5 = requests.request('PUT',url_5,auth = (cred['username'],cred['password']),data = payload_5,headers = headers ,verify = False)
			response_7 = requests.request('PUT',url_7,auth = (cred['username'],cred['password']),data = payload_7,headers = headers ,verify = False)
			if response.status_code == 200 and response_5.status_code == 200 and response_7.status_code == 200:
				return {'status':True,'server_error':False,'message':response.text,'status_code':200}
			else:
				return {'status':False,'server_error':True,
					'message':{'first':response.text,'fifth':response_5.text,'seventh':response_7.text},
					'status_code':{'first':response.status_code,'fifth':response_5.status_code,'seventh':response_7.status_code}}
		except Exception as e:
			return {'status':False,'message':'Internal Error\n'+str(e)}



	def delay_bind(self,value,result):
		print 'Im here\n'
		if value == 'disable':
			result['first']['DBind'] = 2
			return result
		elif value == 'force_proxy':
			result['first']['DBind'] = 3
			return result

		else:	return result




