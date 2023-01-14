import click

from fgApi import fingridApi
from entsoeApi import entsoeApi

from plotdata import plot_data, plot_elecprice

API_URL_FG = 'https://api.fingrid.fi'
API_URL_ENTSOE = 'https://web-api.tp.entsoe.eu/api?'
KEYFILE_FG = './key_fg.txt'
KEYFILE_ENTSOE = './key_entsoe.txt'

DATA_FORMAT_OPTIONS = ['CSV', 'XLSX', 'JSON', 'TXT']


'''
Opens API key and sends request to fetch data from it

Returns: API object if successful, None otherwise
'''
def run_api(keyfile, url, api_class):
	with open(keyfile) as f:
		api_key = f.readline()
	api = api_class(url=url, api_key=api_key)

	if api.server_up():
		if api.send_request():
			return api
		else:
			print("Request to " + api.name +  " failed!")
	else:
		print(api.name + " API down!")
	return None

@click.group()
def main():
	pass

@main.group()
def price():
	pass

@main.group()
def fingrid():
	pass

@price.command(name="plot")
@click.option('--hide', required=False,  is_flag=True, help='Do not display the interactive plot')
@click.option('--save', required=False,  nargs=1, type=str, help='Save the image with given file name')
def plot(hide, save):
	api = run_api(keyfile=KEYFILE_ENTSOE, url=API_URL_ENTSOE, api_class=entsoeApi)
	if api:
		plot_elecprice(api.get_data())

@price.command(name="fetch")
@click.option('--format',   required=False, nargs=1, type=click.Choice(DATA_FORMAT_OPTIONS, case_sensitive=False), help='Data format')
@click.option('--filename', required=False, nargs=1, type=str, help='Filename')
def fetch(format, filename):
	api = run_api(keyfile=KEYFILE_ENTSOE, url=API_URL_ENTSOE, api_class=entsoeApi)
	if api:
		api.save_data(filename, format)

@fingrid.command(name="plot")
@click.option('--hide', required=False,  is_flag=True, help='Do not display the interactive plot')
@click.option('--save', required=False,  nargs=1, type=str, help='Save the image with given file name')
def plot(hide, save):
	api = run_api(keyfile=KEYFILE_FG, url=API_URL_FG, api_class=fingridApi)
	if api:
		plot_data(api.get_data())

@fingrid.command(name="fetch")
@click.option('--format',   required=False, nargs=1, type=click.Choice(DATA_FORMAT_OPTIONS, case_sensitive=False), help='Data format')
@click.option('--filename', required=False, nargs=1, type=str, help='Filename')
def fetch(format, filename):
	api = run_api(keyfile=KEYFILE_FG, url=API_URL_FG, api_class=fingridApi)
	if api:
		api.save_data(filename, format)

if __name__ == "__main__":
	main()