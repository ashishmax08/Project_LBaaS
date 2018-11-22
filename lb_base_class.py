import requests
from auth import credentials as cred
from time import sleep

class lb_base(object):
	lb_ip = '127.0.0.1'
	lb_name=None
	lb_type=None
	
	def connect(self):
		count = 0
		state = False

		while count <3:
			url = 'https://'+self.lb_ip+'/config/sysName'
			try:
				response = requests.get(url,auth = (cred['username'],cred['password']), verify = False)
			except Exception as e:
				return {'status':False,'message':str(e)}

			if response.status_code == 200:
				return {'status':True,'status_code':response.status_code}

			sleep(0.5)
			count += 1

		if state == False:
			return {'status':False,'status_code':response.status_code}
