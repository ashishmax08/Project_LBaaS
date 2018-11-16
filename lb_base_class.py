import requests
from auth import credentials as cred
from time import sleep

class lb_base(object):
	def __init__(self,lb_name=None,lb_type=None,lb_ip='10.248.22.185'):
		self.lb_name = lb_name
		self.lb_type = lb_type
		self.lb_ip = lb_ip

	def connect(self):
		count = 0
		state = False

		while count <3:
			url = 'https://'+self.lb_ip+'/config/sysName'
			response = requests.get(url,auth = (cred['username'],cred['password']), verify = False)

			if response.status_code == 200:
				return {'status':True,'status_code':response.status_code}

			sleep(0.5)
			count += 1

		if state == False:
			return {'status':False,'status_code':response.status_code}
