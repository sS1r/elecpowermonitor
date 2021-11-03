from fgApi import fingridApi
from plotdata import plot_data

API_URL = 'https://api.fingrid.fi'
KEYFILE = '../key.txt'

with open(KEYFILE) as f: api_key = f.readline()
api = fingridApi(url=API_URL, api_key=api_key)

if api.server_up():
	if api.send_request():
		data = api.get_data()
		plot_data(data)