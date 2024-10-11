'''
ENTSOE Open Data API interface
Because one API interface would be too convenient!
Mainly used for fetching electricity market price, which is not available on Fingrid.

2022-12-14
'''

import requests
import pandas
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone


class timeSeriesData():
	def __init__(self):
		self.data = pandas.DataFrame(columns=("time", "price"))

	# Adds a block of data to time series
	# The data must not overlap the existing data
	def append(self, prices, t_start, t_end):
		assert type(prices)  is list
		assert type(t_start) is datetime
		assert type(t_end)   is datetime

		interval = (t_end - t_start) / len(prices)
		times = [t_start + i * interval for i in range(len(prices))]

		newdata = pandas.DataFrame(index=times, data={"price" : prices})
		newdata.index.name = "time"

		if self.data.empty:
			self.data = newdata
		elif t_end <= self.data.index[0]:
			self.data = pandas.concat([newdata, self.data])
		elif t_start >= self.data.index[-1]:
			self.data = pandas.concat([self.data, newdata])
		else:
			return False
		return True

class entsoeApi():
	def __init__(self, url, api_key, vat):
		self.url = url
		self.token = api_key
		self.data = None
		self.country_code = "10YFI-1--------U"
		self.t_format = "%Y%m%d%H00"
		self.vat = vat
		self.name = "ENTSOE"

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

			# Find period(s)
			periods = ts.findall("ns:Period", namespaces=ns)
			if not periods:
				raise RuntimeError('Time series data not found')

			# Iterate periods
			for period in periods:
				# Find start and end times from period
				interval = period.find("ns:timeInterval", namespaces=ns)
				t_start_str = interval.find("ns:start", namespaces=ns).text
				t_end_str = interval.find("ns:end", namespaces=ns).text

				# Resolve time from the strings (ISO format)
				t_str_format = "%Y-%m-%dT%H:%MZ"
				tz_offset = datetime.now().astimezone().utcoffset()
				t_start = datetime.strptime(t_start_str, t_str_format) + tz_offset
				t_end = datetime.strptime(t_end_str, t_str_format) + tz_offset

				# Find points from period
				points = period.findall("ns:Point", namespaces=ns)

				# Find prices
				pricedata = [0] * max([int(point.find("ns:position", namespaces=ns).text) for point in points])
				for point in points:
					price = float(point.find("ns:price.amount", namespaces=ns).text) / 1000.0
					price = price * (1.0 + self.vat / 100.0)
					pos = int(point.find("ns:position", namespaces=ns).text)
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

		resp = requests.get(url=self.url, headers=headers, params=params)
		if resp.status_code != 200:
			print("entsoeApi: Received HTTP status code {:d}!".format(resp.status_code))
			return False

		self.data = self.parse_data(resp.text)
		return True

	def send_request(self):
		t_end = datetime.now(timezone.utc).astimezone() + timedelta(days=1)
		t_start = t_end - timedelta(hours=48)
		return self.fetch_data(t_start, t_end)

	def get_data(self):
		return self.data

	def save_data(self, filename, format):
		assert type(format) is str
		format = format.lower()

		if self.data:
			if format == "csv":
				self.data.data.to_csv(filename)
			elif format == "excel":
				self.data.data.to_excel(filename)
			elif format == "json":
				self.data.data.to_json(filename)
			elif format == "text":
				self.data.data.to_string(filename)
	# Todo
	def server_up(self):
		return True