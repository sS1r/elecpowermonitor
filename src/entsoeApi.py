'''
ENTSOE Open Data API interface
Because one API interface would be too convenient!
Mainly used for fetching electricity market price, which is not available on Fingrid.

2022-12-14
'''

import requests
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone


class timeSeriesData():
	def __init__(self):
		self.prices = []
		self.time = []

	# Adds a block of data to time series
	# The data must not overlap the existing data
	def append(self, prices, t_start, t_end):
		assert type(prices)  is list
		assert type(t_start) is datetime
		assert type(t_end)   is datetime

		interval = (t_end - t_start) / len(prices)
		times = [t_start + i * interval for i in range(len(prices))]

		if not self.time:
			self.prices = prices
			self.time = times
		elif t_end < self.time[0]:
			self.prices = prices + self.prices
			self.time   = times + self.time
		elif t_start > self.time[-1]:
			self.prices = self.prices + prices
			self.time   = self.time + times
		else:
			return False
		return True

class entsoeApi():
	def __init__(self, url, api_key, vat=0.0):
		self.url = url
		self.token = api_key
		self.data = None
		self.country_code = "10YFI-1--------U"
		self.t_format = "%Y%m%d%H00"
		self.vat = vat

	def parse_data(self, data):
		root = ET.fromstring(data)

		# Resolve namespace
		match = re.match(r'\{.*\}', root.tag)
		if match:
			ns = {'ns' : match.group(0)[1:-1]}
		else:
			raise RuntimeError('Could not resolve namespace')

		# Find all TimeSeries elements
		timeSeries = root.findall("ns:TimeSeries", namespaces=ns)
		if not timeSeries:
			raise RuntimeError('Could not find time series')

		# Iterate TimeSeries
		tsdata = timeSeriesData()
		for ts in timeSeries:

			# Find period
			period = ts.findall("ns:Period", namespaces=ns)
			if not period or len(period) != 1:
				raise RuntimeError('Could not parse time series')

			# Find start and end times from period
			interval = period[0].find("ns:timeInterval", namespaces=ns)
			t_start_str = interval.find("ns:start", namespaces=ns).text
			t_end_str = interval.find("ns:end", namespaces=ns).text

			# Resolve time from the strings (ISO format)
			t_start = datetime.fromisoformat(t_start_str)
			t_end = datetime.fromisoformat(t_end_str)

			# Find points from period
			points = period[0].findall("ns:Point", namespaces=ns)

			# Find prices
			pricedata = [0] * len(points)
			for p in points:
				price = float(p.find("ns:price.amount", namespaces=ns).text) / 1000.0
				pos = int(p.find("ns:position", namespaces=ns).text)
				pricedata[pos - 1] = price

			# Append prices to data container
			assert tsdata.append(pricedata, t_start, t_end)

		return tsdata

	def fetch_data(self, t_start, t_end):
		t_start_str = t_start.strftime(self.t_format)
		t_end_str = t_end.strftime(self.t_format)

		headers = {}
		params = {}
		params["securityToken"] = self.token
		params["In_Domain"] = self.country_code
		params["Out_Domain"] = self.country_code
		params["DocumentType"] = "A44"
		params["periodStart"] = t_start_str
		params["periodEnd"] = t_end_str

		url = self.url
		# import pdb; pdb.set_trace()
		resp = requests.get(url=url, headers=headers, params=params)
		if resp.status_code != 200:
			return False

		self.data = self.parse_data(resp.text)
		return True

	def send_request(self):
		t_end = datetime.now(timezone.utc).astimezone() + timedelta(days=1)
		t_start = t_end - timedelta(hours=48)

		if not self.fetch_data(t_start, t_end):
			return False
		return True

	def get_data(self):
		return self.data