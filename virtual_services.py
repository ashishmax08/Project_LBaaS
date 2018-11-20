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
		result = {'first':{},'fifth':{},'seventh':{}}
		
		# setting values
		result['first']['VirtPort'] = vport
		result['first']['RealPort'] = rport
		# defult delayed binding set to enabled
		result['first']['DBind'] = 1
		# default persistency mode is set to clientIP
		result['first']['PBind'] = 2
		# defaul redirection is set to group
		result['fifth']['action'] = 1
		result['seventh']['real_group'] = rindex
		# default persistency time out is set to 10 minutes
		result['seventh']['ptimeout'] = 10
		result['seventh']['proxy_mode'] = 4

		url = 'https://'+lb_base.lb_ip+'/config/SlbNewCfgEnhVirtServicesTable/'+str(vindex)
		response = requests.get(url,auth = (cred['username'],cred['password']),verify = False)
		if response.status_code == 200:
			data = response.json()['SlbNewCfgEnhVirtServicesTable']
			if len(data) > 0:
				part_index = max(map(lambda x: int(x['Index']),data)) + 1
			else: part_index = 1

		url = 'https://'+lb_base.lb_ip+'/config/SlbNewCfgEnhVirtServicesTable/'+str(vindex)+'/'+str(part_index)
		payload = "{"
		for k,v in result['first']:
			payload += "\n\t"+k+"\":"+v+","
		payload += "}"
		
		try:
			response = requests.request('POST')



		if kwargs.has_key('dbind'):
			delay_bind(kwargs['dbind'])
		if kwargs.has_key('pbind'):
			persist_bind(kwargs['pbind'])
		if kwargs.has_key('action'):
			action(kwargs['action'])





