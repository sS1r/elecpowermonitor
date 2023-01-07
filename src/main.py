from fgApi import fingridApi
from entsoeApi import entsoeApi

from plotdata import plot_data, plot_elecprice

API_URL_FG = 'https://api.fingrid.fi'
API_URL_ENTSOE = 'https://web-api.tp.entsoe.eu/api?'
KEYFILE_FG = './key_fg.txt'
KEYFILE_ENTSOE = './key_entsoe.txt'

def main():
	with open(KEYFILE_FG) as f:
		api_key_fg = f.readline()
	api_fg = fingridApi(url=API_URL_FG, api_key=api_key_fg)

	with open(KEYFILE_ENTSOE) as f:
		api_key_entsoe = f.readline()
	api_entsoe = entsoeApi(url=API_URL_ENTSOE, api_key=api_key_entsoe)

	if api_fg.server_up():
		if api_fg.send_request():
			data = api_fg.get_data()
			plot_data(data)
	else:
		print("Fingrid API down :(")

	if api_entsoe.send_request():
		data = api_entsoe.get_data()
	plot_elecprice(data)

if __name__ == "__main__":
	main()