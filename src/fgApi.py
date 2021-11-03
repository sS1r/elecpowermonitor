'''
Fingrid Open Data API interface

2021-11-02
'''

import requests
from datetime import datetime, timedelta, timezone

class fingridVariable():
	def __init__(self, id, string):
		self.id = id
		self.string = string
		self.data = None

	def to_path(self):
		return "/v1/variable/{:d}/events/json".format(self.id)

class fingridApi():
	
	def __init__(self, url, api_key, interval=24):
		self.url = url
		self.api_key = api_key
		self.ready = False
		self.data = {}
		
		# Variable IDs for different data
		self.vars = []
		self.vars.append(fingridVariable(id=192, string="production"))
		self.vars.append(fingridVariable(id=193, string="consumption")) 
		self.vars.append(fingridVariable(id=194, string="import"))
		self.vars.append(fingridVariable(id=195, string="import_russia"))
		self.vars.append(fingridVariable(id=180, string="import_estonia"))
		self.vars.append(fingridVariable(id=187, string="import_norway"))
		self.vars.append(fingridVariable(id=87,  string="import_sweden"))
		self.vars.append(fingridVariable(id=89,  string="import_sweden_mid"))
		self.vars.append(fingridVariable(id=90,  string="import_sweden_aland"))
		

		self.interval = interval
		self.t_format = "%Y-%m-%dT%H:%M:%S%z"
		
	def server_up(self):
		url = self.url + "/ping"
		headers = {"accept" : "application/json"}
		resp = requests.get(url=url, headers=headers)
		return resp.status_code == 200
	
	
	def fetch_var(self, var, t_start, t_end):
		t_start_str = t_start.strftime(self.t_format)
		t_end_str = t_end.strftime(self.t_format)
		headers = {"variableId" : str(var.id), "x-api-key" : self.api_key}
		params = {"start_time" : t_start_str, "end_time" : t_end_str}
		
		url = self.url + var.to_path()
		
		resp = requests.get(url=url, headers=headers, params=params)
		if resp.status_code != 200:
			return False
		
		var.data = resp.json()
		return True
	
	def send_request(self):
	
		t_end = datetime.now(timezone.utc).astimezone()
		t_start = t_end - timedelta(hours = self.interval)
		
		#import pdb; pdb.set_trace()
		
		# Fetch the data
		print("Fetching data from Fingrid...")
		for var in self.vars:
			if not self.fetch_var(var, t_start, t_end):
				return False
		print("Done!")
		
		# Parse data
		for var in self.vars:
			t0 = datetime.strptime(var.data[0]["start_time"], self.t_format)
			self.data[var.string] = {}
			self.data[var.string]["values"] = [d["value"] for d in var.data]
			self.data[var.string]["time"] = [(datetime.strptime(d["start_time"], self.t_format) - t0).total_seconds() / 3600 for d in var.data]
		
		# import pdb; pdb.set_trace()
		
		return True
		
	def get_data(self):
		return self.data
