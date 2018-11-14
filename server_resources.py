import requests

class Server_Resource(object):
	def __init__(self,ip_addr,port,name):
		ip_addr = self.ip_addr
		port = self.port
		name = self.name


	def ip_check(self):
		# check if server ip already exists
		url = requests.get