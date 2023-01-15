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
def run_api(api_key, url, api_class):
	api = api_class(url=url, api_key=api_key)
	if api.server_up():
		if api.send_request():
			return api
		else:
			print("Request to " + api.name +  " failed!")
	else:
		print(api.name + " API down!")
	return None


'''
Resolves API key from command line options and default values.
The priorities are:

1. API key passed from command line
2. API key file passed from command line
3. Default API key file

Returns: None
'''
def resolve_api_key(ctx, default_file):
	if not ctx.obj["api_key"]:
		if not ctx.obj["api_keyfile"]:
			ctx.obj["api_keyfile"] = default_file
		with open(ctx.obj["api_keyfile"]) as f:
			ctx.obj["api_key"] = f.readline()


@click.group()
@click.option('--api-key',     required=False, nargs=1, type=str, help='Give API key on command line instead of reading from file')
@click.option('--api-keyfile', required=False, nargs=1, type=str, help='API key file')
@click.pass_context
def main(ctx, api_key, api_keyfile):
	ctx.ensure_object(dict)
	ctx.obj["api_key"] = api_key
	ctx.obj["api_keyfile"] = api_keyfile

@main.group()
@click.pass_context
def price(ctx):
	resolve_api_key(ctx, KEYFILE_ENTSOE)

@main.group()
@click.pass_context
def fingrid(ctx):
	resolve_api_key(ctx, KEYFILE_FG)

@price.command(name="plot")
@click.option('--hide', required=False,  is_flag=True, help='Do not display the interactive plot')
@click.option('--save', required=False,  nargs=1, type=str, help='Save the image with given file name')
@click.pass_context
def plot(ctx, hide, save):
	api = run_api(api_key=ctx.obj["api_key"], url=API_URL_ENTSOE, api_class=entsoeApi)
	if api:
		plot_elecprice(api.get_data(), hide=hide, fname=save)

@price.command(name="fetch")
@click.option('--format',   required=False, nargs=1, type=click.Choice(DATA_FORMAT_OPTIONS, case_sensitive=False), help='Data format')
@click.option('--filename', required=False, nargs=1, type=str, help='Filename')
@click.pass_context
def fetch(ctx, format, filename):
	api = run_api(api_key=ctx.obj["api_key"], url=API_URL_ENTSOE, api_class=entsoeApi)
	if api:
		api.save_data(filename, format)

@fingrid.command(name="plot")
@click.option('--hide', required=False,  is_flag=True, help='Do not display the interactive plot')
@click.option('--save', required=False,  nargs=1, type=str, help='Save the image with given file name')
@click.pass_context
def plot(ctx, hide, save):
	api = run_api(api_key=ctx.obj["api_key"], url=API_URL_FG, api_class=fingridApi)
	if api:
		plot_data(api.get_data(), hide=hide, fname=save)

@fingrid.command(name="fetch")
@click.option('--format',   required=False, nargs=1, type=click.Choice(DATA_FORMAT_OPTIONS, case_sensitive=False), help='Data format')
@click.option('--filename', required=False, nargs=1, type=str, help='Filename')
@click.pass_context
def fetch(ctx, format, filename):
	api = run_api(api_key=ctx.obj["api_key"], url=API_URL_FG, api_class=fingridApi)
	if api:
		api.save_data(filename, format)

if __name__ == "__main__":
	main(obj={})